from aegis.lexer import Lexer, TokenType


def test_whitespace_and_line_comments_are_ignored() -> None:
    source = "POWER 80; // configure power\n\tMOVE 10;\n// complete"

    tokens = Lexer(source).tokenize()

    assert [token.type for token in tokens] == [
        TokenType.POWER,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.MOVE,
        TokenType.INTEGER,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]
    assert tokens[3].line == 2
    assert tokens[3].column == 2
