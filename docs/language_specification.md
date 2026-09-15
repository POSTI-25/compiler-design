# AEGIS Initial Language Specification

This document records the initial language subset selected for implementation. It is intentionally small and is not a claim that the entire language has been finalized.

## Purpose

AEGIS is a readable domain-specific language for describing high-level spacecraft mission actions in a simulated environment. It is an academic compiler language, not a spacecraft flight-control language.

## Approved Initial Features

The first language slice includes:

- A `MISSION` declaration with an identifier name.
- Braced mission blocks.
- Semicolon-terminated statements.
- `POWER` commands.
- `MOVE` commands.
- `CAMERA ON` and `CAMERA OFF` commands.
- `CAPTURE IMAGE` and `TRANSMIT IMAGE` commands.
- `WAIT` and `SAFE_MODE` commands.
- The planned `IF`, `ELSE`, and bounded `REPEAT` constructs.
- Numeric literals.
- Boolean conditions for control flow.
- Comments and whitespace.

The command and control-flow syntax will be implemented incrementally. At this foundation stage, this document defines the intended subset but no lexer or parser exists yet.

## Mission Declaration

The provisional form is:

```aegis
MISSION observation {
    POWER 80;
}
```

The mission name is an identifier. A mission body is enclosed in `{` and `}`. Braces are the selected initial block style; `END` is not mixed into the same initial syntax.

## Supported Commands

The intended command forms are:

```aegis
POWER 80;
MOVE 10;
CAMERA ON;
CAMERA OFF;
CAPTURE IMAGE;
TRANSMIT IMAGE;
WAIT 5;
SAFE_MODE;
```

Exact argument rules for `WAIT`, `SAFE_MODE`, and later expressions remain provisional and will be defined before implementation of those constructs.

## Control Flow

The planned block forms are:

```aegis
IF battery < 30 {
    SAFE_MODE;
} ELSE {
    WAIT 5;
}

REPEAT 3 {
    MOVE 10;
}
```

The exact sensor/state expression syntax, declaration syntax, and repetition bound are still open. No `END`-based form will be supported in the initial syntax unless this decision is revisited explicitly.

## Literals and Conditions

Numeric literals are required for command arguments and may include integers and decimals as supported by the eventual lexer. String literals are not needed by the currently selected command examples and are deferred unless a concrete initial command requires them.

Conditions are intended to evaluate to booleans and may use comparisons such as `<`, `>`, `==`, `!=`, `<=`, and `>=`. Boolean literals and variable/state references remain provisional until the expression subset is finalized.

## Comments and Whitespace

Whitespace is insignificant except for separating tokens. The initial comment syntax is provisionally `//` through the end of a line. Block comments are deferred.

## Case Sensitivity

The language is provisionally case-sensitive. Keywords and commands will be written in uppercase, while mission names and identifiers follow identifier rules. This keeps the grammar explicit and diagnostics predictable.

## Valid Example

```aegis
MISSION observation {
    POWER 80;
    CAMERA ON;
    CAPTURE IMAGE;
    CAMERA OFF;
    TRANSMIT IMAGE;
}
```

This is a future compiler input example only; the compiler pipeline is not implemented yet.

## Invalid Examples

These examples are structurally invalid for the selected initial style:

```aegis
MISSION observation
    POWER 80;
}
```

```aegis
MISSION observation {
    POWER 80
}
```

The first omits the opening brace. The second omits the statement semicolon. Semantic invalidity, such as `POWER 140`, will be defined by the semantic phase rather than the foundation CLI.

## Provisional Decisions

- Handwritten recursive-descent parsing is selected for the first version instead of ANTLR4.
- Braces are the initial block delimiters; `END` is not combined with braces.
- The language is case-sensitive.
- The first implementation will prioritize the command subset above before variables and richer expressions.

## Current Limitations

No lexer, parser, AST, semantic analyzer, symbol table, IR, optimizer, code generator, or VM has been implemented. Exact declarations, types, sensor reads, safe-mode restrictions, and runtime state transitions remain unspecified.

## Future Enhancements

Future work may add variables and declarations, richer data types, sensor expressions, detailed resource modeling, scheduling, fault injection, advanced optimization, bytecode serialization, and interactive visualization. These are not part of the current foundation.
