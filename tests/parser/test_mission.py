from aegis.ast import CameraCommand, Mission, PowerCommand
from aegis.lexer import Lexer
from aegis.parser import Parser


def parse(source: str) -> Parser:
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize())
    parser.program = parser.parse()
    assert lexer.errors == []
    return parser


def test_empty_mission_is_valid() -> None:
    parser = parse("MISSION empty {}")

    assert isinstance(parser.program, Mission)
    assert parser.program.name == "empty"
    assert parser.program.body.statements == ()
    assert parser.errors == []


def test_mission_name_and_commands_are_preserved() -> None:
    parser = parse("MISSION observation { POWER 80; CAMERA ON; }")

    assert parser.errors == []
    assert parser.program.name == "observation"
    assert isinstance(parser.program.body.statements[0], PowerCommand)
    assert parser.program.body.statements[0].value.value == 80
    assert isinstance(parser.program.body.statements[1], CameraCommand)
    assert parser.program.body.statements[1].enabled is True
