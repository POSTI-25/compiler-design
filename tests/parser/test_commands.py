from aegis.ast import (
    CameraCommand,
    CaptureImageCommand,
    MoveCommand,
    PowerCommand,
    SafeModeCommand,
    TransmitImageCommand,
    WaitCommand,
)
from aegis.lexer import Lexer
from aegis.parser import Parser


def parse_one(statement: str):
    parser = Parser(Lexer(f"MISSION test {{ {statement} }}").tokenize())
    program = parser.parse()
    assert parser.errors == []
    return program.body.statements[0]


def test_all_basic_commands_parse() -> None:
    statements = Parser(
        Lexer("MISSION test { POWER 80; MOVE 10.5; CAMERA OFF; CAPTURE IMAGE; TRANSMIT IMAGE; WAIT 5; SAFE_MODE; }").tokenize()
    )
    program = statements.parse()

    assert statements.errors == []
    assert [type(item) for item in program.body.statements] == [
        PowerCommand,
        MoveCommand,
        CameraCommand,
        CaptureImageCommand,
        TransmitImageCommand,
        WaitCommand,
        SafeModeCommand,
    ]
    assert program.body.statements[1].distance.value == 10.5
    assert program.body.statements[2].enabled is False


def test_camera_requires_on_or_off() -> None:
    parser = Parser(Lexer("MISSION test { CAMERA; }").tokenize())

    parser.parse()

    assert len(parser.errors) == 1
    assert "ON" in str(parser.errors[0])
