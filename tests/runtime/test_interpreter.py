import pytest

from aegis.ast import SourceLocation
from aegis.ir import (
    IRBinary,
    IRBlock,
    IRCamera,
    IRCaptureImage,
    IRIf,
    IRIdentifier,
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
from aegis.runtime import Interpreter, RuntimeError, RuntimeState


LOCATION = SourceLocation(1, 1)


def literal(value):
    return IRLiteral(value, location=LOCATION)


def block(*instructions):
    return IRBlock(tuple(instructions), location=LOCATION)


def program(*instructions):
    return IRProgram("test", block(*instructions), location=LOCATION)


def test_runtime_state_has_deterministic_defaults() -> None:
    state = RuntimeState()

    assert state.battery == 100
    assert state.position == 0
    assert state.elapsed_time == 0
    assert state.camera_on is False
    assert state.image_captured is False
    assert state.safe_mode is False
    assert state.trace == []


def test_basic_commands_update_state_and_trace() -> None:
    state = Interpreter().run(
        program(
            IRPower(literal(80), location=LOCATION),
            IRCamera(True, location=LOCATION),
            IRCaptureImage(location=LOCATION),
            IRMove(literal(10), location=LOCATION),
            IRWait(literal(5), location=LOCATION),
            IRCamera(False, location=LOCATION),
            IRTransmitImage(location=LOCATION),
        )
    )

    assert state.battery == 70
    assert state.position == 10
    assert state.elapsed_time == 5
    assert state.camera_on is False
    assert state.image_captured is False
    assert state.trace == [
        "MISSION test",
        "POWER 80",
        "CAMERA ON",
        "CAPTURE IMAGE",
        "MOVE 10",
        "WAIT 5",
        "CAMERA OFF",
        "TRANSMIT IMAGE",
        "END_MISSION",
    ]


def test_expression_evaluation_supports_identifiers_unary_and_binary_operations() -> None:
    condition = IRBinary(
        IRIdentifier("BATTERY", location=LOCATION),
        ">",
        IRUnary("-", literal(-1), location=LOCATION),
        location=LOCATION,
    )
    state = Interpreter().run(
        program(
            IRPower(literal(20), location=LOCATION),
            IRIf(condition, block(IRWait(literal(2), location=LOCATION)), None, location=LOCATION),
        )
    )

    assert state.elapsed_time == 2


def test_if_and_repeat_execute_nested_blocks() -> None:
    state = Interpreter().run(
        program(
            IRIf(literal(False), block(IRMove(literal(20), location=LOCATION)), block(IRMove(literal(3), location=LOCATION)), location=LOCATION),
            IRRepeat(literal(2), block(IRWait(literal(4), location=LOCATION)), location=LOCATION),
        )
    )

    assert state.position == 3
    assert state.elapsed_time == 8
    assert "REPEAT 2" in state.trace


def test_safe_mode_rejects_camera_on_and_movement() -> None:
    with pytest.raises(RuntimeError, match="MOVE is unavailable in safe mode"):
        Interpreter().run(program(IRSafeMode(location=LOCATION), IRMove(literal(1), location=LOCATION)))

    with pytest.raises(RuntimeError, match="CAMERA ON is unavailable in safe mode"):
        Interpreter().run(program(IRSafeMode(location=LOCATION), IRCamera(True, location=LOCATION)))


def test_invalid_image_actions_raise_runtime_errors() -> None:
    with pytest.raises(RuntimeError, match="camera is off"):
        Interpreter().run(program(IRCaptureImage(location=LOCATION)))

    with pytest.raises(RuntimeError, match="no image has been captured"):
        Interpreter().run(program(IRTransmitImage(location=LOCATION)))


def test_invalid_expressions_and_repeat_counts_raise_runtime_errors() -> None:
    division = IRBinary(literal(1), "/", literal(0), location=LOCATION)
    with pytest.raises(RuntimeError, match="Division by zero"):
        Interpreter().run(program(IRWait(division, location=LOCATION)))

    with pytest.raises(RuntimeError, match="nonnegative integer"):
        Interpreter().run(program(IRRepeat(literal(-1), block(), location=LOCATION)))
