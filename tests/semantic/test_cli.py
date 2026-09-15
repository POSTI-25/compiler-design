from pathlib import Path

from aegis.cli import main


PROJECT_ROOT = Path(__file__).parents[2]


def test_check_cli_accepts_valid_mission(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "valid" / "observation.aegis"

    assert main(["check", str(source)]) == 0

    output = capsys.readouterr()
    assert "Semantic check passed." in output.out
    assert output.err == ""


def test_check_cli_rejects_semantic_errors(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "invalid" / "semantic_errors.aegis"

    assert main(["check", str(source)]) == 1

    output = capsys.readouterr()
    assert "SEM006" in output.err
    assert "SEM008" in output.err
    assert "line" in output.err
