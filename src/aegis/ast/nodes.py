"""Readable dataclass-based AST nodes for AEGIS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SourceLocation:
    line: int
    column: int


@dataclass(frozen=True, slots=True, kw_only=True)
class AstNode:
    location: SourceLocation


@dataclass(frozen=True, slots=True)
class Mission(AstNode):
    name: str
    body: Block


@dataclass(frozen=True, slots=True)
class Block(AstNode):
    statements: tuple[Statement, ...]


@dataclass(frozen=True, slots=True)
class Statement(AstNode):
    pass


@dataclass(frozen=True, slots=True)
class PowerCommand(Statement):
    value: Expression


@dataclass(frozen=True, slots=True)
class MoveCommand(Statement):
    distance: Expression


@dataclass(frozen=True, slots=True)
class CameraCommand(Statement):
    enabled: bool


@dataclass(frozen=True, slots=True)
class CaptureImageCommand(Statement):
    pass


@dataclass(frozen=True, slots=True)
class TransmitImageCommand(Statement):
    pass


@dataclass(frozen=True, slots=True)
class WaitCommand(Statement):
    duration: Expression


@dataclass(frozen=True, slots=True)
class SafeModeCommand(Statement):
    pass


@dataclass(frozen=True, slots=True)
class IfStatement(Statement):
    condition: Expression
    then_branch: Block
    else_branch: Block | None


@dataclass(frozen=True, slots=True)
class RepeatStatement(Statement):
    count: Expression
    body: Block


@dataclass(frozen=True, slots=True)
class Expression(AstNode):
    pass


@dataclass(frozen=True, slots=True)
class NumberLiteral(Expression):
    value: int | float


@dataclass(frozen=True, slots=True)
class StringLiteral(Expression):
    value: str


@dataclass(frozen=True, slots=True)
class BooleanLiteral(Expression):
    value: bool


@dataclass(frozen=True, slots=True)
class Identifier(Expression):
    name: str


@dataclass(frozen=True, slots=True)
class BinaryExpression(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass(frozen=True, slots=True)
class UnaryExpression(Expression):
    operator: str
    operand: Expression


def ast_to_dict(node: Any) -> Any:
    """Convert AST nodes to plain data for readable inspection."""
    if isinstance(node, AstNode):
        result = {"type": type(node).__name__, "line": node.location.line, "column": node.location.column}
        for field_name in node.__dataclass_fields__:
            if field_name != "location":
                result[field_name] = ast_to_dict(getattr(node, field_name))
        return result
    if isinstance(node, tuple):
        return [ast_to_dict(item) for item in node]
    return node
