"""Readable, structured intermediate representation nodes for AEGIS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aegis.ast import SourceLocation


@dataclass(frozen=True, slots=True, kw_only=True)
class IRNode:
    location: SourceLocation


@dataclass(frozen=True, slots=True)
class IRProgram(IRNode):
    name: str
    body: IRBlock


@dataclass(frozen=True, slots=True)
class IRBlock(IRNode):
    instructions: tuple[IRInstruction, ...]


@dataclass(frozen=True, slots=True)
class IRInstruction(IRNode):
    pass


@dataclass(frozen=True, slots=True)
class IRPower(IRInstruction):
    value: IRExpression


@dataclass(frozen=True, slots=True)
class IRMove(IRInstruction):
    distance: IRExpression


@dataclass(frozen=True, slots=True)
class IRCamera(IRInstruction):
    enabled: bool


@dataclass(frozen=True, slots=True)
class IRCaptureImage(IRInstruction):
    pass


@dataclass(frozen=True, slots=True)
class IRTransmitImage(IRInstruction):
    pass


@dataclass(frozen=True, slots=True)
class IRWait(IRInstruction):
    duration: IRExpression


@dataclass(frozen=True, slots=True)
class IRSafeMode(IRInstruction):
    pass


@dataclass(frozen=True, slots=True)
class IRIf(IRInstruction):
    condition: IRExpression
    then_block: IRBlock
    else_block: IRBlock | None


@dataclass(frozen=True, slots=True)
class IRRepeat(IRInstruction):
    count: IRExpression
    body: IRBlock


@dataclass(frozen=True, slots=True)
class IRExpression(IRNode):
    pass


@dataclass(frozen=True, slots=True)
class IRLiteral(IRExpression):
    value: int | float | str | bool


@dataclass(frozen=True, slots=True)
class IRStringLiteral(IRLiteral):
    value: str


@dataclass(frozen=True, slots=True)
class IRBooleanLiteral(IRLiteral):
    value: bool


@dataclass(frozen=True, slots=True)
class IRIdentifier(IRExpression):
    name: str


@dataclass(frozen=True, slots=True)
class IRUnary(IRExpression):
    operator: str
    operand: IRExpression


@dataclass(frozen=True, slots=True)
class IRBinary(IRExpression):
    left: IRExpression
    operator: str
    right: IRExpression


def render_ir(program: IRProgram) -> str:
    """Render structured IR deterministically for reports and tests."""
    lines = [f"MISSION {program.name}"]
    _render_block(program.body, lines, 1)
    lines.append("END_MISSION")
    return "\n".join(lines)


def _render_block(block: IRBlock, lines: list[str], indent: int) -> None:
    for instruction in block.instructions:
        prefix = "  " * indent
        if isinstance(instruction, IRPower):
            lines.append(f"{prefix}POWER {_render_expression(instruction.value)}")
        elif isinstance(instruction, IRMove):
            lines.append(f"{prefix}MOVE {_render_expression(instruction.distance)}")
        elif isinstance(instruction, IRCamera):
            lines.append(f"{prefix}CAMERA {'ON' if instruction.enabled else 'OFF'}")
        elif isinstance(instruction, IRCaptureImage):
            lines.append(f"{prefix}CAPTURE IMAGE")
        elif isinstance(instruction, IRTransmitImage):
            lines.append(f"{prefix}TRANSMIT IMAGE")
        elif isinstance(instruction, IRWait):
            lines.append(f"{prefix}WAIT {_render_expression(instruction.duration)}")
        elif isinstance(instruction, IRSafeMode):
            lines.append(f"{prefix}SAFE_MODE")
        elif isinstance(instruction, IRIf):
            lines.append(f"{prefix}IF {_render_expression(instruction.condition)}")
            _render_block(instruction.then_block, lines, indent + 1)
            if instruction.else_block is not None:
                lines.append(f"{prefix}ELSE")
                _render_block(instruction.else_block, lines, indent + 1)
            lines.append(f"{prefix}END_IF")
        elif isinstance(instruction, IRRepeat):
            lines.append(f"{prefix}REPEAT {_render_expression(instruction.count)}")
            _render_block(instruction.body, lines, indent + 1)
            lines.append(f"{prefix}END_REPEAT")
        else:
            raise TypeError(f"Unsupported IR instruction: {type(instruction).__name__}")


def _render_expression(expression: IRExpression) -> str:
    if isinstance(expression, IRLiteral):
        if isinstance(expression.value, bool):
            return "TRUE" if expression.value else "FALSE"
        if isinstance(expression.value, str):
            return repr(expression.value)
        return str(expression.value)
    if isinstance(expression, IRIdentifier):
        return expression.name
    if isinstance(expression, IRUnary):
        return f"({expression.operator}{_render_expression(expression.operand)})"
    if isinstance(expression, IRBinary):
        return f"({_render_expression(expression.left)} {expression.operator} {_render_expression(expression.right)})"
    raise TypeError(f"Unsupported IR expression: {type(expression).__name__}")
