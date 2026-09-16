"""Command-line entry point for the AEGIS project foundation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from aegis.ast import ast_to_dict
from aegis.ir import IRGenerator, render_ir
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


if __name__ == "__main__":
    raise SystemExit(main())
