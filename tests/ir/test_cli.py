from pathlib import Path

from aegis.cli import main


PROJECT_ROOT = Path(__file__).parents[2]


def test_ir_cli_prints_deterministic_ir_for_valid_source(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "valid" / "observation.aegis"

    assert main(["ir", str(source)]) == 0
    first = capsys.readouterr()

    assert main(["ir", str(source)]) == 0
    second = capsys.readouterr()
    assert first.out == second.out
    assert "MISSION observation" in first.out
    assert "END_MISSION" in first.out
    assert first.err == ""


def test_ir_cli_rejects_invalid_source(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "invalid" / "semantic_errors.aegis"

    assert main(["ir", str(source)]) == 1

    output = capsys.readouterr()
    assert "SEM006" in output.err
    assert output.out == ""
