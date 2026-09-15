# AEGIS Architecture

This document describes the planned architecture. The project foundation, lexer, parser, and AST currently exist; semantic analysis and later compiler phases remain planned.

## Compiler Pipeline

```text
Source Code
    |
    v
Lexer
    |
    v
Parser
    |
    v
AST
    |
    v
Symbol Table and Semantic Analysis
    |
    v
Intermediate Representation
    |
    v
Optimizer
    |
    v
Target Code Generator
    |
    v
Mission Virtual Machine
    |
    v
Execution Trace and Diagnostics
```

## Module Responsibilities

- **Lexer:** Convert source text into positioned tokens and report invalid characters or literals.
- **Parser:** Use the provisional handwritten recursive-descent strategy to validate syntax and construct the AST.
- **AST:** Represent missions, blocks, commands, control flow, and expressions independently of grammar-only details, with source locations.
- **Symbol table:** Store declarations, types, scopes, locations, and mutability metadata.
- **Semantic analyzer:** Build mission/state symbols and validate conservative types, ranges, expression operands, conditions, repeat counts, and camera/image dependencies.
- **IR generator:** Translate the AST into readable machine-independent instructions, temporaries, and labels.
- **Optimizer:** Apply independently testable, semantics-preserving general and mission-specific transformations.
- **Code generator:** Lower optimized IR into one documented AEGIS target instruction format.
- **Mission VM:** Execute target instructions against simulated state and produce an execution trace.
- **Diagnostics:** Provide shared lexical, syntax, semantic, and runtime messages with source locations.
- **Visualization:** Initially expose readable text artifacts; richer Graphviz output is optional.
- **Pipeline coordinator:** Connect phases, preserve artifacts, and block execution when fatal diagnostics remain.
- **CLI:** Provide the user-facing command for source files, reports, and demonstrations.

## Design Principles

- **Modular compiler phases:** Each phase has a clear input and output.
- **Readable intermediate representations:** Artifacts should be explainable during a course demonstration.
- **Explainable implementation:** Prefer straightforward Python structures over opaque machinery.
- **Testability:** Major phases will receive focused unit tests and end-to-end integration tests.
- **Clear diagnostics:** Errors should identify their category and source location where available.
- **Simulation boundary:** The VM will operate only on synthetic state; no real spacecraft control or hardware integration is allowed.
- **Incremental implementation:** A small tested vertical slice is completed before adding the next phase.
- **PRD-driven development:** `compiler_prd.md` remains the requirements authority; proposals are labeled as provisional or future work.

## Current Foundation

The current package contains the project metadata, package initialization, pipeline placeholder, status/tokenize/parse CLI, tested lexer, parser, and AST. No semantic analyzer, symbol table, IR, optimizer, code generator, VM, or visualization implementation is present yet.

## Implemented Semantic Slice

The semantic layer contains a scoped `SymbolTable`, `Scope`, and `Symbol` model. The current grammar has no declarations, so analysis installs one mission symbol and predefined state symbols (`BATTERY`, `TEMPERATURE`, and `VISIBILITY`). Nested scopes are available for future declaration syntax but are not created by the current AST.

`SemanticAnalyzer` traverses the AST and emits positioned `SemanticDiagnostic` instances. It checks expression types, numeric command arguments, constant ranges, boolean conditions, bounded repetition, undefined identifiers, and camera/image operation dependencies. It does not generate IR, optimize, generate target code, or execute a VM.
