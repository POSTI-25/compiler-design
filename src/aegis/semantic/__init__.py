"""Symbol-table and semantic-analysis APIs for AEGIS."""

from .analyzer import SemanticAnalyzer
from .diagnostics import SemanticDiagnostic
from .symbols import Scope, Symbol, SymbolKind, SymbolTable

__all__ = [
    "Scope",
    "SemanticAnalyzer",
    "SemanticDiagnostic",
    "Symbol",
    "SymbolKind",
    "SymbolTable",
]
