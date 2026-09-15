from aegis.lexer import Lexer, TokenType


def test_observation_mission_tokenizes_in_order() -> None:
    source = "MISSION observation {\n    POWER 80;\n    CAMERA ON;\n}"

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert [token.type for token in tokens] == [
        TokenType.MISSION,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACE,
        TokenType.POWER,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.CAMERA,
        TokenType.ON,
        TokenType.SEMICOLON,
        TokenType.RIGHT_BRACE,
        TokenType.EOF,
    ]
    assert lexer.errors == []


def test_token_positions_are_one_based() -> None:
    tokens = Lexer("MISSION test {\n  POWER 80;\n}").tokenize()

    assert (tokens[0].line, tokens[0].column) == (1, 1)
    assert (tokens[1].line, tokens[1].column) == (1, 9)
    assert (tokens[3].line, tokens[3].column) == (2, 3)
    assert (tokens[-1].type, tokens[-1].line, tokens[-1].column) == (TokenType.EOF, 3, 2)
