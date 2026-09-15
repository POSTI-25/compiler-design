"""Command-line entry point for the AEGIS project foundation."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AEGIS compiler foundation")
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        help="optional .aegis source file; compilation is not implemented yet",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    print("AEGIS Compiler")
    print("Status: Project foundation initialized")
    print("Compiler pipeline: Not implemented yet")
    if args.source is not None:
        print(f"Source file detected: {args.source}")
        print("Processing: Not implemented yet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
