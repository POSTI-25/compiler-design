from aegis.lexer import Lexer, TokenType


def test_integer_decimal_and_string_literals_preserve_values() -> None:
    tokens = Lexer('80 12.5 "image\\nname"').tokenize()

    assert [(token.type, token.value) for token in tokens[:-1]] == [
        (TokenType.INTEGER, 80),
        (TokenType.DECIMAL, 12.5),
        (TokenType.STRING, "image\nname"),
    ]


def test_invalid_number_is_reported_and_lexing_continues() -> None:
    lexer = Lexer("12.5.6 POWER")
    tokens = lexer.tokenize()

    assert [token.type for token in tokens] == [TokenType.POWER, TokenType.EOF]
    assert len(lexer.errors) == 1
    assert "Invalid numeric literal" in str(lexer.errors[0])
