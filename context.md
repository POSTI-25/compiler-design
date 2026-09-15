# AEGIS Project Context

## 1. Project Identity

- Name: AEGIS
- Course: Compiler Design (BCSE307P)
- Institution: Vellore Institute of Technology, Vellore
- Project type: Academic domain-specific language compiler and simulated mission VM
- Context last updated: 2026-09-15

## 2. Project Objective

AEGIS will compile a small spacecraft-mission DSL through lexical analysis, syntax analysis, AST construction, semantic analysis, symbol-table management, IR generation, optimization, target-code generation, and execution in a simulated Mission Virtual Machine.

The system is an explainable educational prototype. It must not be presented as spacecraft flight software, hardware control, real telemetry integration, safety-certified software, or a detailed physical simulator.

## 3. Current Status

The project foundation and lexer are implemented and validated. The repository now contains Python project metadata, a package skeleton, a status/tokenize CLI, positioned token definitions, lexical diagnostics, documentation, one valid source example, and smoke/lexer tests. No compiler phase after lexical analysis has been implemented.

## 4. Approved Requirements

Requirements explicitly stated in `compiler_prd.md`:

- Accept mission source files and, where practical, source strings through an API.
- Preserve line and column locations.
- Define a small language with keywords, identifiers, numbers, strings where needed, booleans, operators, delimiters, comments, statement termination, blocks, precedence, command forms, and type rules.
- Implement lexical, syntax, AST, semantic, symbol-table, IR, optimization, target-code, VM, diagnostics, testing, and reporting capabilities.
- Initial commands: `POWER`, `MOVE`, `CAMERA ON`, `CAMERA OFF`, `CAPTURE IMAGE`, `TRANSMIT IMAGE`, `WAIT`, and `SAFE_MODE`.
- Initial state concepts: battery, temperature, visibility, camera, captured image, movement distance, communication, and safe mode.
- Initial control flow: `IF`, `ELSE`, `END`, and bounded `REPEAT`.
- Validate declarations, types, ranges, command sequencing, resource dependencies, and bounded repetition.
- Implement at least two documented optimizations, including candidates such as constant folding, unreachable/dead code removal, redundant camera-command removal, and movement merging.
- Generate a documented custom instruction set or bytecode for one simulated target.
- Execute valid target code in a VM with runtime state and an execution trace.
- Distinguish lexical, syntax, semantic, and runtime diagnostics and avoid executing unresolved fatal compilation errors.
- Provide unit tests for major modules and integration tests for complete workflows.
- Provide command-line demonstration scripts for successful compilation, fault detection, and optimization.
- Provide readable intermediate artifacts; visualization is optional and may begin with text output.

Explicit exclusions include hardware drivers, real telemetry or networking, uplink/downlink, orbital mechanics, high-fidelity physics, real-time OS behavior, flight certification, multiple hardware targets, and industrial-scale performance.

## 5. Requirements Still Requiring Clarification

- Exact declaration and type-annotation syntax; the PRD lists possible types but does not define their grammar.
- Exact semantics and syntax of sensor/state reads such as `BATTERY` and `TEMPERATURE`.
- Whether `END` is a standalone block terminator, whether braces are also required, or whether both forms are accepted.
- Exact argument grammar for `MOVE`, `WAIT`, `REPEAT`, `POWER SAVE`, and `SAFE_MODE`.
- Whether decimal values, strings, booleans, and variables are required in the first language slice or can be staged.
- Safe-mode restrictions and the precise battery/energy update rules in the simulator.
- The initial bounded maximum for `REPEAT`.
- Which visualization outputs are required for the final demonstration versus optional text reports.

Resolved for lexical analysis: the PRD requires string and boolean token recognition, while the provisional language specification deferred their use in commands. The lexer will recognize `TRUE`/`FALSE` and quoted strings without assigning them parser or semantic meaning yet.

These questions do not block repository planning, but they must be resolved before the grammar and semantic contract are finalized.

## 6. Current Architecture

Proposed data flow:

```text
Source -> Lexer -> Tokens -> Parser -> AST -> Symbols/Semantics
       -> Raw IR -> Optimizer -> Target Instructions -> Mission VM
       -> Simulated State and Execution Trace
```

Proposed modules and responsibilities:

