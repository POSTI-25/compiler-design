"""Semantic analysis for the current AEGIS AST."""

from __future__ import annotations

from dataclasses import dataclass
from aegis.ast import (
    BinaryExpression,
    Block,
    BooleanLiteral,
    CameraCommand,
    CaptureImageCommand,
    Expression,
    Identifier,
    IfStatement,
    Mission,
    MoveCommand,
    NumberLiteral,
    RepeatStatement,
    SafeModeCommand,
    SourceLocation,
    StringLiteral,
    TransmitImageCommand,
    UnaryExpression,
    WaitCommand,
    PowerCommand,
)

from .diagnostics import SemanticDiagnostic
from .symbols import Symbol, SymbolKind, SymbolTable

NUMBER_TYPES = {"integer", "decimal", "number"}
STATE_TYPES = {
    "BATTERY": "number",
    "TEMPERATURE": "number",
    "VISIBILITY": "boolean",
}
MAX_REPEAT_COUNT = 1000


@dataclass
class _RuntimeFacts:
    camera_on: bool = False
    image_captured: bool = False

    def copy(self) -> _RuntimeFacts:
        return _RuntimeFacts(self.camera_on, self.image_captured)

    def merge(self, other: _RuntimeFacts) -> _RuntimeFacts:
        return _RuntimeFacts(
            camera_on=self.camera_on and other.camera_on,
            image_captured=self.image_captured and other.image_captured,
        )


