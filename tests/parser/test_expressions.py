from aegis.ast import BinaryExpression, BooleanLiteral, StringLiteral, UnaryExpression
from aegis.lexer import Lexer
from aegis.parser import Parser


def test_string_boolean_and_unary_expressions_parse() -> None:
    parser = Parser(Lexer('MISSION values { IF TRUE == FALSE { WAIT "five"; } POWER -10; }').tokenize())
    program = parser.parse()

    assert parser.errors == []
    condition = program.body.statements[0].condition
    assert isinstance(condition, BinaryExpression)
    assert isinstance(condition.left, BooleanLiteral)
    assert isinstance(program.body.statements[0].then_branch.statements[0].duration, StringLiteral)
    assert isinstance(program.body.statements[1].value, UnaryExpression)
