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

Initialization analysis complete. The repository contains only the authoritative PRD, `compiler_prd.md`, and the newly created project context. No compiler implementation, configuration, examples, tests, or dependencies have been added yet.

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

- Whether the parser will use ANTLR4 or a handwritten recursive-descent implementation.
- Exact declaration and type-annotation syntax; the PRD lists possible types but does not define their grammar.
- Exact semantics and syntax of sensor/state reads such as `BATTERY` and `TEMPERATURE`.
- Whether `END` is a standalone block terminator, whether braces are also required, or whether both forms are accepted.
- Exact argument grammar for `MOVE`, `WAIT`, `REPEAT`, `POWER SAVE`, and `SAFE_MODE`.
- Whether decimal values, strings, booleans, and variables are required in the first language slice or can be staged.
- Safe-mode restrictions and the precise battery/energy update rules in the simulator.
- The initial bounded maximum for `REPEAT`.
- Which visualization outputs are required for the final demonstration versus optional text reports.

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

- Audited the workspace: only `compiler_prd.md` existed; no source, tests, configuration, dependency files, examples, or documentation beyond the PRD were present.
- Confirmed the workspace is a Git repository on branch `main` with no reported changes before initialization.
- Read the complete PRD.
- Created this initial project context.

## 9. Work In Progress

- Translating the PRD into a precise language specification.
- Selecting and documenting the parser strategy.
- Defining the smallest vertical slice for the first implementation milestone.

## 10. Pending Tasks

- Confirm parser strategy and declaration/type syntax.
- Create project metadata and setup documentation.
- Define tokens and source-location/diagnostic contracts.
- Implement and test the lexer.
- Define the first grammar slice and parser recovery rules.
- Add AST, symbol table, semantic rules, IR, optimizer, code generator, VM, CLI, examples, and integration tests incrementally.
- Add optional visualization after text reports and core behavior are stable.

## 11. Known Issues

- The PRD has several intentionally open language details, so a final grammar cannot yet be treated as approved.
- There is no implementation or automated test suite yet.
- The VM state-transition model and safe-mode restrictions are not yet specified precisely.

## 12. Design Decisions

- The project will be implemented incrementally, one coherent compiler slice at a time.
- Python 3 is the implementation language; the available runtime is Python 3.12.4.
- A custom, readable IR and custom Mission VM are preferred for educational transparency.
- Text-based artifact reporting will precede optional Graphviz or other visualization.
- The provisional parser direction is handwritten recursive descent because it minimizes setup and keeps grammar/recovery behavior visible; this is a proposal, not an approved irreversible decision.
- The first vertical slice should cover source input, tokens, a minimal mission/command AST, diagnostics, and tests before control flow or optimization.

## 13. Assumptions

- The PRD is the current requirements authority.
- Braced mission examples are the initial syntax reference; `END` and alternate block forms remain open until clarified.
- The first target is a single readable assembly-like instruction format consumed directly by the VM.
- `pytest` is the provisional test framework unless the project chooses standard-library `unittest`.
- No external runtime dependency will be added until a concrete requirement justifies it.
- Semantic validation will block VM execution when fatal diagnostics remain.

## 14. Testing Status

No tests exist yet and no test command has been run. Planned coverage includes unit tests for each compiler phase and integration tests for valid, faulty, conditional, repetition, and optimization-focused missions.

## 15. Commands

Available environment check:

```text
python --version  -> Python 3.12.4
py --version      -> Python 3.12.4
```

No project setup, build, test, or execution command exists yet. The first setup milestone must define these commands in `README.md` and project metadata.

## 16. Dependencies

No project dependencies are currently declared or installed. Candidate development dependencies are `pytest` and, only if selected, ANTLR4 tooling or Graphviz support. The core design should remain usable without optional visualization dependencies.

## 17. Compiler Pipeline Status

| Stage | Status | Files | Tests | Notes |
|---|---|---|---|---|
| Source input | Planned | None | None | File input and source-string API required |
| Lexer | Not started | None | None | Token positions and lexical diagnostics required |
| Parser | Not started | None | None | Parser strategy remains open |
| AST | Not started | None | None | Must preserve logical structure and locations |
| Semantic analysis | Not started | None | None | Domain rules and type checks required |
| Symbol table | Not started | None | None | Scope and declaration metadata required |
| IR generation | Not started | None | None | Readable machine-independent representation |
| Optimization | Not started | None | None | At least two independently testable passes |
| Target code generation | Not started | None | None | One documented target format |
| Mission VM | Not started | None | None | Simulated state and trace only |
| Error recovery | Planned | None | None | Recover at safe statement/block boundaries |
| Visualization | Planned | None | None | Text reports first; richer output optional |

## 18. Important Files

- `compiler_prd.md`: authoritative product requirements document.
- `context.md`: maintained project memory, status, decisions, assumptions, and activity log.

## 19. Agent Activity Log

- 2026-09-15: Audited the repository and found only `compiler_prd.md`.
- 2026-09-15: Confirmed Git branch `main` and Python 3.12.4 availability.
- 2026-09-15: Read the complete PRD and recorded explicit requirements, exclusions, ambiguities, architecture, and roadmap direction.
- 2026-09-15: Created the initial `context.md`; no compiler implementation was started.

## 20. Next Recommended Action

Resolve the parser and grammar questions, then create the project foundation (`README.md`, `pyproject.toml`, package skeleton, and test configuration) followed by a tested lexer slice. Do not begin semantic, IR, optimization, or VM work until the language subset and token contract are stable.

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