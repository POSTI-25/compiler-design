from pathlib import Path

from aegis.cli import main


PROJECT_ROOT = Path(__file__).parents[2]


def test_run_cli_executes_valid_mission(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "valid" / "observation.aegis"

    assert main(["run", str(source)]) == 0

    output = capsys.readouterr()
    assert "Execution trace:" in output.out
    assert "CAPTURE IMAGE" in output.out
    assert "Final runtime state:" in output.out
    assert "battery: 80" in output.out
    assert output.err == ""


def test_run_cli_rejects_invalid_source(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "invalid" / "semantic_errors.aegis"

    assert main(["run", str(source)]) == 1

    output = capsys.readouterr()
    assert "SEM006" in output.err
    assert output.out == ""


def test_run_cli_reports_runtime_failure(tmp_path, capsys) -> None:
    source = tmp_path / "runtime_failure.aegis"
    source.write_text(
        "MISSION unsafe { SAFE_MODE; MOVE 1; }",
        encoding="utf-8",
    )

    assert main(["run", str(source)]) == 1

    output = capsys.readouterr()
    assert "[RUNTIME ERROR]" in output.err
    assert "MOVE is unavailable in safe mode" in output.err
    assert output.out == ""
