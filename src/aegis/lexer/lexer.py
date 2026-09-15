"""Handwritten lexer for the initial AEGIS language subset."""

from __future__ import annotations

from .errors import LexicalError
from .tokens import Token, TokenType


_KEYWORDS = {
    "MISSION": TokenType.MISSION,
    "POWER": TokenType.POWER,
    "MOVE": TokenType.MOVE,
    "CAMERA": TokenType.CAMERA,
    "ON": TokenType.ON,
    "OFF": TokenType.OFF,
    "CAPTURE": TokenType.CAPTURE,
    "IMAGE": TokenType.IMAGE,
    "TRANSMIT": TokenType.TRANSMIT,
    "WAIT": TokenType.WAIT,
    "SAFE_MODE": TokenType.SAFE_MODE,
    "IF": TokenType.IF,
    "ELSE": TokenType.ELSE,
    "REPEAT": TokenType.REPEAT,
    "END": TokenType.END,
    "TRUE": TokenType.TRUE,
    "FALSE": TokenType.FALSE,
}

_SINGLE_CHARACTER_TOKENS = {
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    ";": TokenType.SEMICOLON,
    ",": TokenType.COMMA,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
}


class Lexer:
    """Tokenize AEGIS source while collecting recoverable lexical errors."""

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []
        self.errors: list[LexicalError] = []
        self._current = 0
        self._line = 1
        self._column = 1
        self._token_line = 1
        self._token_column = 1

    def tokenize(self) -> list[Token]:
        """Return tokens, including exactly one EOF token."""
        while not self._at_end():
            self._start = self._current
            self._token_line = self._line
            self._token_column = self._column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self._line, self._column))
        return self.tokens

    def _scan_token(self) -> None:
        character = self._advance()

        if character in " \t\r\n":
            return

        if character == "/" and self._peek() == "/":
            self._skip_comment()
            return

        if character.isalpha() or character == "_":
            self._scan_identifier()
            return

        if character.isdigit():
            self._scan_number()
            return

        if character == '"':
            self._scan_string()
            return

        token_type = _SINGLE_CHARACTER_TOKENS.get(character)
        if token_type is not None:
            self._add_token(token_type, character)
            return

        if character in "<>!=":
            self._scan_comparison(character)
            return

        self._error(f"Unexpected character {character!r}", character)

    def _scan_identifier(self) -> None:
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        lexeme = self.source[self._start : self._current]
        token_type = _KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
        value = lexeme if token_type is TokenType.IDENTIFIER else None
        self._add_token(token_type, lexeme, value)

    def _scan_number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        is_decimal = False
        if self._peek() == ".":
            is_decimal = True
            self._advance()
            if not self._peek().isdigit():
                self._consume_invalid_number_tail()
                lexeme = self.source[self._start : self._current]
                self._error("Invalid numeric literal", lexeme)
                return
            while self._peek().isdigit():
                self._advance()

        if self._peek().isalpha() or self._peek() == "_" or self._peek() == ".":
            self._consume_invalid_number_tail()
            lexeme = self.source[self._start : self._current]
            self._error("Invalid numeric literal", lexeme)
            return

        lexeme = self.source[self._start : self._current]
        value = float(lexeme) if is_decimal else int(lexeme)
        token_type = TokenType.DECIMAL if is_decimal else TokenType.INTEGER
        self._add_token(token_type, lexeme, value)

    def _scan_string(self) -> None:
        value_characters: list[str] = []
        terminated = False
        while not self._at_end():
            character = self._advance()
            if character == '"':
                terminated = True
                break
            if character == "\\" and not self._at_end():
                escaped = self._advance()
                escape_values = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}
                value_characters.append(escape_values.get(escaped, escaped))
            else:
                value_characters.append(character)

        lexeme = self.source[self._start : self._current]
        if not terminated:
            self._error("Unterminated string literal", lexeme)
            return
        self._add_token(TokenType.STRING, lexeme, "".join(value_characters))

    def _scan_comparison(self, character: str) -> None:
        next_character = self._peek()
        if next_character == "=":
            self._advance()
            token_types = {"=": TokenType.EQUAL_EQUAL, "!": TokenType.NOT_EQUAL, "<": TokenType.LESS_EQUAL, ">": TokenType.GREATER_EQUAL}
            self._add_token(token_types[character], self.source[self._start : self._current])
            return
        if character == "<":
            self._add_token(TokenType.LESS, character)
        elif character == ">":
            self._add_token(TokenType.GREATER, character)
        else:
            self._error(f"Unexpected character {character!r}", character)

    def _skip_comment(self) -> None:
        self._advance()
        while self._peek() not in "\r\n" and not self._at_end():
            self._advance()

    def _consume_invalid_number_tail(self) -> None:
        while self._peek().isalnum() or self._peek() in "._":
            self._advance()

    def _add_token(self, token_type: TokenType, lexeme: str, value: object = None) -> None:
        self.tokens.append(Token(token_type, lexeme, self._token_line, self._token_column, value))

    def _error(self, message: str, lexeme: str) -> None:
        self.errors.append(LexicalError(message, self._token_line, self._token_column, lexeme))

    def _advance(self) -> str:
        character = self.source[self._current]
        self._current += 1
        if character == "\n":
            self._line += 1
            self._column = 1
        else:
            self._column += 1
        return character

    def _peek(self) -> str:
        if self._at_end():
            return "\0"
        return self.source[self._current]

    def _at_end(self) -> bool:
        return self._current >= len(self.source)
