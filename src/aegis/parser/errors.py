"""Parser diagnostics for AEGIS source tokens."""

from __future__ import annotations

from dataclasses import dataclass

from aegis.lexer import Token


@dataclass(frozen=True, slots=True)
class ParserError:
    message: str
    line: int
    column: int
    unexpected: str = ""
    expected: str | None = None

    def __str__(self) -> str:
        detail = f"Syntax error at line {self.line}, column {self.column}: {self.message}"
        if self.expected:
            detail += f" Expected {self.expected}."
        if self.unexpected:
            detail += f" Unexpected {self.unexpected!r}."
        return detail


class ParseFailure(Exception):
    """Internal control flow for recovering from one syntax error."""

    def __init__(self, error: ParserError) -> None:
        super().__init__(error.message)
        self.error = error


def error_for_token(message: str, token: Token, expected: str | None = None) -> ParserError:
    return ParserError(message, token.line, token.column, token.lexeme, expected)
