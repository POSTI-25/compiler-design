"""Minimal runtime interpreter for structured AEGIS IR."""

from .errors import RuntimeError
from .interpreter import Interpreter
from .state import RuntimeState

__all__ = ["Interpreter", "RuntimeError", "RuntimeState"]