- `lexer`: token kinds, source positions, tokenization, lexical diagnostics.
- `parser`: grammar implementation, recovery at statement/block boundaries, AST construction entry point.
- `ast`: readable node dataclasses, source spans, traversal, and serialization/printing.
- `symbols`: scoped symbol table and declaration metadata.
- `semantic`: type checking, declaration checks, command sequencing, ranges, and domain rules.
- `ir`: machine-independent instructions, temporaries, labels, and readable IR output.
- `optimizer`: independently testable passes, before/after output, and transformation records.
- `codegen`: documented target instruction format and IR-to-target lowering.
- `runtime`: VM, runtime environment, simulated spacecraft state, and execution trace.
- `diagnostics`: shared errors/warnings with category, location, message, and optional context.
- `visualization`: text reports first; Graphviz export only after the core pipeline is stable.
- `pipeline`: orchestration and phase results for the CLI and programmatic API.

The initial implementation should prefer readable Python data structures and a custom IR/VM. No LLVM, database, cloud service, hardware API, or machine-learning dependency is planned.

## 7. Repository Structure

Current structure:

```text
compiler_prd.md
context.md
README.md
pyproject.toml
src/aegis/__init__.py
src/aegis/cli.py
src/aegis/pipeline/__init__.py
tests/__init__.py
tests/test_smoke.py
examples/valid/observation.aegis
docs/architecture.md
docs/language_specification.md
```

Planned structure, to be created incrementally:

```text
README.md
pyproject.toml
requirements.txt                 # only if runtime dependencies are needed
grammar/                          # only if ANTLR4 is selected
src/aegis/
  __init__.py
  lexer/
  parser/
  ast/
  symbols/
  semantic/
  ir/
  optimizer/
  codegen/
  runtime/
  diagnostics/
  visualization/
  pipeline/
  cli.py
tests/
examples/
docs/
```

Empty directories will not be created ahead of the module that uses them.

## 8. Completed Work

- Audited the workspace before changes: only `compiler_prd.md` and the historical `context.md` were present; no compiler source, tests, configuration, dependencies, or examples existed.
- Confirmed the Git repository is on branch `main`.
- Read the complete PRD and preserved the existing context history.
- Selected handwritten recursive-descent parsing provisionally instead of ANTLR4.
- Selected brace-based blocks provisionally and excluded mixed `END` syntax from the initial style.
- Created the Python project foundation, package metadata, status CLI, documentation, example, and smoke tests.
- Installed pytest into the configured Python 3.12.4 environment for validation.
- Implemented a handwritten lexer with keywords, identifiers, numeric/string/boolean lexemes, operators, punctuation, comments, positions, recoverable errors, and exactly one EOF token.
- Added focused lexer tests covering token order, keywords, identifiers, literals, symbols, comments, positions, errors, EOF, and CLI behavior.
- Added `tokenize` CLI support for valid and invalid `.aegis` files.
- Updated README and architecture/language documents to reflect the lexer milestone.

## 9. Work In Progress

- Reviewing the lexer contract before parser design.
- Resolving declaration/type syntax and runtime semantics that remain open in the PRD.

## 10. Pending Tasks

- Finalize declaration/type syntax and expression details before implementing the parser.
- Review lexer token and source-location contracts for parser integration.
- Define the first grammar slice and parser recovery rules.
- Add AST, symbol table, semantic rules, IR, optimizer, code generator, VM, CLI, examples, and integration tests incrementally.
- Add optional visualization after text reports and core behavior are stable.

## 11. Known Issues

- The PRD has several intentionally open language details, so a final grammar cannot yet be treated as approved.
- Parser and later compiler phases have not been implemented yet.
- The VM state-transition model and safe-mode restrictions are not yet specified precisely.

## 12. Design Decisions

- The project will be implemented incrementally, one coherent compiler slice at a time.
- Python 3 is the implementation language; the available runtime is Python 3.12.4.
- A custom, readable IR and custom Mission VM are preferred for educational transparency.
- Text-based artifact reporting will precede optional Graphviz or other visualization.
- Handwritten recursive-descent parsing is selected provisionally because the language is small and the implementation is easier to explain and control than ANTLR4 for the first version.
- Braces are the provisional block delimiters for the initial language style; `END` will not be mixed with braces.
- The initial language subset is limited to mission declarations, the PRD command set, planned `IF`/`ELSE`/`REPEAT` control flow, numeric literals, boolean conditions, comments, braces, and semicolons.
- The project uses a `src` package layout, `pyproject.toml`, and pytest for development testing.
- The CLI accepts an optional source path but only reports that processing is not implemented; it does not emit fake compiler artifacts.
- The lexer will ignore whitespace and `//` line comments, track newlines for positions, and emit no newline tokens because the language specification treats whitespace as insignificant.
- The lexer will recover from lexical errors by recording them, consuming the invalid sequence where possible, and continuing to emit later tokens plus exactly one EOF token.
- The first vertical slice should cover source input, tokens, a minimal mission/command AST, diagnostics, and tests before control flow or optimization.

