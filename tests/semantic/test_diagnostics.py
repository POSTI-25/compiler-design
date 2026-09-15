from aegis.semantic import SemanticDiagnostic


def test_semantic_diagnostic_has_stable_format() -> None:
    diagnostic = SemanticDiagnostic("SEM002", "Undefined identifier", 3, 7, "BATTERY_LEVEL")

    assert diagnostic.category == "semantic"
    assert str(diagnostic) == (
        "[SEMANTIC SEM002] at line 3, column 7: Undefined identifier. "
        "Symbol: BATTERY_LEVEL."
    )
