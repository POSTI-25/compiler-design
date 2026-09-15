from aegis.ast import SourceLocation
from aegis.ir import IRBinary, IRBlock, IRLiteral, IRProgram, IRRepeat, render_ir


def test_ir_nodes_are_typed_and_source_located() -> None:
    location = SourceLocation(2, 4)
    literal = IRLiteral(3, location=location)
    expression = IRBinary(literal, "+", literal, location=location)
    body = IRBlock((IRRepeat(literal, IRBlock((), location=location), location=location),), location=location)
    program = IRProgram("demo", body, location=location)

    assert expression.left.value == 3
    assert program.body.instructions[0].count.value == 3
    assert render_ir(program).splitlines() == ["MISSION demo", "  REPEAT 3", "  END_REPEAT", "END_MISSION"]
