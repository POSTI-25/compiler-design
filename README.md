# AEGIS Compiler

AEGIS is an academic domain-specific language and compiler project for expressing high-level autonomous spacecraft mission logic. It is designed for Compiler Design (BCSE307P) at Vellore Institute of Technology, Vellore.

## Current Status

The project foundation, lexer, parser, AST, semantic analysis, symbol table, and structured IR are implemented. Optimization, target-code generation, bytecode generation, and the Mission VM are not implemented yet.

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
# parse a source file and print its AST
python -m aegis.cli parse examples/valid/observation.aegis
# run semantic checks
python -m aegis.cli check examples/valid/observation.aegis
# generate structured IR
python -m aegis.cli ir examples/valid/observation.aegis
```

The default CLI reports project status. `tokenize` prints positioned tokens. `parse` prints the AST and syntax diagnostics. `check` performs semantic analysis. `ir` prints deterministic structured IR. None of these commands performs optimization, target-code generation, bytecode generation, or VM execution.

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
