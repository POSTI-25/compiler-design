import json
from pathlib import Path

from aegis.cli import main


PROJECT_ROOT = Path(__file__).parents[2]
ARTIFACT = PROJECT_ROOT / "artifacts" / "last_run.json"


def read_artifact() -> dict:
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))


def test_inspect_succeeds_for_valid_program(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "valid" / "observation.aegis"

    assert main(["inspect", str(source)]) == 0

    output = capsys.readouterr()
    report = read_artifact()
    assert "runtime_execution: success" in output.out
    assert report["overall_status"] == "success"
    assert report["token_count"] > 0
    assert report["ir_instruction_count"] == 5
    assert set(report["stages"]) == {
        "source_loading",
        "lexical_analysis",
        "parsing",
        "ast_generation",
        "semantic_analysis",
        "ir_generation",
        "runtime_execution",
        "final_runtime_state",
    }


def test_inspect_reports_semantic_failure(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "invalid" / "semantic_errors.aegis"

    assert main(["inspect", str(source)]) == 1

    output = capsys.readouterr()
    report = read_artifact()
    assert "semantic_analysis: failure" in output.out
    assert report["overall_status"] == "failure"
    assert report["stages"]["semantic_analysis"]["errors"]
    assert report["stages"]["ir_generation"]["status"] == "not_run"


def test_inspect_events_capture_state_changes_and_final_state(capsys) -> None:
    source = PROJECT_ROOT / "examples" / "valid" / "observation.aegis"

    assert main(["inspect", str(source)]) == 0

    capsys.readouterr()
    report = read_artifact()
    events = report["execution_events"]
    mutations = [event for event in events if event["state_changed"]]

    assert events
    assert all("state_before" in event and "state_after" in event for event in events)
    assert mutations
    assert report["state_mutation_count"] == len(mutations)
    assert events[-1]["state_after"] == report["final_runtime_state"]
    assert any(event["battery_before"] != event["battery_after"] for event in events)
