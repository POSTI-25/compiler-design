"""Minimal interpreter for the existing structured AEGIS IR."""

from __future__ import annotations

from aegis.ir import (
    IRBinary,
    IRBlock,
    IRCamera,
    IRCaptureImage,
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
from aegis.ir.nodes import IRExpression

from .errors import RuntimeError
from .state import RuntimeState


class Interpreter:
    """Execute supported structured IR instructions against simulated state."""

    def __init__(self, state: RuntimeState | None = None) -> None:
        self.state = state or RuntimeState()

    def run(self, program: IRProgram) -> RuntimeState:
        self._trace(f"MISSION {program.name}")
        self._execute_block(program.body)
        self._trace("END_MISSION")
        return self.state

    def _execute_block(self, block: IRBlock) -> None:
        for instruction in block.instructions:
            if isinstance(instruction, IRPower):
                self._execute_power(instruction)
            elif isinstance(instruction, IRMove):
                self._execute_move(instruction)
            elif isinstance(instruction, IRCamera):
                self._execute_camera(instruction)
            elif isinstance(instruction, IRCaptureImage):
                self._execute_capture(instruction)
            elif isinstance(instruction, IRTransmitImage):
                self._execute_transmit(instruction)
            elif isinstance(instruction, IRWait):
                self._execute_wait(instruction)
            elif isinstance(instruction, IRSafeMode):
                self._execute_safe_mode(instruction)
            elif isinstance(instruction, IRIf):
                self._execute_if(instruction)
            elif isinstance(instruction, IRRepeat):
                self._execute_repeat(instruction)
            else:
                raise RuntimeError(f"Unsupported runtime instruction: {type(instruction).__name__}")

    def _execute_power(self, instruction: IRPower) -> None:
        value = self._number(self._evaluate(instruction.value), "POWER value")
        if not 0 <= value <= 100:
            raise RuntimeError("POWER value must be between 0 and 100")
        self.state.battery = value
        self._trace(f"POWER {value}")

    def _execute_move(self, instruction: IRMove) -> None:
        distance = self._number(self._evaluate(instruction.distance), "MOVE distance")
        if distance < 0:
            raise RuntimeError("MOVE distance must be nonnegative")
        if self.state.safe_mode:
            raise RuntimeError("MOVE is unavailable in safe mode")
        if distance > self.state.battery:
            raise RuntimeError("Insufficient battery for MOVE")
        self.state.position += distance
        self.state.battery -= distance
        self._trace(f"MOVE {distance}")

    def _execute_camera(self, instruction: IRCamera) -> None:
        if self.state.safe_mode and instruction.enabled:
            raise RuntimeError("CAMERA ON is unavailable in safe mode")
        self.state.camera_on = instruction.enabled
        self._trace(f"CAMERA {'ON' if instruction.enabled else 'OFF'}")

    def _execute_capture(self, instruction: IRCaptureImage) -> None:
        if self.state.safe_mode:
            raise RuntimeError("CAPTURE IMAGE is unavailable in safe mode")
        if not self.state.camera_on:
            raise RuntimeError("Cannot capture IMAGE while the camera is off")
        self.state.image_captured = True
        self._trace("CAPTURE IMAGE")

    def _execute_transmit(self, instruction: IRTransmitImage) -> None:
        if not self.state.image_captured:
            raise RuntimeError("Cannot transmit IMAGE because no image has been captured")
        self.state.image_captured = False
        self._trace("TRANSMIT IMAGE")

    def _execute_wait(self, instruction: IRWait) -> None:
        duration = self._number(self._evaluate(instruction.duration), "WAIT duration")
        if duration < 0:
            raise RuntimeError("WAIT duration must be nonnegative")
        self.state.elapsed_time += duration
        self._trace(f"WAIT {duration}")

    def _execute_safe_mode(self, instruction: IRSafeMode) -> None:
        self.state.safe_mode = True
        self._trace("SAFE_MODE")

    def _execute_if(self, instruction: IRIf) -> None:
        condition = self._evaluate(instruction.condition)
        if not isinstance(condition, bool):
            raise RuntimeError("IF condition must evaluate to boolean")
        self._trace(f"IF {'TRUE' if condition else 'FALSE'}")
        if condition:
            self._execute_block(instruction.then_block)
        elif instruction.else_block is not None:
            self._execute_block(instruction.else_block)

    def _execute_repeat(self, instruction: IRRepeat) -> None:
        count = self._evaluate(instruction.count)
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise RuntimeError("REPEAT count must be a nonnegative integer")
        self._trace(f"REPEAT {count}")
        for _ in range(count):
            self._execute_block(instruction.body)

    def _evaluate(self, expression: IRExpression):
        if isinstance(expression, IRLiteral):
            return expression.value
        if isinstance(expression, IRIdentifier):
            values = {
                "BATTERY": self.state.battery,
                "POSITION": self.state.position,
                "TIME": self.state.elapsed_time,
                "CAMERA": self.state.camera_on,
                "IMAGE": self.state.image_captured,
                "SAFE_MODE": self.state.safe_mode,
            }
            if expression.name not in values:
                raise RuntimeError(f"Undefined runtime identifier: {expression.name}")
            return values[expression.name]
        if isinstance(expression, IRUnary):
            operand = self._evaluate(expression.operand)
            if expression.operator == "+":
                return self._number(operand, "unary operand")
            if expression.operator == "-":
                return -self._number(operand, "unary operand")
            raise RuntimeError(f"Unsupported unary operator: {expression.operator}")
        if isinstance(expression, IRBinary):
            left = self._evaluate(expression.left)
            right = self._evaluate(expression.right)
            return self._evaluate_binary(expression.operator, left, right)
        raise RuntimeError(f"Unsupported runtime expression: {type(expression).__name__}")

    def _evaluate_binary(self, operator: str, left, right):
        if operator == "+":
            return self._number(left, "left operand") + self._number(right, "right operand")
        if operator == "-":
            return self._number(left, "left operand") - self._number(right, "right operand")
        if operator == "*":
            return self._number(left, "left operand") * self._number(right, "right operand")
        if operator == "/":
            denominator = self._number(right, "right operand")
            if denominator == 0:
                raise RuntimeError("Division by zero")
            return self._number(left, "left operand") / denominator
        if operator in {"<", "<=", ">", ">="}:
            left_number = self._number(left, "left operand")
            right_number = self._number(right, "right operand")
            return {"<": left_number < right_number, "<=": left_number <= right_number, ">": left_number > right_number, ">=": left_number >= right_number}[operator]
        if operator == "!=":
            return left != right
        raise RuntimeError(f"Unsupported binary operator: {operator}")

    @staticmethod
    def _number(value, description: str) -> int | float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise RuntimeError(f"{description} must be numeric")
        return value

    def _trace(self, message: str) -> None:
        self.state.trace.append(message)
