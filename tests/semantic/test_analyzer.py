from aegis.lexer import Lexer
from aegis.parser import Parser
from aegis.semantic import SemanticAnalyzer


def analyze(source: str):
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize())
    program = parser.parse()
    assert lexer.errors == []
    assert parser.errors == []
    assert program is not None
    return SemanticAnalyzer().analyze(program)


def codes(source: str) -> list[str]:
    return [diagnostic.code for diagnostic in analyze(source)]


def test_valid_mission_passes_semantic_analysis() -> None:
    source = """MISSION observation {
        POWER 80;
        CAMERA ON;
        CAPTURE IMAGE;
        CAMERA OFF;
        TRANSMIT IMAGE;
        IF BATTERY < 30 { SAFE_MODE; }
        REPEAT 3 { WAIT 1; }
    }"""

    assert analyze(source) == []


def test_predefined_state_identifiers_are_available() -> None:
    assert analyze("MISSION state { IF VISIBILITY == TRUE { WAIT 1; } }") == []


def test_undefined_identifier_is_reported_with_location() -> None:
    diagnostics = analyze("MISSION broken { IF UNKNOWN < 30 { WAIT 1; } }")

    assert [item.code for item in diagnostics] == ["SEM002"]
    assert diagnostics[0].symbol == "UNKNOWN"
    assert (diagnostics[0].line, diagnostics[0].column) == (1, 21)


def test_command_ranges_and_types_are_checked() -> None:
    diagnostics = analyze("MISSION broken { POWER 140; MOVE -2; WAIT TRUE; }")

    assert [item.code for item in diagnostics] == ["SEM006", "SEM007", "SEM003"]


def test_conditions_and_repeat_counts_are_checked() -> None:
    diagnostics = analyze("MISSION broken { IF 10 { WAIT 1; } REPEAT 1.5 { WAIT 1; } }")

    assert [item.code for item in diagnostics] == ["SEM004", "SEM005"]


def test_expression_operand_types_are_checked() -> None:
    diagnostics = analyze('MISSION broken { POWER "high" + 1; IF TRUE + FALSE { WAIT 1; } }')

    assert [item.code for item in diagnostics] == ["SEM003", "SEM003"]


def test_camera_and_image_dependencies_are_checked() -> None:
    diagnostics = analyze("MISSION broken { CAPTURE IMAGE; TRANSMIT IMAGE; }")

    assert [item.code for item in diagnostics] == ["SEM008", "SEM009"]


def test_multiple_semantic_errors_are_collected() -> None:
    diagnostics = analyze("MISSION broken { POWER 140; IF UNKNOWN { MOVE \"ten\"; } }")

    assert [item.code for item in diagnostics] == ["SEM006", "SEM002", "SEM003"]
