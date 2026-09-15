from aegis.lexer import Lexer, TokenType


def test_unknown_character_is_reported_without_stopping_lexing() -> None:
    lexer = Lexer("POWER @ 80;")
    tokens = lexer.tokenize()

    assert [token.type for token in tokens] == [
        TokenType.POWER,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    assert len(lexer.errors) == 1
    assert lexer.errors[0].line == 1
    assert lexer.errors[0].column == 7
    assert "'@'" in str(lexer.errors[0])


def test_unterminated_string_is_reported() -> None:
    lexer = Lexer('"unfinished')
    tokens = lexer.tokenize()

    assert [token.type for token in tokens] == [TokenType.EOF]
    assert len(lexer.errors) == 1
    assert "Unterminated string literal" in str(lexer.errors[0])


def test_exactly_one_eof_token_is_emitted_after_multiple_errors() -> None:
    lexer = Lexer("@ # POWER")
    tokens = lexer.tokenize()

    assert tokens[-1].type is TokenType.EOF
    assert sum(token.type is TokenType.EOF for token in tokens) == 1
    assert len(lexer.errors) == 2
