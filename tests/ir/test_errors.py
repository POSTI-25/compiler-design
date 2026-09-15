import pytest

from aegis.ir import IRGenerationError, IRGenerator
from aegis.lexer import Lexer
from aegis.parser import Parser
from aegis.semantic import SemanticAnalyzer


def test_ir_generation_is_blocked_by_lexer_errors() -> None:
    lexer = Lexer("MISSION broken { POWER @ 80; }")
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    assert lexer.errors
    with pytest.raises(IRGenerationError):
        IRGenerator().generate(program, lexer.errors)


def test_ir_generation_is_blocked_by_parser_errors() -> None:
    parser = Parser(Lexer("MISSION broken { POWER 80 }").tokenize())
    program = parser.parse()

    assert parser.errors
    with pytest.raises(IRGenerationError):
        IRGenerator().generate(program, parser.errors)


def test_ir_generation_is_blocked_by_semantic_errors() -> None:
    source = "MISSION broken { POWER 140; }"
    parser = Parser(Lexer(source).tokenize())
    program = parser.parse()
    diagnostics = SemanticAnalyzer().analyze(program)

    assert diagnostics
    with pytest.raises(IRGenerationError):
        IRGenerator().generate(program, diagnostics)


def test_ir_generation_rejects_missing_program() -> None:
    with pytest.raises(IRGenerationError):
        IRGenerator().generate(None)
