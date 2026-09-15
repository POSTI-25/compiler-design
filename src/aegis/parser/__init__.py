"""Public parser API for AEGIS source tokens."""

from .errors import ParserError
from .parser import Parser

__all__ = ["Parser", "ParserError"]