## 13. Assumptions

- The PRD is the current requirements authority.
- Braced mission examples are the initial syntax reference; `END` and alternate block forms remain open until clarified.
- The first target is a single readable assembly-like instruction format consumed directly by the VM.
- `pytest` is the provisional test framework unless the project chooses standard-library `unittest`.
- No external runtime dependency will be added until a concrete requirement justifies it.
- Semantic validation will block VM execution when fatal diagnostics remain.

## 14. Testing Status

- Foundation smoke suite: passed, 2 tests.
- Validation command: `C:/Users/JAHNAVI SINGH/AppData/Local/Programs/Python/Python312/python.exe -m pytest`.
- The `pytest` shell command was not initially available on `PATH`; pytest was installed into the configured interpreter and the module invocation passed.
- No compiler-phase tests exist yet. Planned coverage includes unit tests for each compiler phase and integration tests for valid, faulty, conditional, repetition, and optimization-focused missions.

## 15. Commands

Available environment check:

```text
python --version  -> Python 3.12.4
py --version      -> Python 3.12.4
```

Setup: `python -m pip install -e ".[test]"`

Tests: `python -m pytest`

CLI after editable installation: `aegis` or `python -m aegis.cli examples/valid/observation.aegis`

The CLI currently reports foundation status only and does not compile source files.

## 16. Dependencies

- Runtime dependencies: none.
- Development/test dependency: `pytest>=8.0` in the optional `test` dependency group.
- ANTLR4 and Graphviz are not configured.
- The core design should remain usable without optional visualization dependencies.

## 17. Compiler Pipeline Status

| Stage | Status | Files | Tests | Notes |
|---|---|---|---|---|
| Project foundation | Implemented | `pyproject.toml`, `README.md`, package skeleton | 2 smoke tests passed | Foundation only; no compiler phase implemented |
| Source input | Implemented | `src/aegis/cli.py` | Smoke-tested | CLI can read a source file for tokenization |
| Lexer | Tested | `src/aegis/lexer/` | 13 lexer tests passed | Handwritten lexer with recovery and positioned tokens |
| Parser | Not started | None | None | Handwritten recursive descent selected provisionally |
| AST | Not started | None | None | Must preserve logical structure and locations |
| Semantic analysis | Not started | None | None | Domain rules and type checks required |
| Symbol table | Not started | None | None | Scope and declaration metadata required |
| IR generation | Not started | None | None | Readable machine-independent representation |
| Optimization | Not started | None | None | At least two independently testable passes |
| Target code generation | Not started | None | None | One documented target format |
| Mission VM | Not started | None | None | Simulated state and trace only |
| Error recovery | Partially implemented | `src/aegis/lexer/` | Covered by lexer error tests | Lexer records errors and continues; later phase recovery is not implemented |
| Visualization | Planned | None | None | Text reports first; richer output optional |

## 18. Important Files

- `compiler_prd.md`: authoritative product requirements document.
- `context.md`: maintained project memory, status, decisions, assumptions, and activity log.
- `README.md`: setup, status, usage, tests, and scope boundary.
- `pyproject.toml`: package metadata, editable-install configuration, CLI entry point, and pytest configuration.
- `docs/architecture.md`: planned pipeline and module responsibilities.
- `docs/language_specification.md`: provisional initial language subset and syntax decisions.
- `src/aegis/lexer/`: positioned token definitions, lexical diagnostics, and handwritten lexer.
- `tests/lexer/`: focused lexical and tokenize CLI tests.

## 19. Agent Activity Log

