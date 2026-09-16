# AEGIS Compiler

AEGIS is an academic domain-specific language and compiler project for expressing high-level autonomous spacecraft mission logic. It is designed for Compiler Design (BCSE307P) at Vellore Institute of Technology, Vellore.

## MVP

The bare-minimum MVP accepts an AEGIS mission file, tokenizes it, parses it into an AST, performs semantic checks, generates structured IR, and interprets that IR with a deterministic simulated runtime. It reports diagnostics, execution traces, and final runtime state.

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
# execute the complete MVP
python -m aegis.cli run examples/valid/observation.aegis
```

## Demonstration Workflow

Run the complete MVP from the project root:

```powershell
python -m pip install -e ".[test]"
python -m aegis.cli tokenize examples/valid/observation.aegis
python -m aegis.cli parse examples/valid/observation.aegis
python -m aegis.cli check examples/valid/observation.aegis
python -m aegis.cli ir examples/valid/observation.aegis
python -m aegis.cli run examples/valid/observation.aegis
```

The final command prints the execution trace and final runtime state. To demonstrate semantic failure:

```powershell
python -m aegis.cli run examples/invalid/semantic_errors.aegis
```

## Example

```aegis
MISSION observation {
       POWER 80;
       CAMERA ON;
       CAPTURE IMAGE;
       CAMERA OFF;
       TRANSMIT IMAGE;
}
```

## Tests

```powershell
py -m pytest -q
```

Final validation result: `69 passed`.

## Limitations

AEGIS is a simulated, educational compiler project. It intentionally excludes optimization, target-code generation, bytecode, advanced VM architecture, scheduling, solar/eclipse simulation, thermal simulation, telemetry, fault injection, networking, databases, dashboards, real spacecraft control, hardware, and production flight software.

## Project Documents

- [Product Requirements Document](compiler_prd.md)
- [Project Context](context.md)
- [Architecture](docs/architecture.md)
- [Language Specification](docs/language_specification.md)
