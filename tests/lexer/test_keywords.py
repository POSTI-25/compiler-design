from aegis.lexer import Lexer, TokenType


def test_all_supported_keywords_are_recognized() -> None:
    source = "MISSION POWER MOVE CAMERA ON OFF CAPTURE IMAGE TRANSMIT WAIT SAFE_MODE IF ELSE REPEAT END TRUE FALSE"

    tokens = Lexer(source).tokenize()

    assert [token.type for token in tokens[:-1]] == [
        TokenType.MISSION,
        TokenType.POWER,
        TokenType.MOVE,
        TokenType.CAMERA,
        TokenType.ON,
        TokenType.OFF,
        TokenType.CAPTURE,
        TokenType.IMAGE,
        TokenType.TRANSMIT,
        TokenType.WAIT,
        TokenType.SAFE_MODE,
        TokenType.IF,
        TokenType.ELSE,
        TokenType.REPEAT,
        TokenType.END,
        TokenType.TRUE,
        TokenType.FALSE,
    ]


def test_keyword_matching_is_case_sensitive() -> None:
    tokens = Lexer("mission Power observation").tokenize()

    assert [token.type for token in tokens[:-1]] == [TokenType.IDENTIFIER] * 3
