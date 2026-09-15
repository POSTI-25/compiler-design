from aegis.lexer import Lexer
from aegis.parser import Parser
from aegis.semantic import SemanticAnalyzer


def test_analyzer_api_accepts_parsed_ast() -> None:
    source = "MISSION minimal {}"
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()

    analyzer = SemanticAnalyzer()
    diagnostics = analyzer.analyze(program)

    assert diagnostics == []
    assert analyzer.symbol_table.lookup("minimal").kind.name == "MISSION"
