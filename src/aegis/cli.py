"""Command-line entry point for the AEGIS project foundation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from aegis.ast import ast_to_dict
from aegis.lexer import Lexer
from aegis.parser import Parser


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


if __name__ == "__main__":
    raise SystemExit(main())
