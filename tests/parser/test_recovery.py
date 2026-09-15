from aegis.ast import MoveCommand, WaitCommand
from aegis.lexer import Lexer
from aegis.parser import Parser


def test_parser_recovers_at_statement_boundaries() -> None:
    parser = Parser(Lexer("MISSION test { POWER 80 MOVE 10; CAMERA; WAIT 5; }").tokenize())
    program = parser.parse()

    assert len(parser.errors) == 2
    assert [type(statement) for statement in program.body.statements] == [MoveCommand, WaitCommand]


def test_parser_reports_multiple_errors_without_looping() -> None:
    parser = Parser(Lexer("MISSION test { POWER; MOVE; }").tokenize())

    program = parser.parse()

    assert program is not None
    assert len(parser.errors) == 2
