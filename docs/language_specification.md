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

The command and control-flow syntax is implemented incrementally. The lexer and the initial parser now recognize the active syntax described here; semantic analysis and later compiler phases do not exist yet.

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

## Active Grammar

The parser currently implements this grammar shape:

```text
program       := MISSION IDENTIFIER block EOF
block         := "{" statement* "}"
statement     := power | move | camera | capture | transmit | wait
               | safe_mode | if_statement | repeat_statement
power         := POWER expression ";"
move          := MOVE expression ";"
camera        := CAMERA (ON | OFF) ";"
capture       := CAPTURE IMAGE ";"
transmit      := TRANSMIT IMAGE ";"
wait          := WAIT expression ";"
safe_mode     := SAFE_MODE ";"
if_statement  := IF expression block (ELSE block)?
repeat_statement := REPEAT expression block
```

Expressions use the following precedence, from lowest to highest:

```text
equality -> relational -> additive -> multiplicative -> unary -> primary
```

Primary expressions include numbers, strings, booleans, identifiers, and parenthesized expressions. `END` is not part of this grammar; its lexer token is rejected by the parser.

## Semantic Rules Currently Implemented

The current semantic phase uses a small conservative type model: `integer`, `decimal`, `number`, `string`, `boolean`, and `unknown`. The grammar has no declaration syntax, so the analyzer does not invent variables or user-defined types. It provides these predefined numeric/boolean state identifiers: `BATTERY`, `TEMPERATURE`, and `VISIBILITY`.

Implemented checks include:

- Numeric arguments for `POWER`, `MOVE`, and `WAIT`.
- `POWER` constants between `0` and `100`.
- Nonnegative constant movement and wait values.
- Integer `REPEAT` counts between `0` and `1000`.
- Boolean `IF` conditions.
- Numeric arithmetic and relational operands.
- Compatible equality operands.
- Undefined identifier references.
- Camera-on requirement for `CAPTURE IMAGE`.
- Captured-image requirement for `TRANSMIT IMAGE`.

These checks are static analysis only. They do not execute commands or simulate spacecraft state.

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

This is accepted by the lexer, parser, semantic analyzer, and IR generator. It is not executed.

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

The lexer, parser, AST, semantic analyzer, and structured IR are implemented and tested. IR is not optimized or executed. Exact declarations, type annotations, sensor reads, safe-mode restrictions, and runtime state transitions remain unspecified.

## Future Enhancements

Future work may add variables and declarations, richer data types, sensor expressions, detailed resource modeling, scheduling, fault injection, advanced optimization, bytecode serialization, and interactive visualization. These are not part of the current foundation.
