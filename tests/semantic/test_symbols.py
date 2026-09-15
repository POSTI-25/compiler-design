from aegis.ast import SourceLocation
from aegis.semantic import Symbol, SymbolKind, SymbolTable


def symbol(name: str, kind: SymbolKind = SymbolKind.VARIABLE) -> Symbol:
    return Symbol(name, kind, "number", SourceLocation(2, 3))


def test_symbol_table_inserts_and_looks_up_symbols() -> None:
    table = SymbolTable()
    mission = symbol("observation", SymbolKind.MISSION)

    assert table.define(mission) is True
    assert table.lookup("observation") == mission
    assert table.lookup_current("observation") == mission
    assert table.lookup_current("missing") is None


def test_nested_scopes_look_up_parent_symbols_and_allow_shadowing() -> None:
    table = SymbolTable()
    outer = symbol("limit")
    inner = symbol("limit")
    table.define(outer)

    table.enter_scope()
    assert table.lookup("limit") == outer
    assert table.define(inner) is True
    assert table.lookup_current("limit") == inner
    assert table.lookup("limit") == inner

    table.exit_scope()
    assert table.lookup("limit") == outer


def test_duplicate_symbol_is_rejected_in_current_scope() -> None:
    table = SymbolTable()

    assert table.define(symbol("limit")) is True
    assert table.define(symbol("limit")) is False
