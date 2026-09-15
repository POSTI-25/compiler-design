from pathlib import Path

from aegis.cli import main


PROJECT_ROOT = Path(__file__).parents[2]


def test_tokenize_cli_prints_tokens_for_valid_source(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "valid" / "observation.aegis"

    assert main(["tokenize", str(source)]) == 0

    output = capsys.readouterr()
    assert "MISSION 'MISSION'" in output.out
    assert "EOF ''" in output.out
    assert output.err == ""


def test_tokenize_cli_returns_nonzero_for_lexical_errors(tmp_path, capsys) -> None:
    source = tmp_path / "invalid.aegis"
    source.write_text("MISSION @", encoding="utf-8")

    assert main(["tokenize", str(source)]) == 1

    output = capsys.readouterr()
    assert "Lexical error at line 1, column 9" in output.err
