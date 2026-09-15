from pathlib import Path

from aegis import __version__
from aegis.cli import main


PROJECT_ROOT = Path(__file__).parents[1]


def test_foundation_package_and_files_exist() -> None:
    assert __version__ == "0.1.0"
    assert (PROJECT_ROOT / "compiler_prd.md").is_file()
    assert (PROJECT_ROOT / "context.md").is_file()


def test_cli_reports_foundation_status(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "valid" / "observation.aegis"

    assert main([str(source)]) == 0

    output = capsys.readouterr().out
    assert "AEGIS Compiler" in output
    assert "Project foundation initialized" in output
    assert "Compiler pipeline: Not implemented yet" in output
    assert str(source) in output
