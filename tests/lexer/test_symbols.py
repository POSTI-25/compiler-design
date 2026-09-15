from aegis.lexer import Lexer, TokenType


def test_punctuation_and_operators_are_tokenized() -> None:
    tokens = Lexer("{}();,+-*/ < > == != <= >=").tokenize()

    assert [token.type for token in tokens[:-1]] == [
        TokenType.LEFT_BRACE,
        TokenType.RIGHT_BRACE,
        TokenType.LEFT_PAREN,
        TokenType.RIGHT_PAREN,
        TokenType.SEMICOLON,
        TokenType.COMMA,
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.STAR,
        TokenType.SLASH,
        TokenType.LESS,
        TokenType.GREATER,
        TokenType.EQUAL_EQUAL,
        TokenType.NOT_EQUAL,
        TokenType.LESS_EQUAL,
        TokenType.GREATER_EQUAL,
    ]
