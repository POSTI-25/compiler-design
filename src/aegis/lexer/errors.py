"""Lexical diagnostics for AEGIS source text."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LexicalError:
    """A recoverable lexical error with its source location."""

    message: str
    line: int
    column: int
    lexeme: str = ""

    def __str__(self) -> str:
        return f"Lexical error at line {self.line}, column {self.column}: {self.message}"
