"""Token definitions for the AEGIS lexer."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    MISSION = auto()
    POWER = auto()
    MOVE = auto()
    CAMERA = auto()
    ON = auto()
    OFF = auto()
    CAPTURE = auto()
    IMAGE = auto()
    TRANSMIT = auto()
    WAIT = auto()
    SAFE_MODE = auto()
    IF = auto()
    ELSE = auto()
    REPEAT = auto()
    END = auto()
    TRUE = auto()
    FALSE = auto()

    IDENTIFIER = auto()
    INTEGER = auto()
    DECIMAL = auto()
    STRING = auto()

    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    SEMICOLON = auto()
    COMMA = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LESS = auto()
    GREATER = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    EOF = auto()


@dataclass(frozen=True, slots=True)
class Token:
    """A lexical token with its original text and source position."""

    type: TokenType
    lexeme: str
    line: int
    column: int
    value: Any = None

    def __str__(self) -> str:
        return f"{self.type.name} {self.lexeme!r} at line {self.line}, column {self.column}"
