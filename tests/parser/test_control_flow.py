from aegis.ast import IfStatement, RepeatStatement
from aegis.lexer import Lexer
from aegis.parser import Parser


def test_if_else_and_repeat_build_nested_blocks() -> None:
    source = """MISSION monitoring {
        IF BATTERY < 30 {
            SAFE_MODE;
        } ELSE {
            WAIT 5;
        }
        REPEAT 3 {
            MOVE 10;
        }
    }"""
    parser = Parser(Lexer(source).tokenize())
    program = parser.parse()

    assert parser.errors == []
    conditional, repetition = program.body.statements
    assert isinstance(conditional, IfStatement)
    assert conditional.condition.left.name == "BATTERY"
    assert len(conditional.then_branch.statements) == 1
    assert len(conditional.else_branch.statements) == 1
    assert isinstance(repetition, RepeatStatement)
    assert repetition.count.value == 3


def test_parentheses_and_operator_precedence_are_preserved() -> None:
    parser = Parser(Lexer("MISSION math { POWER (40 + 40) * 2; }").tokenize())
    program = parser.parse()

    assert parser.errors == []
    expression = program.body.statements[0].value
    assert expression.operator == "*"
    assert expression.left.operator == "+"