class SemanticAnalyzer:
    """Build symbols and validate types and domain rules without executing code."""

    def __init__(self) -> None:
        self.symbol_table = SymbolTable()
        self.diagnostics: list[SemanticDiagnostic] = []
        self._install_state_symbols()

    def analyze(self, program: Mission | None) -> list[SemanticDiagnostic]:
        self.diagnostics.clear()
        if program is None:
            return self.diagnostics

        mission_symbol = Symbol(
            program.name,
            SymbolKind.MISSION,
            "mission",
            program.location,
        )
        if not self.symbol_table.define(mission_symbol):
            self._report("SEM001", "Duplicate mission symbol", program.location, program.name)
        self._analyze_block(program.body, _RuntimeFacts())
        return list(self.diagnostics)

    def _install_state_symbols(self) -> None:
        for name, type_name in STATE_TYPES.items():
            self.symbol_table.define(
                Symbol(name, SymbolKind.STATE, type_name, SourceLocation(1, 1))
            )

    def _analyze_block(self, block: Block, facts: _RuntimeFacts) -> _RuntimeFacts:
        for statement in block.statements:
            if isinstance(statement, PowerCommand):
                self._check_numeric_command(statement.value, statement.location, "POWER")
                self._check_power_range(statement.value)
            elif isinstance(statement, MoveCommand):
                self._check_numeric_command(statement.distance, statement.location, "MOVE")
                self._check_nonnegative(statement.distance, statement.location, "MOVE distance", "SEM007")
            elif isinstance(statement, WaitCommand):
                self._check_numeric_command(statement.duration, statement.location, "WAIT")
                self._check_nonnegative(statement.duration, statement.location, "WAIT duration", "SEM003")
            elif isinstance(statement, CameraCommand):
                facts.camera_on = statement.enabled
            elif isinstance(statement, CaptureImageCommand):
                if not facts.camera_on:
                    self._report(
                        "SEM008",
                        "Cannot capture IMAGE while the camera is off",
                        statement.location,
                    )
                else:
                    facts.image_captured = True
            elif isinstance(statement, TransmitImageCommand):
                if not facts.image_captured:
                    self._report(
                        "SEM009",
                        "Cannot transmit IMAGE because no image has been captured",
                        statement.location,
                    )
            elif isinstance(statement, IfStatement):
                condition_type = self._expression_type(statement.condition)
                if condition_type not in {"boolean", "unknown"}:
                    self._report("SEM004", "IF condition must be boolean", statement.condition.location)
                then_facts = self._analyze_block(statement.then_branch, facts.copy())
                if statement.else_branch is None:
                    facts = facts.merge(then_facts)
                else:
                    else_facts = self._analyze_block(statement.else_branch, facts.copy())
                    facts = then_facts.merge(else_facts)
            elif isinstance(statement, RepeatStatement):
                self._check_repeat_count(statement.count)
                body_facts = self._analyze_block(statement.body, facts.copy())
                facts = facts.merge(body_facts)
            elif isinstance(statement, SafeModeCommand):
                continue
        return facts

    def _check_numeric_command(self, expression: Expression, location: SourceLocation, command: str) -> None:
        expression_type = self._expression_type(expression)
        if expression_type not in NUMBER_TYPES and expression_type != "unknown":
            self._report("SEM003", f"{command} argument must be numeric", location)

    def _check_power_range(self, expression: Expression) -> None:
        value = self._constant_number(expression)
        if value is not None and not 0 <= value <= 100:
            self._report("SEM006", "POWER value must be between 0 and 100", expression.location)

    def _check_nonnegative(self, expression: Expression, location: SourceLocation, name: str, code: str) -> None:
        value = self._constant_number(expression)
        if value is not None and value < 0:
            self._report(code, f"{name} must be nonnegative", location)

    def _check_repeat_count(self, expression: Expression) -> None:
        expression_type = self._expression_type(expression)
        if expression_type not in {"integer", "unknown"}:
            self._report("SEM005", "REPEAT count must be an integer", expression.location)
            return
        value = self._constant_number(expression)
        if value is not None and (value < 0 or value > MAX_REPEAT_COUNT or int(value) != value):
            self._report("SEM005", f"REPEAT count must be between 0 and {MAX_REPEAT_COUNT}", expression.location)

    def _expression_type(self, expression: Expression) -> str:
        if isinstance(expression, NumberLiteral):
            return "integer" if isinstance(expression.value, int) else "decimal"
        if isinstance(expression, StringLiteral):
            return "string"
        if isinstance(expression, BooleanLiteral):
            return "boolean"
        if isinstance(expression, Identifier):
            symbol = self.symbol_table.lookup(expression.name)
            if symbol is None:
                self._report("SEM002", "Undefined identifier", expression.location, expression.name)
                return "unknown"
            return symbol.type_name
        if isinstance(expression, UnaryExpression):
            operand_type = self._expression_type(expression.operand)
            if operand_type not in NUMBER_TYPES and operand_type != "unknown":
                self._report("SEM003", "Unary operator requires a numeric operand", expression.location)
                return "unknown"
            return operand_type
        if isinstance(expression, BinaryExpression):
            left_type = self._expression_type(expression.left)
            right_type = self._expression_type(expression.right)
            if left_type == "unknown" or right_type == "unknown":
                return "unknown"
            if expression.operator in {"+", "-", "*", "/"}:
                if left_type not in NUMBER_TYPES or right_type not in NUMBER_TYPES:
                    self._report("SEM003", "Arithmetic operators require numeric operands", expression.location)
                    return "unknown"
                return "decimal" if "decimal" in {left_type, right_type} else "integer"
            if expression.operator in {"<", "<=", ">", ">="}:
                if left_type not in NUMBER_TYPES or right_type not in NUMBER_TYPES:
                    self._report("SEM003", "Relational operators require numeric operands", expression.location)
                    return "unknown"
                return "boolean"
            if expression.operator in {"==", "!="}:
                if not self._types_compatible(left_type, right_type):
                    self._report("SEM003", "Equality operands must have compatible types", expression.location)
                return "boolean"
        return "unknown"

    @staticmethod
    def _types_compatible(left_type: str, right_type: str) -> bool:
        return left_type == right_type or left_type in NUMBER_TYPES and right_type in NUMBER_TYPES

    def _constant_number(self, expression: Expression) -> float | None:
        if isinstance(expression, NumberLiteral):
            return float(expression.value)
        if isinstance(expression, UnaryExpression):
            value = self._constant_number(expression.operand)
            if value is None:
                return None
            return value if expression.operator == "+" else -value
        if isinstance(expression, BinaryExpression):
            left = self._constant_number(expression.left)
            right = self._constant_number(expression.right)
            if left is None or right is None:
                return None
            if expression.operator == "+":
                return left + right
            if expression.operator == "-":
                return left - right
            if expression.operator == "*":
                return left * right
            if expression.operator == "/" and right != 0:
                return left / right
        return None

    def _report(self, code: str, message: str, location: SourceLocation, symbol: str | None = None) -> None:
        self.diagnostics.append(SemanticDiagnostic(code, message, location.line, location.column, symbol))
