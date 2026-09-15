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
    IRGenerator,
    render_ir,
)
from aegis.lexer import Lexer
from aegis.parser import Parser
from aegis.semantic import SemanticAnalyzer


def compile_ir(source: str):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    assert lexer.errors == []
    assert parser.errors == []
    assert program is not None
    semantic_diagnostics = SemanticAnalyzer().analyze(program)
    assert semantic_diagnostics == []
    return IRGenerator().generate(program)


def test_minimal_mission_generates_program_and_empty_block() -> None:
    ir = compile_ir("MISSION empty {}")

    assert isinstance(ir, IRProgram)
    assert ir.name == "empty"
    assert isinstance(ir.body, IRBlock)
    assert ir.body.instructions == ()


def test_all_basic_commands_map_to_structured_instructions() -> None:
    ir = compile_ir(
        "MISSION observation { POWER 80; MOVE 10; CAMERA ON; CAPTURE IMAGE; "
        "CAMERA OFF; TRANSMIT IMAGE; WAIT 5; SAFE_MODE; }"
    )

    assert [type(item) for item in ir.body.instructions] == [
        IRPower,
        IRMove,
        IRCamera,
        IRCaptureImage,
        IRCamera,
        IRTransmitImage,
        IRWait,
        IRSafeMode,
    ]


def test_expressions_preserve_literals_identifiers_unary_and_binary_structure() -> None:
    ir = compile_ir(
        "MISSION expressions { POWER (BATTERY + 5) * -2; IF VISIBILITY == TRUE { WAIT 1; } }"
    )

    power = ir.body.instructions[0]
    assert isinstance(power.value, IRBinary)
    assert isinstance(power.value.left, IRBinary)
    assert isinstance(power.value.left.left, IRIdentifier)
    assert isinstance(power.value.right, IRUnary)
    assert power.value.operator == "*"


def test_control_flow_is_nested_structured_ir() -> None:
    ir = compile_ir(
        "MISSION control { IF BATTERY < 30 { SAFE_MODE; } ELSE { WAIT 1; } "
        "REPEAT 2 { MOVE 3; IF TRUE { WAIT 1; } } }"
    )

    conditional, repetition = ir.body.instructions
    assert isinstance(conditional, IRIf)
    assert conditional.else_block is not None
    assert isinstance(repetition, IRRepeat)
    assert isinstance(repetition.body.instructions[1], IRIf)


def test_ir_preserves_source_locations() -> None:
    ir = compile_ir("MISSION test { POWER 80; }")

    assert (ir.location.line, ir.location.column) == (1, 1)
    assert (ir.body.location.line, ir.body.location.column) == (1, 14)
    assert (ir.body.instructions[0].location.line, ir.body.instructions[0].location.column) == (1, 16)
    assert (ir.body.instructions[0].value.location.line, ir.body.instructions[0].value.location.column) == (1, 22)


def test_ir_rendering_is_deterministic_and_readable() -> None:
    ir = compile_ir("MISSION test { POWER 40 + 40; IF TRUE { WAIT 1; } ELSE { SAFE_MODE; } }")
    expected = "\n".join(
        [
            "MISSION test",
            "  POWER (40 + 40)",
            "  IF TRUE",
            "    WAIT 1",
            "  ELSE",
            "    SAFE_MODE",
            "  END_IF",
            "END_MISSION",
        ]
    )

    assert render_ir(ir) == expected
    assert render_ir(ir) == render_ir(ir)
