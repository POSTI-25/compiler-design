"""Semantic diagnostics for AEGIS programs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SemanticDiagnostic:
    code: str
    message: str
    line: int
    column: int
    symbol: str | None = None

    @property
    def category(self) -> str:
        return "semantic"

    def __str__(self) -> str:
        message = self.message if self.message.endswith(".") else f"{self.message}."
        detail = f"[SEMANTIC {self.code}] at line {self.line}, column {self.column}: {message}"
        if self.symbol:
            detail += f" Symbol: {self.symbol}."
        return detail