- 2026-09-15: Audited the repository and found only `compiler_prd.md`.
- 2026-09-15: Confirmed Git branch `main` and Python 3.12.4 availability.
- 2026-09-15: Read the complete PRD and recorded explicit requirements, exclusions, ambiguities, architecture, and roadmap direction.
- 2026-09-15: Created the initial `context.md`; no compiler implementation was started.
- 2026-09-15: Re-read the PRD and context, checked the repository and Git status, and confirmed no compiler phase was present.
- 2026-09-15: Created `README.md`, `pyproject.toml`, `src/aegis/__init__.py`, `src/aegis/cli.py`, `src/aegis/pipeline/__init__.py`, `tests/__init__.py`, `tests/test_smoke.py`, `examples/valid/observation.aegis`, `docs/architecture.md`, and `docs/language_specification.md`.
- 2026-09-15: Ran the foundation smoke suite successfully: 2 tests passed.
- 2026-09-15: Unresolved questions remain around declaration/type syntax, expressions, and VM semantics. The next task is lexer implementation after those contracts are reviewed.
- 2026-09-15: Resolved the PRD/specification tension by recognizing strings and booleans lexically while deferring their parser and semantic use.
- 2026-09-15: Implemented `src/aegis/lexer/` with positioned tokens, comments, literals, operators, lexical diagnostics, recovery, and EOF handling.
- 2026-09-15: Added lexer tests and validated 13 lexer tests successfully.
- 2026-09-15: Added `python -m aegis.cli tokenize <source>` and validated valid and invalid lexical CLI behavior.

## 20. Next Recommended Action

Review the tested lexer and its token contract, then implement the parser. Keep AST, semantic analysis, IR, optimization, code generation, and VM work out of the parser milestone.

## Initial Implementation Roadmap

### Milestone 1: Foundation

- Objective: Establish a runnable Python package, CLI entry point, test discovery, README, and a minimal example.
- Dependencies: Parser and language choices only need provisional documentation.
- Expected output: A command can load a source file and report that the pipeline is not yet implemented.
- Tests: Package import and CLI smoke test.
- Completion criteria: Setup instructions work on Windows and tests are discoverable.

### Milestone 2: Lexer

- Objective: Tokenize the approved initial language subset with positions and recoverable lexical diagnostics.
- Dependencies: Token contract and lexical grammar.
- Expected output: Token stream for a valid mission and diagnostics for invalid characters/literals.
- Tests: Keywords, identifiers, literals, operators, punctuation, comments, positions, and invalid input.
- Completion criteria: Lexer behavior is documented and independently tested.

### Milestone 3: Parser and AST

- Objective: Parse mission declarations, initial commands, expressions, and the approved block form into a readable AST.
- Dependencies: Lexer and resolved grammar decisions.
- Expected output: AST printer/serializer and recoverable syntax diagnostics.
- Tests: Valid programs, missing delimiters/semicolons, malformed commands, and recovery boundaries.
- Completion criteria: Representative scripts parse and AST structure is inspectable.

### Milestone 4: Symbols and Semantics

- Objective: Add declarations, scopes, types, command arguments, ranges, and mission-specific sequencing rules.
- Dependencies: AST and resolved type/declaration syntax.
- Expected output: Symbol table and categorized semantic diagnostics.
- Tests: Undeclared/duplicate names, type errors, ranges, camera/image dependencies, and invalid repetition.
- Completion criteria: Fatal semantic errors prevent later execution.

### Milestone 5: IR and Optimization

- Objective: Generate readable machine-independent IR and implement at least two semantics-preserving optimizations.
- Dependencies: Valid AST and semantic contract.
- Expected output: Raw/optimized IR plus transformation records.
- Tests: Commands, expressions, labels, conditionals, repetition, constant folding, dead/unreachable code, and one mission-specific rule.
- Completion criteria: Before/after output is understandable and tests cover meaning preservation.

### Milestone 6: Target Code and VM

- Objective: Lower optimized IR to one documented instruction set and execute it in a simulated VM.
- Dependencies: Stable IR and runtime rules.
- Expected output: Target instructions, simulated state, runtime diagnostics, and execution trace.
- Tests: Power, movement, camera, image, wait, safe mode, jumps, and runtime failures.
- Completion criteria: Valid representative missions execute with expected final state.

### Milestone 7: Integration and Demonstration

- Objective: Connect the complete pipeline and provide successful, faulty, and optimization demonstrations.
- Dependencies: All core stages tested.
- Expected output: End-to-end CLI reports and final documentation.
- Tests: Full source-to-execution workflows and multi-error reporting.
- Completion criteria: The major Phase 2 success criteria are demonstrated without claiming excluded capabilities.