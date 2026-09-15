# AEGIS Compiler

AEGIS is an academic domain-specific language and compiler project for expressing high-level autonomous spacecraft mission logic. It is designed for Compiler Design (BCSE307P) at Vellore Institute of Technology, Vellore.

## Current Status

The project foundation and lexer are implemented. The parser, AST, semantic analyzer, symbol table, IR, optimizer, target-code generator, and Mission VM are not implemented yet.

## Planned Pipeline

```text
Source -> Lexer -> Parser -> AST -> Semantic Analysis
       -> IR -> Optimizer -> Target Code -> Mission VM
       -> Execution Trace and Diagnostics
```

## Setup

Requires Python 3.12 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
```

## CLI

```powershell
aegis
# or
python -m aegis.cli examples/valid/observation.aegis
# tokenize a source file
python -m aegis.cli tokenize examples/valid/observation.aegis
```

The default CLI reports project status. The `tokenize` command runs lexical analysis and prints positioned tokens; it does not parse or compile the example yet.

## Tests

```powershell
pytest
```

## Limitations

AEGIS is a simulated, educational compiler project. It will not control real spacecraft, hardware, telemetry, networks, or flight systems. Detailed physics, real-time behavior, and production safety certification are outside the project scope.

## Project Documents

- [Product Requirements Document](compiler_prd.md)
- [Project Context](context.md)
- [Architecture](docs/architecture.md)
- [Language Specification](docs/language_specification.md)
