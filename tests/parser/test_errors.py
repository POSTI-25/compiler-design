from aegis.lexer import Lexer
from aegis.parser import Parser


def parse_with_errors(source: str) -> Parser:
    parser = Parser(Lexer(source).tokenize())
    parser.parse()
    return parser


def test_missing_mission_and_braces_report_errors_without_crashing() -> None:
    parser = parse_with_errors("POWER 80;")

    assert parser.errors
    assert "MISSION" in str(parser.errors[0])

    parser = parse_with_errors("MISSION test { POWER 80;")
    assert any("'}'" in str(error) for error in parser.errors)


def test_missing_semicolon_reports_location() -> None:
    parser = parse_with_errors("MISSION test { POWER 80 } ")

    assert len(parser.errors) == 1
    assert parser.errors[0].line == 1
    assert parser.errors[0].column > 0
    assert "';'" in str(parser.errors[0])


def test_end_is_rejected_in_brace_based_grammar() -> None:
    parser = parse_with_errors("MISSION test { END }")

    assert parser.errors
    assert "Expected a statement" in str(parser.errors[0])
