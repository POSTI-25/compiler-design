"""AST-to-IR generation for the current AEGIS language."""

from __future__ import annotations

from collections.abc import Iterable

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
    PowerCommand,
    RepeatStatement,
    SafeModeCommand,
    StringLiteral,
    TransmitImageCommand,
    UnaryExpression,
    WaitCommand,
)

from .nodes import (
    IRBinary,
    IRBlock,
    IRCamera,
    IRCaptureImage,
    IRExpression,
    IRIdentifier,
    IRIf,
    IRLiteral,
    IRMove,
    IRPower,
    IRProgram,
    IRRepeat,
    IRSafeMode,
    IRTransmitImage,
    IRUnary,
    IRWait,
)


class IRGenerationError(Exception):
    """Raised when IR generation cannot safely proceed."""


class IRGenerator:
    """Translate a validated AST into deterministic structured IR."""

    def generate(self, program: Mission | None, semantic_diagnostics: Iterable[object] = ()) -> IRProgram:
        if program is None:
            raise IRGenerationError("Cannot generate IR without a parsed mission")
        if tuple(semantic_diagnostics):
            raise IRGenerationError("Cannot generate IR while semantic diagnostics exist")

        return IRProgram(
            program.name,
            self._generate_block(program.body),
            location=program.location,
        )

    def _generate_block(self, block: Block) -> IRBlock:
        instructions = tuple(self._generate_statement(statement) for statement in block.statements)
        return IRBlock(instructions, location=block.location)

    def _generate_statement(self, statement: object):
        if isinstance(statement, PowerCommand):
            return IRPower(self._generate_expression(statement.value), location=statement.location)
        if isinstance(statement, MoveCommand):
            return IRMove(self._generate_expression(statement.distance), location=statement.location)
        if isinstance(statement, CameraCommand):
            return IRCamera(statement.enabled, location=statement.location)
        if isinstance(statement, CaptureImageCommand):
            return IRCaptureImage(location=statement.location)
        if isinstance(statement, TransmitImageCommand):
            return IRTransmitImage(location=statement.location)
        if isinstance(statement, WaitCommand):
            return IRWait(self._generate_expression(statement.duration), location=statement.location)
        if isinstance(statement, SafeModeCommand):
            return IRSafeMode(location=statement.location)
        if isinstance(statement, IfStatement):
            return IRIf(
                self._generate_expression(statement.condition),
                self._generate_block(statement.then_branch),
                self._generate_block(statement.else_branch) if statement.else_branch else None,
                location=statement.location,
            )
        if isinstance(statement, RepeatStatement):
            return IRRepeat(
                self._generate_expression(statement.count),
                self._generate_block(statement.body),
                location=statement.location,
            )
        raise IRGenerationError(f"Unsupported AST statement: {type(statement).__name__}")

    def _generate_expression(self, expression: Expression) -> IRExpression:
        if isinstance(expression, (NumberLiteral, StringLiteral, BooleanLiteral)):
            return IRLiteral(expression.value, location=expression.location)
        if isinstance(expression, Identifier):
            return IRIdentifier(expression.name, location=expression.location)
        if isinstance(expression, UnaryExpression):
            return IRUnary(
                expression.operator,
                self._generate_expression(expression.operand),
                location=expression.location,
            )
        if isinstance(expression, BinaryExpression):
            return IRBinary(
                self._generate_expression(expression.left),
                expression.operator,
                self._generate_expression(expression.right),
                location=expression.location,
            )
        raise IRGenerationError(f"Unsupported AST expression: {type(expression).__name__}")
