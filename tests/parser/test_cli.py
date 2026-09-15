from pathlib import Path

from aegis.cli import main


PROJECT_ROOT = Path(__file__).parents[2]


def test_parse_cli_prints_ast_for_valid_source(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "valid" / "observation.aegis"

    assert main(["parse", str(source)]) == 0

    output = capsys.readouterr()
    assert '"type": "Mission"' in output.out
    assert '"name": "observation"' in output.out
    assert output.err == ""


def test_parse_cli_returns_nonzero_for_invalid_source(tmp_path, capsys) -> None:
    source = tmp_path / "invalid.aegis"
    source.write_text("MISSION broken { POWER 80 }", encoding="utf-8")

    assert main(["parse", str(source)]) == 1

    output = capsys.readouterr()
    assert "Expected ';'" in output.err
