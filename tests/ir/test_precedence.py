from aegis.ir import IRBinary, IRGenerator
from aegis.lexer import Lexer
from aegis.parser import Parser
from aegis.semantic import SemanticAnalyzer


def test_operator_precedence_survives_ast_to_ir_mapping() -> None:
    source = "MISSION math { POWER 1 + 2 * 3; }"
    program = Parser(Lexer(source).tokenize()).parse()
    assert program is not None
    assert SemanticAnalyzer().analyze(program) == []

    expression = IRGenerator().generate(program).body.instructions[0].value

    assert isinstance(expression, IRBinary)
    assert expression.operator == "+"
    assert isinstance(expression.right, IRBinary)
    assert expression.right.operator == "*"
