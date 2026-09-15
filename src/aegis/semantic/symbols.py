"""Scoped symbols and symbol tables for the current AEGIS language."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from aegis.ast import SourceLocation


class SymbolKind(Enum):
    MISSION = auto()
    STATE = auto()
    VARIABLE = auto()


@dataclass(frozen=True, slots=True)
class Symbol:
    name: str
    kind: SymbolKind
    type_name: str
    location: SourceLocation
    mutable: bool = False


class Scope:
    """One lexical scope with an optional parent scope."""

    def __init__(self, parent: Scope | None = None) -> None:
        self.parent = parent
        self.symbols: dict[str, Symbol] = {}

    def define(self, symbol: Symbol) -> bool:
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True

    def lookup_current(self, name: str) -> Symbol | None:
        return self.symbols.get(name)

    def lookup(self, name: str) -> Symbol | None:
        symbol = self.lookup_current(name)
        if symbol is not None or self.parent is None:
            return symbol
        return self.parent.lookup(name)


class SymbolTable:
    """Manage nested scopes and expose lookup operations for semantic analysis."""

    def __init__(self) -> None:
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def enter_scope(self) -> Scope:
        self.current_scope = Scope(self.current_scope)
        return self.current_scope

    def exit_scope(self) -> Scope:
        if self.current_scope.parent is None:
            raise RuntimeError("Cannot exit the global symbol scope")
        exited = self.current_scope
        self.current_scope = exited.parent
        return exited

    def define(self, symbol: Symbol) -> bool:
        return self.current_scope.define(symbol)

    def lookup_current(self, name: str) -> Symbol | None:
        return self.current_scope.lookup_current(name)

    def lookup(self, name: str) -> Symbol | None:
        return self.current_scope.lookup(name)
