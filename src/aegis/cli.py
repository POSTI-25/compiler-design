"""Command-line entry point for the AEGIS project foundation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from aegis.ast import ast_to_dict
from aegis.ir import IRGenerator, render_ir
from aegis.ir.nodes import (
    IRBinary,
    IRBlock,
    IRCamera,
    IRCaptureImage,
    IRIf,
    IRIdentifier,
    IRLiteral,
    IRMove,
    IRPower,
    IRRepeat,
    IRSafeMode,
    IRTransmitImage,
    IRUnary,
    IRWait,
)
from aegis.lexer import Lexer
from aegis.parser import Parser
from aegis.runtime import Interpreter, RuntimeError
from aegis.semantic import SemanticAnalyzer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AEGIS compiler foundation")
    parser.add_argument(
        "command_or_source",
        nargs="?",
        help="use 'tokenize' or provide an optional source path",
    )
    parser.add_argument("source", nargs="?", type=Path, help="source path for the tokenize command")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command_or_source == "tokenize":
        if args.source is None:
            print("Usage error: tokenize requires a source file path.", file=sys.stderr)
            return 2
        return _tokenize_file(args.source)
    if args.command_or_source == "parse":
        if args.source is None:
            print("Usage error: parse requires a source file path.", file=sys.stderr)
            return 2
        return _parse_file(args.source)
    if args.command_or_source == "check":
        if args.source is None:
            print("Usage error: check requires a source file path.", file=sys.stderr)
            return 2
        return _check_file(args.source)
    if args.command_or_source == "ir":
        if args.source is None:
            print("Usage error: ir requires a source file path.", file=sys.stderr)
            return 2
        return _ir_file(args.source)
    if args.command_or_source == "run":
        if args.source is None:
            print("Usage error: run requires a source file path.", file=sys.stderr)
            return 2
        return _run_file(args.source)
    if args.command_or_source == "inspect":
        if args.source is None:
            print("Usage error: inspect requires a source file path.", file=sys.stderr)
            return 2
        return _inspect_file(args.source)

    print("AEGIS Compiler")
    print("Status: Project foundation initialized")
    print("Compiler pipeline: Not implemented yet")
    if args.command_or_source is not None:
        print(f"Source file detected: {args.command_or_source}")
        print("Processing: Not implemented yet")
    return 0


def _tokenize_file(source_path: Path) -> int:
    try:
        source = source_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Could not read source file {source_path}: {error}", file=sys.stderr)
        return 1

    lexer = Lexer(source)
    tokens = lexer.tokenize()
    for token in tokens:
        print(f"{token.line}:{token.column} {token.type.name} {token.lexeme!r}")
    for error in lexer.errors:
        print(error, file=sys.stderr)
    return 1 if lexer.errors else 0


def _parse_file(source_path: Path) -> int:
    try:
        source = source_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Could not read source file {source_path}: {error}", file=sys.stderr)
        return 1

    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    for error in lexer.errors:
        print(error, file=sys.stderr)
    for error in parser.errors:
        print(error, file=sys.stderr)
    if program is not None:
        print(json.dumps(ast_to_dict(program), indent=2))
    return 1 if lexer.errors or parser.errors else 0


def _check_file(source_path: Path) -> int:
    try:
        source = source_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Could not read source file {source_path}: {error}", file=sys.stderr)
        return 1

    lexer = Lexer(source)
    program = Parser(lexer.tokenize())
    parsed_program = program.parse()
    if lexer.errors or program.errors or parsed_program is None:
        for error in lexer.errors:
            print(error, file=sys.stderr)
        for error in program.errors:
            print(error, file=sys.stderr)
        return 1

    diagnostics = SemanticAnalyzer().analyze(parsed_program)
    for diagnostic in diagnostics:
        print(diagnostic, file=sys.stderr)
    if not diagnostics:
        print("Semantic check passed.")
    return 1 if diagnostics else 0


def _ir_file(source_path: Path) -> int:
    try:
        source = source_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Could not read source file {source_path}: {error}", file=sys.stderr)
        return 1

    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    if lexer.errors or parser.errors or program is None:
        for error in lexer.errors:
            print(error, file=sys.stderr)
        for error in parser.errors:
            print(error, file=sys.stderr)
        return 1

    semantic_diagnostics = SemanticAnalyzer().analyze(program)
    if semantic_diagnostics:
        for diagnostic in semantic_diagnostics:
            print(diagnostic, file=sys.stderr)
        return 1

    print(render_ir(IRGenerator().generate(program)))
    return 0


def _run_file(source_path: Path) -> int:
    try:
        source = source_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Could not read source file {source_path}: {error}", file=sys.stderr)
        return 1

    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    if lexer.errors or parser.errors or program is None:
        for error in lexer.errors:
            print(error, file=sys.stderr)
        for error in parser.errors:
            print(error, file=sys.stderr)
        return 1

    semantic_diagnostics = SemanticAnalyzer().analyze(program)
    if semantic_diagnostics:
        for diagnostic in semantic_diagnostics:
            print(diagnostic, file=sys.stderr)
        return 1

    try:
        state = Interpreter().run(IRGenerator().generate(program))
    except RuntimeError as error:
        print(f"[RUNTIME ERROR] {error}", file=sys.stderr)
        return 1

    print("Execution trace:")
    for entry in state.trace:
        print(f"  {entry}")
    print("Final runtime state:")
    print(f"  battery: {state.battery}")
    print(f"  position: {state.position}")
    print(f"  elapsed_time: {state.elapsed_time}")
    print(f"  camera_on: {state.camera_on}")
    print(f"  image_captured: {state.image_captured}")
    print(f"  safe_mode: {state.safe_mode}")
    return 0


def _inspect_file(source_path: Path) -> int:
    report: dict[str, object] = {
        "source_file": str(source_path),
        "overall_status": "failure",
        "stages": {
            name: {"status": "not_run", "summary": "not reached"}
            for name in (
                "source_loading",
                "lexical_analysis",
                "parsing",
                "ast_generation",
                "semantic_analysis",
                "ir_generation",
                "runtime_execution",
                "final_runtime_state",
            )
        },
        "token_count": None,
        "ast_statement_count": None,
        "ir_instruction_count": None,
        "executed_instruction_count": 0,
        "state_mutation_count": 0,
        "execution_events": [],
        "final_runtime_state": None,
    }

    try:
        source = source_path.read_text(encoding="utf-8")
        _record_stage(report, "source_loading", True, f"loaded {len(source)} characters")
    except OSError as error:
        _record_stage(report, "source_loading", False, "source could not be loaded", [str(error)])
        return _finish_inspection(report, "Source loading failed.")

    lexer = Lexer(source)
    tokens = lexer.tokenize()
    report["token_count"] = len(tokens)
    if lexer.errors:
        _record_stage(report, "lexical_analysis", False, f"{len(tokens)} tokens produced", [str(error) for error in lexer.errors])
        return _finish_inspection(report, "Lexical analysis failed.")
    _record_stage(report, "lexical_analysis", True, f"{len(tokens)} tokens produced")

    parser = Parser(tokens)
    program = parser.parse()
    if parser.errors or program is None:
        _record_stage(report, "parsing", False, "AST was not produced", [str(error) for error in parser.errors])
        _record_stage(report, "ast_generation", False, "blocked by parser errors")
        return _finish_inspection(report, "Parsing failed.")
    _record_stage(report, "parsing", True, "source accepted by grammar")
    report["ast_statement_count"] = _count_ast_statements(program.body)
    _record_stage(report, "ast_generation", True, f"{report['ast_statement_count']} statements")

    semantic_diagnostics = SemanticAnalyzer().analyze(program)
    if semantic_diagnostics:
        _record_stage(report, "semantic_analysis", False, "semantic errors found", [str(item) for item in semantic_diagnostics])
        return _finish_inspection(report, "Semantic analysis failed.")
    _record_stage(report, "semantic_analysis", True, "no semantic errors")

    ir = IRGenerator().generate(program)
    report["ir_instruction_count"] = _count_ir_instructions(ir.body)
    _record_stage(report, "ir_generation", True, f"{report['ir_instruction_count']} instructions")

    events: list[dict[str, object]] = []

    def on_event(instruction, before, after, success, error):
        event = {
            "instruction": _describe_ir_instruction(instruction),
            "instruction_type": type(instruction).__name__,
            "state_before": before,
            "state_after": after,
            "state_changed": before != after,
            "battery_before": before["battery"],
            "battery_after": after["battery"],
            "success": success,
        }
        if error is not None:
            event["error"] = error
        events.append(event)

    interpreter = Interpreter(event_callback=on_event)
    try:
        state = interpreter.run(ir)
    except RuntimeError as error:
        report["execution_events"] = events
        report["executed_instruction_count"] = len(events)
        report["state_mutation_count"] = sum(bool(event["state_changed"]) for event in events)
        report["final_runtime_state"] = _runtime_state_dict(interpreter.state)
        _record_stage(report, "runtime_execution", False, "runtime error", [str(error)])
        _record_stage(report, "final_runtime_state", True, "partial runtime state captured")
        return _finish_inspection(report, "Runtime execution failed.")

    report["execution_events"] = events
    report["executed_instruction_count"] = len(events)
    report["state_mutation_count"] = sum(bool(event["state_changed"]) for event in events)
    report["final_runtime_state"] = _runtime_state_dict(state)
    _record_stage(report, "runtime_execution", True, f"{len(events)} instructions executed")
    _record_stage(report, "final_runtime_state", True, "runtime state captured")
    report["overall_status"] = "success"
    return _finish_inspection(report, "Inspection succeeded.")


def _record_stage(report: dict[str, object], name: str, success: bool, summary: str, errors: list[str] | None = None) -> None:
    stage = {"status": "success" if success else "failure", "summary": summary}
    if errors:
        stage["errors"] = errors
    report["stages"][name] = stage


def _finish_inspection(report: dict[str, object], message: str) -> int:
    artifact_path = Path("artifacts") / "last_run.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(message)
    for name, stage in report["stages"].items():
        print(f"{name}: {stage['status']} - {stage['summary']}")
        for error in stage.get("errors", []):
            print(f"  error: {error}")
    for event in report["execution_events"]:
        print(f"instruction: {event['instruction']}")
        print(f"  before: {event['state_before']}")
        print(f"  after: {event['state_after']}")
        print(f"  changed: {event['state_changed']}; battery: {event['battery_before']} -> {event['battery_after']}; success: {event['success']}")
    if report["final_runtime_state"] is not None:
        print(f"final runtime state: {report['final_runtime_state']}")
    return 0 if report["overall_status"] == "success" else 1


def _count_ast_statements(block) -> int:
    count = 0
    for statement in block.statements:
        count += 1
        if hasattr(statement, "then_branch"):
            count += _count_ast_statements(statement.then_branch)
            if statement.else_branch is not None:
                count += _count_ast_statements(statement.else_branch)
        if hasattr(statement, "body") and hasattr(statement.body, "statements"):
            count += _count_ast_statements(statement.body)
    return count


def _count_ir_instructions(block: IRBlock) -> int:
    count = len(block.instructions)
    for instruction in block.instructions:
        if isinstance(instruction, IRIf):
            count += _count_ir_instructions(instruction.then_block)
            if instruction.else_block is not None:
                count += _count_ir_instructions(instruction.else_block)
        elif isinstance(instruction, IRRepeat):
            count += _count_ir_instructions(instruction.body)
    return count


def _runtime_state_dict(state) -> dict[str, object]:
    return {
        "battery": state.battery,
        "position": state.position,
        "elapsed_time": state.elapsed_time,
        "camera_on": state.camera_on,
        "image_captured": state.image_captured,
        "safe_mode": state.safe_mode,
    }


def _describe_ir_instruction(instruction) -> str:
    if isinstance(instruction, IRPower):
        return f"POWER {_describe_ir_expression(instruction.value)}"
    if isinstance(instruction, IRMove):
        return f"MOVE {_describe_ir_expression(instruction.distance)}"
    if isinstance(instruction, IRCamera):
        return f"CAMERA {'ON' if instruction.enabled else 'OFF'}"
    if isinstance(instruction, IRCaptureImage):
        return "CAPTURE IMAGE"
    if isinstance(instruction, IRTransmitImage):
        return "TRANSMIT IMAGE"
    if isinstance(instruction, IRWait):
        return f"WAIT {_describe_ir_expression(instruction.duration)}"
    if isinstance(instruction, IRSafeMode):
        return "SAFE_MODE"
    if isinstance(instruction, IRIf):
        return f"IF {_describe_ir_expression(instruction.condition)}"
    if isinstance(instruction, IRRepeat):
        return f"REPEAT {_describe_ir_expression(instruction.count)}"
    return type(instruction).__name__


def _describe_ir_expression(expression) -> str:
    if isinstance(expression, IRLiteral):
        return repr(expression.value) if isinstance(expression.value, str) else str(expression.value)
    if isinstance(expression, IRIdentifier):
        return expression.name
    if isinstance(expression, IRUnary):
        return f"({expression.operator}{_describe_ir_expression(expression.operand)})"
    if isinstance(expression, IRBinary):
        return f"({_describe_ir_expression(expression.left)} {expression.operator} {_describe_ir_expression(expression.right)})"
    return type(expression).__name__


if __name__ == "__main__":
    raise SystemExit(main())
