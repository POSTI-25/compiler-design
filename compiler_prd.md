# AEGIS

## A Product Requirements Document for a Domain-Specific Language and Compiler for Autonomous Spacecraft Missions

**Course:** Compiler Design (BCSE307P)  
**Institution:** Vellore Institute of Technology, Vellore  
**Project Phase:** Core Implementation and Functional Prototype  

---

## 1. Abstract

Aegis is a domain-specific language (DSL) and compiler for autonomous spacecraft and satellite mission scripts. The system is designed to allow mission engineers to express high-level mission operations through readable commands such as power management, movement, camera operations, image capture, communication, waiting, and conditional execution.

The proposed system will implement the major phases of compiler construction: lexical analysis, syntax analysis, abstract syntax tree construction, semantic analysis, symbol table management, intermediate code generation, code optimization, target code generation, and interpretation on a simulated mission virtual machine. The system will also provide error detection and recovery for lexical, syntax, semantic, and runtime errors.

Aegis focuses on high-level mission logic that can be validated and executed in a simulated environment when ground contact is delayed or unavailable. It does not attempt to implement actual spacecraft flight software, hardware drivers, real telemetry systems, or detailed physical simulation. Instead, it provides a controlled and explainable compiler-design prototype that demonstrates how domain-specific language features can be integrated with traditional compiler techniques.

The product will be developed as a modular command-line application, with optional visualization support for tokens, parse trees, abstract syntax trees, intermediate representation, optimization results, and simulated execution. The final prototype will demonstrate an end-to-end workflow from source code to executable mission instructions and simulated spacecraft output.

---

## 2. Problem Statement

Space missions increasingly require spacecraft and satellites to perform complex operations autonomously, especially when communication with ground stations is delayed, intermittent, or temporarily unavailable. Mission instructions must therefore be expressed clearly, validated before execution, and translated into a form that can be executed reliably by an onboard or simulated execution environment.

Traditional general-purpose programming languages do not directly express spacecraft mission concepts such as power levels, camera states, image capture, communication operations, movement, safety modes, or mission-specific resource conditions. As a result, high-level mission logic may require additional translation layers, custom command systems, or low-level implementation details.

The problem addressed by Aegis is:

> How can a domain-specific compiler translate high-level spacecraft mission commands into valid, optimized, and executable instructions for a simulated mission environment while detecting and explaining errors at different stages of compilation?

The system must ensure that a mission script is:

- Lexically valid.
- Syntactically valid.
- Semantically meaningful.
- Consistent with the defined mission rules.
- Translated into an intermediate representation.
- Optimized using general and mission-specific rules.
- Converted into executable instructions or bytecode.
- Executed safely within a simulated mission virtual machine.
- Accompanied by clear diagnostic messages when errors occur.

Aegis will address this problem by combining a custom spacecraft-oriented language with a complete compiler pipeline and a simulated execution environment.

---

## 3. Motivation

Several factors motivate the development of Aegis.

First, reliability and safety are important in spacecraft operations. A mission script containing invalid commands, incorrect types, impossible resource values, or invalid operation sequences should be detected before execution. A compiler with semantic validation can identify such issues early and provide useful diagnostics.

Second, autonomy is increasingly important for spacecraft and satellite missions. When communication with the ground station is delayed or unavailable, a spacecraft may need to execute a previously prepared sequence of operations without continuous human intervention. Aegis models this requirement through a mission language that can be compiled and executed independently in a simulated environment.

Third, spacecraft systems operate under limited resources. Even though Aegis does not implement detailed physical or hardware-level simulation, it can demonstrate resource-aware language rules and mission-specific optimizations. Examples include removing redundant camera operations, folding constant expressions, combining consecutive movement commands, and eliminating unreachable code.

Fourth, domain-specific languages improve expressiveness by allowing users to work with concepts directly related to their problem domain. In Aegis, mission engineers can write commands such as `POWER 80`, `CAMERA ON`, `CAPTURE IMAGE`, and `TRANSMIT IMAGE` instead of expressing every operation through general-purpose programming constructs.

Finally, Aegis provides a practical way to demonstrate the concepts covered in a compiler-design course. The project connects theoretical topics such as tokenization, parsing, abstract syntax trees, semantic analysis, symbol tables, intermediate code, optimization, code generation, interpretation, and error recovery into one working system.

---

## 4. Product Vision

The vision of Aegis is to create a readable, modular, and explainable spacecraft mission compiler that demonstrates the complete transformation of high-level mission scripts into executable instructions for a simulated spacecraft environment.

The product will act as a bridge between:

- Human-readable mission commands.
- Formal language grammar.
- Compiler analysis and validation.
- Intermediate representations.
- Optimized target instructions.
- Simulated spacecraft execution.

The product will prioritize correctness, transparency, modularity, and educational value rather than industrial-grade spacecraft deployment.

---

## 5. Objectives

The primary objectives of Aegis are:

- **Design a domain-specific language.** Define a readable syntax for spacecraft mission commands, expressions, variables, and control flow.

- **Implement lexical analysis.** Recognize keywords, identifiers, numbers, strings, operators, punctuation, comments, and invalid characters.

- **Implement syntax analysis.** Process the token stream using a formal grammar and construct a parse tree or abstract syntax tree.

- **Construct an abstract syntax tree.** Represent the logical structure of a mission script independently of unnecessary grammar details.

- **Implement semantic analysis.** Validate data types, declarations, command arguments, operation order, resource rules, and mission-specific constraints.

- **Implement symbol table management.** Store and retrieve variables, constants, resource names, types, scopes, and related attributes.

- **Generate intermediate code.** Translate the AST into a machine-independent representation such as three-address code or quadruples.

- **Implement code optimization.** Apply general optimizations such as constant folding and dead code elimination, along with mission-specific optimizations such as merging consecutive movement commands and removing redundant camera toggles.

- **Generate target code.** Translate optimized intermediate code into a documented instruction set or bytecode for the simulated mission virtual machine.

- **Implement an interpreter or virtual machine.** Execute the generated instructions and update a simulated spacecraft state.

- **Implement error detection and recovery.** Detect lexical, syntax, semantic, and runtime errors, report them with line and column information where possible, and continue compilation when safe.

- **Provide compiler visualization.** Display or export tokens, parse trees, ASTs, intermediate code, optimization changes, target instructions, and execution traces.

- **Deliver a functional prototype.** Demonstrate successful compilation, error reporting, optimization, and simulated execution using representative mission scripts.

---

## 6. Scope

### 6.1 Included

The project focuses on high-level mission logic compilation for a simplified spacecraft or satellite environment.

The included functionality is:

- A custom spacecraft mission DSL.
- Mission declaration and mission naming.
- Basic spacecraft commands.
- Numeric and boolean expressions.
- Variables and constants where supported by the language version.
- Conditional control flow.
- Bounded repetition.
- Lexical analysis.
- Syntax analysis.
- AST construction.
- Semantic analysis.
- Symbol table management.
- Intermediate representation generation.
- Basic and mission-specific optimization.
- Target instruction or bytecode generation.
- A simulated mission virtual machine.
- Runtime state tracking.
- Error detection and recovery.
- Unit and integration tests.
- Command-line demonstration.
- Optional compiler-stage visualization.

The initial command set will include:

- `POWER`
- `MOVE`
- `CAMERA ON`
- `CAMERA OFF`
- `CAPTURE IMAGE`
- `TRANSMIT IMAGE`
- `WAIT`
- `SAFE_MODE`

The initial sensor and state concepts may include:

- `BATTERY`
- `TEMPERATURE`
- `VISIBILITY`
- Camera state.
- Captured-image state.
- Simulated movement distance.
- Communication state.
- Safe-mode state.

The initial control-flow constructs will include:

- `IF`
- `ELSE`
- `END`
- Bounded `REPEAT`

### 6.2 Excluded

The following are outside the scope of the project:

- Actual spacecraft flight software.
- Direct control of spacecraft hardware.
- Low-level hardware drivers.
- Real-time operating-system implementation.
- Real spacecraft networking.
- Actual telemetry ingestion.
- Real command uplink or downlink.
- Detailed orbital mechanics.
- High-fidelity spacecraft physics.
- Advanced mission planning.
- Autonomous path planning.
- Fault-tolerant flight certification.
- Multiple hardware target architectures.
- Industrial-grade compiler performance.
- Deployment on an actual spacecraft or satellite.

### 6.3 Limitations

The project will target a single custom instruction set or bytecode format for the simulated mission virtual machine. Multiple target architectures will not be supported.

The simulator will use simplified state transitions rather than detailed physical models. Resource values and mission conditions will be represented through predefined rules and synthetic values.

The product will be a proof-of-concept intended for academic demonstration. It must not be presented as flight-qualified software or as a replacement for certified spacecraft command and control systems.

---

## 7. Target Users

### 7.1 Primary Users

The primary users are:

- Compiler-design students.
- Mission-language designers.
- Students studying domain-specific languages.
- Students studying interpreters and virtual machines.
- Instructors evaluating compiler-design projects.

### 7.2 Secondary Users

Secondary users may include:

- Students interested in space systems.
- Researchers exploring educational mission languages.
- Developers experimenting with compiler visualization.
- Users who want to write and simulate simple spacecraft mission sequences.

The system is not intended for direct use by spacecraft operators in real missions.

---

## 8. User Stories

- As a user, I want to write a mission script using readable spacecraft commands so that I can express mission operations without using a general-purpose language.

- As a user, I want the compiler to identify invalid characters and malformed tokens so that lexical mistakes can be corrected.

- As a user, I want syntax errors to be reported with line information so that I can correct the structure of my mission script.

- As a user, I want the compiler to build an AST so that the logical structure of my program can be inspected.

- As a user, I want semantic errors to be detected before execution so that invalid mission operations are not executed.

- As a user, I want variables and resources to be stored in a symbol table so that declarations and references can be checked.

- As a user, I want to view intermediate code so that I can understand how high-level mission commands are translated.

- As a user, I want the compiler to optimize redundant or constant operations so that the generated mission instructions are simpler.

- As a user, I want to execute the compiled program in a simulated mission VM so that I can observe the effect of each instruction.

- As a user, I want multiple errors to be reported in one compilation attempt whenever recovery is safe so that debugging is faster.

- As a user, I want test cases for successful and faulty scripts so that the correctness of each compiler phase can be demonstrated.

- As an evaluator, I want the project to show intermediate results and module-wise explanations so that the implementation progress can be assessed.

---

## 9. Functional Requirements

### 9.1 Source Input

The system shall:

- Accept a mission source file as input.
- Accept a source string through a programmatic API where practical.
- Support a defined file extension such as `.aegis`.
- Preserve line and column information.
- Reject empty or structurally invalid mission files with a meaningful diagnostic.

### 9.2 Language Specification

The language shall define:

- Keywords.
- Identifiers.
- Numeric literals.
- String literals where required.
- Boolean literals.
- Operators.
- Delimiters.
- Comments.
- Whitespace rules.
- Statement termination rules.
- Block structure.
- Expression precedence.
- Valid command forms.
- Type rules.
- Domain-specific semantic rules.

The initial syntax shall remain small enough to be implemented and tested during the course project.

### 9.3 Lexical Analysis

The lexer shall:

- Recognize keywords such as `MISSION`, `POWER`, `MOVE`, `CAMERA`, `ON`, `OFF`, `CAPTURE`, `TRANSMIT`, `IMAGE`, `WAIT`, `SAFE_MODE`, `IF`, `ELSE`, `END`, and `REPEAT`.
- Recognize identifiers.
- Recognize integer and decimal numbers where supported.
- Recognize strings.
- Recognize operators such as `+`, `-`, `*`, `/`, `<`, `>`, `==`, `!=`, `<=`, and `>=`.
- Recognize punctuation such as braces, parentheses, semicolons, and commas where used.
- Ignore defined whitespace and comments.
- Report invalid characters.
- Produce a token stream suitable for the parser.
- Include token type, token value, line, and column information.

### 9.4 Syntax Analysis

The parser shall:

- Consume the token stream.
- Validate the source against the language grammar.
- Recognize mission declarations.
- Recognize valid command statements.
- Recognize expressions.
- Recognize conditional blocks.
- Recognize bounded repetition blocks.
- Construct a parse tree or directly construct an AST.
- Report syntax errors with useful context.
- Attempt recovery at statement or block boundaries where possible.

### 9.5 Abstract Syntax Tree

The AST shall:

- Represent the logical structure of a mission program.
- Contain nodes for mission declarations.
- Contain nodes for command statements.
- Contain nodes for expressions.
- Contain nodes for conditional statements.
- Contain nodes for repetition statements.
- Preserve source location information where practical.
- Support traversal by visitors or equivalent mechanisms.
- Support serialization or readable printing.
- Support visualization through a tree representation or Graphviz output.

### 9.6 Semantic Analysis

The semantic analyzer shall:

- Check whether identifiers are declared before use.
- Check whether identifiers are declared more than once in the same scope when redeclaration is not allowed.
- Check command argument types.
- Check numeric ranges.
- Check boolean conditions.
- Check valid command sequences.
- Check whether an image exists before transmission.
- Check whether the camera is enabled before image capture.
- Check whether movement values are numeric and nonnegative.
- Check whether power values are within the defined range.
- Check whether repetition counts are valid and bounded.
- Check whether mission declarations are valid.
- Report semantic errors without executing invalid programs.

### 9.7 Symbol Table

The symbol table shall:

- Support insertion.
- Support lookup.
- Support update where permitted.
- Track identifier names.
- Track data types.
- Track scope.
- Track declaration location.
- Track constant or mutable status where applicable.
- Provide useful information to semantic analysis and later compiler stages.
- Support future extension to mission resources such as images and sensor values.

### 9.8 Intermediate Representation

The IR generator shall:

- Traverse the AST.
- Produce machine-independent instructions.
- Represent commands and expressions.
- Represent temporary values.
- Represent labels.
- Represent conditional jumps.
- Represent unconditional jumps.
- Represent repetition control flow.
- Use a documented representation such as three-address code, quadruples, or a structured instruction list.
- Preserve enough information for optimization and code generation.

Example IR instructions may include:

```text
POWER 80
CAMERA_ON
CAPTURE_IMAGE
CAMERA_OFF
TRANSMIT_IMAGE
```

For conditional logic, the IR may include:

```text
t1 = BATTERY < 30
JUMP_IF_FALSE t1, L1
MOVE 10
LABEL L1
```

### 9.9 Code Optimization

The optimizer shall implement at least two documented optimization rules.

The initial optimization rules may include:

- Constant folding.
- Dead code elimination.
- Removal of unreachable conditional branches.
- Removal of redundant consecutive `CAMERA ON` commands.
- Removal of redundant consecutive `CAMERA OFF` commands.
- Merging consecutive `MOVE` commands where semantics permit.
- Elimination of redundant state transitions.
- Simplification of constant boolean conditions.

Each optimization pass shall:

- Receive a valid IR.
- Produce semantically equivalent IR.
- Record or expose the transformation where practical.
- Be independently testable.
- Avoid changing the meaning of valid mission programs.

### 9.10 Target Code Generation

The code generator shall:

- Translate optimized IR into a custom target instruction set or bytecode.
- Use a documented instruction format.
- Represent commands such as `POWER`, `MOVE`, `CAMERA_ON`, `CAMERA_OFF`, `CAPTURE_IMAGE`, `TRANSMIT_IMAGE`, `WAIT`, and control-flow operations.
- Generate labels or resolved jump targets.
- Produce output that can be consumed by the mission VM.
- Optionally export target code to a file.
- Provide readable target instructions for demonstration.

### 9.11 Interpreter and Mission Virtual Machine

The mission VM shall:

- Load generated target instructions.
- Execute instructions sequentially.
- Maintain a program counter.
- Maintain a runtime environment.
- Maintain simulated spacecraft state.
- Execute arithmetic and comparison operations.
- Support conditional and unconditional jumps.
- Support bounded repetition after compilation.
- Update battery or other simplified state values where defined.
- Track camera state.
- Track image-capture state.
- Track movement distance.
- Track communication events.
- Support safe-mode state.
- Produce an execution trace.
- Detect runtime errors.
- Stop safely when an unrecoverable runtime error occurs.

### 9.12 Error Handling and Recovery

The compiler shall distinguish between:

- Lexical errors.
- Syntax errors.
- Semantic errors.
- Runtime errors.

Each diagnostic should include, where available:

- Error category.
- Message.
- Line number.
- Column number.
- Relevant token or command.
- Suggested correction or contextual explanation.

The compiler should continue after recoverable errors, especially at statement boundaries, so that multiple errors can be reported in one run.

The system shall not execute a program when compilation has unresolved fatal errors.

### 9.13 Visualization and Reporting

The system should provide optional outputs for:

- Token stream.
- Parse tree.
- AST.
- Symbol table.
- Semantic diagnostics.
- Raw IR.
- Optimized IR.
- Target instructions.
- Runtime execution trace.
- Final simulated spacecraft state.

Visualization may be implemented using text output initially and Graphviz or another visualization library later.

---

## 10. Non-Functional Requirements

### 10.1 Correctness

The compiler shall produce correct diagnostics for supported invalid programs and correct execution results for supported valid programs.

### 10.2 Modularity

Each compiler phase shall be implemented as a separate module with clear inputs and outputs.

### 10.3 Explainability

The system shall expose intermediate results so that the compiler pipeline can be demonstrated and understood.

### 10.4 Maintainability

The codebase shall use meaningful names, clear module boundaries, documentation, and consistent error-handling conventions.

### 10.5 Testability

Each major module shall have unit tests. The complete pipeline shall have integration tests.

### 10.6 Portability

The command-line application should run on a modern Windows or Linux system using the selected Python runtime and dependencies.

### 10.7 Performance

The prototype should process small and medium-sized mission scripts without noticeable delay. Industrial-scale performance is not required.

### 10.8 Safety of Simulation

The VM shall operate only on simulated state. It shall not access real spacecraft hardware, real telemetry, external control systems, or live communication channels.

---

## 11. Proposed Language Specification

### 11.1 Example Mission Structure

```aegis
MISSION observation {
    POWER 80;
    CAMERA ON;
    CAPTURE IMAGE;
    CAMERA OFF;
    TRANSMIT IMAGE;
}
```

### 11.2 Faulty Mission Example

```aegis
MISSION faulty {
    MOVE "ten";
    TRANSMIT IMAGE;
    CAMERA OFF;
    CAPTURE IMAGE;
    UNKNOWN_COMMAND;
    POWER 140;
}
```

Expected issues include:

- Invalid type for `MOVE`.
- Image transmission before a valid image is captured.
- Invalid camera and capture sequence.
- Unknown command.
- Power value outside the valid range.

### 11.3 Optimization Example

```aegis
MISSION optimized {
    POWER 40 + 40;
    CAMERA ON;
    CAMERA ON;
    MOVE 10;
    MOVE 20;
    IF 1 == 0 {
        MOVE 100;
    }
}
```

Possible optimization results include:

- Folding `40 + 40` into `80`.
- Removing the redundant second `CAMERA ON`.
- Merging `MOVE 10` and `MOVE 20` where permitted.
- Removing the unreachable conditional body.

### 11.4 Initial Data Types

The initial type system may include:

- `number`
- `percentage`
- `boolean`
- `image`
- `status`
- `duration`

The exact syntax for declarations and type annotations will be finalized during language-specification implementation.

### 11.5 Initial Domain Rules

The initial domain rules shall include:

- Battery and power percentages must remain within the range `0` to `100`.
- Movement distance must be numeric and nonnegative.
- Camera capture requires the camera to be on.
- Image transmission requires a captured image.
- Safe mode disables or restricts noncritical operations in the simulator.
- Repetition counts must be numeric, nonnegative, and bounded.
- Conditions must evaluate to boolean values.
- Mission names must be valid identifiers.
- Unsupported commands must be rejected.

---

## 12. System Architecture

The system will follow a modular front-end and back-end architecture.

```text
Mission Source Code
        |
        v
Lexer
        |
        v
Token Stream
        |
        v
Parser
        |
        v
Parse Tree / AST
        |
        v
Symbol Table + Semantic Analyzer
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
Mission Bytecode / Instructions
        |
        v
Mission Virtual Machine
        |
        v
Simulated Spacecraft State
        |
        v
Execution Trace + Output
```

### 12.1 Lexer Module

The lexer converts source text into tokens. It is responsible for keyword recognition, identifier recognition, literal recognition, operator recognition, punctuation recognition, comment handling, and lexical diagnostics.

### 12.2 Parser Module

The parser consumes tokens and validates the source against the grammar. It produces a parse tree or AST and reports syntax errors.

### 12.3 AST Module

The AST module defines node classes and traversal mechanisms. It removes unnecessary grammar details while preserving the logical structure of the mission program.

### 12.4 Symbol Table Module

The symbol table stores declarations, types, scope information, and resource metadata. It is used by semantic analysis and may also support later code-generation stages.

### 12.5 Semantic Analyzer Module

The semantic analyzer traverses the AST and checks type rules, declaration rules, command constraints, resource dependencies, and mission-specific semantics.

### 12.6 IR Generator Module

The IR generator converts AST nodes into a machine-independent instruction sequence with temporary values, labels, and control-flow operations.

### 12.7 Optimizer Module

The optimizer applies documented transformations to the IR. It should expose both the original and optimized representations for comparison.

### 12.8 Code Generator Module

The code generator converts optimized IR into the instruction set supported by the mission VM.

### 12.9 Runtime and Simulator Module

The runtime loads and executes target instructions. It updates the simulated spacecraft state and produces an execution trace.

### 12.10 Diagnostics Module

The diagnostics module provides a common representation for errors and warnings from all compiler stages.

### 12.11 Visualization Module

The visualization module displays or exports compiler artifacts such as tokens, ASTs, IR, and execution traces.

---

## 13. Technology Stack

The initial technology stack will be:

- **Implementation Language:** Python 3.x.
- **Parser Generator:** ANTLR4 is the preferred option.
- **Alternative Parser Approach:** A manually implemented recursive-descent parser may be used if it provides better control for the educational prototype.
- **Intermediate Representation:** Custom Python data structures representing three-address code or structured instructions.
- **Target Code:** Custom mission bytecode or assembly-like instruction text.
- **Execution Engine:** Custom Python interpreter or mission virtual machine.
- **Testing:** `pytest` or Python `unittest`.
- **Visualization:** Graphviz and/or text-based visualization.
- **Development Environment:** Visual Studio Code or PyCharm.
- **Version Control:** Git.
- **Operating Systems:** Windows and Linux.
- **Optional Future Backend:** LLVM or `llvmlite`, only if the core compiler pipeline is already stable.

LLVM will not be a mandatory dependency for the initial prototype. A custom IR and interpreter are preferred initially because they provide better control over the educational objectives and reduce unnecessary implementation complexity.

---

## 14. Project Structure

The implementation should follow a modular structure similar to:

```text
aegis/
│
├── README.md
├── requirements.txt
├── pyproject.toml
├── grammar/
│   └── Aegis.g4
│
├── src/
│   └── aegis/
│       ├── __init__.py
│       ├── lexer/
│       ├── parser/
│       ├── ast/
│       ├── semantic/
│       ├── symbols/
│       ├── ir/
│       ├── optimizer/
│       ├── codegen/
│       ├── runtime/
│       ├── diagnostics/
│       ├── visualization/
│       └── cli.py
│
├── examples/
│   ├── observation.aegis
│   ├── faulty.aegis
│   └── optimized.aegis
│
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_ast.py
│   ├── test_semantic.py
│   ├── test_symbol_table.py
│   ├── test_ir.py
│   ├── test_optimizer.py
│   ├── test_codegen.py
│   ├── test_runtime.py
│   └── test_integration.py
│
└── docs/
    ├── language_specification.md
    ├── grammar.md
    ├── architecture.md
    ├── ir_specification.md
    ├── bytecode_specification.md
    └── testing_report.md
```

The exact structure may be adjusted during implementation, but compiler phases must remain clearly separated.

---

## 15. Phase 2 Implementation Plan

### 15.1 Stage 1: Project Foundation

Deliverables:

- Project repository.
- Python environment.
- Dependency configuration.
- Basic command-line entry point.
- Initial README.
- Example source files.
- Test framework setup.

Acceptance criteria:

- The project runs locally.
- A sample command can be executed from the command line.
- Tests can be discovered and executed.

### 15.2 Stage 2: Lexical Analysis

Deliverables:

- Token definitions.
- Lexer implementation or generated lexer.
- Token stream output.
- Lexical error reporting.
- Lexer unit tests.

Acceptance criteria:

- Keywords, identifiers, literals, operators, and punctuation are recognized.
- Invalid characters produce diagnostics.
- Line and column information is preserved.
- Valid sample scripts produce the expected token stream.

### 15.3 Stage 3: Syntax Analysis

Deliverables:

- Grammar file or parser implementation.
- Parser module.
- Parse tree or AST construction entry point.
- Syntax error handling.
- Parser unit tests.

Acceptance criteria:

- Valid mission scripts parse successfully.
- Invalid command structures are rejected.
- Missing delimiters and malformed expressions produce useful diagnostics.
- Recoverable syntax errors do not necessarily stop all further analysis.

### 15.4 Stage 4: AST and Symbol Table

Deliverables:

- AST node definitions.
- AST traversal support.
- Symbol table implementation.
- AST printing or visualization.
- Symbol table tests.

Acceptance criteria:

- The AST represents mission structure correctly.
- Symbols can be inserted and looked up.
- Scope and type information are stored.
- AST output is understandable during demonstration.

### 15.5 Stage 5: Semantic Analysis

Deliverables:

- Semantic analyzer.
- Type checking.
- Declaration checking.
- Mission-specific validation rules.
- Semantic diagnostic reporting.
- Semantic analysis tests.

Acceptance criteria:

- Invalid command arguments are detected.
- Invalid operation sequences are detected.
- Invalid power and movement values are detected.
- Multiple semantic errors can be reported where possible.
- Invalid programs are prevented from reaching execution.

### 15.6 Stage 6: Intermediate Representation

Deliverables:

- IR instruction definitions.
- AST-to-IR generator.
- Label and temporary management.
- IR printer.
- IR tests.

Acceptance criteria:

- Basic commands produce valid IR.
- Expressions produce appropriate intermediate instructions.
- Conditional and repetition constructs produce control-flow instructions.
- IR is independent of the final VM instruction format.

### 15.7 Stage 7: Optimization

Deliverables:

- Optimization pass framework.
- At least two optimization passes.
- Before-and-after IR output.
- Optimization tests.

Acceptance criteria:

- Constant folding works.
- Dead code or unreachable branch elimination works.
- At least one mission-specific optimization works.
- Optimized IR preserves program meaning for supported programs.

### 15.8 Stage 8: Target Code and Mission VM

Deliverables:

- Target instruction-set specification.
- Code generator.
- Mission VM.
- Runtime state model.
- Execution trace.
- Runtime tests.

Acceptance criteria:

- Optimized IR is converted into target instructions.
- Target instructions can be executed by the VM.
- The VM updates simulated spacecraft state.
- Valid mission scripts produce expected output.
- Runtime errors are reported clearly.

### 15.9 Stage 9: Integration and Demonstration

Deliverables:

- End-to-end compiler command.
- Successful mission demonstration.
- Faulty mission demonstration.
- Optimization demonstration.
- Test report.
- Module-wise explanation.
- Implementation progress report.

Acceptance criteria:

- Source code can be compiled through all implemented stages.
- Intermediate results can be displayed.
- Successful missions execute correctly.
- Faulty missions produce useful diagnostics.
- The demonstration clearly maps implementation modules to Phase 2 requirements.

---

## 16. Testing Requirements

Testing shall be performed at both module and system levels.

### 16.1 Lexer Tests

Test cases shall include:

- Valid keywords.
- Valid identifiers.
- Integer and decimal literals.
- Operators.
- Punctuation.
- Comments.
- Invalid characters.
- Incorrect literal formats.

### 16.2 Parser Tests

Test cases shall include:

- Valid mission declarations.
- Valid command sequences.
- Valid expressions.
- Valid conditional blocks.
- Valid repetition blocks.
- Missing semicolons.
- Missing braces.
- Unexpected tokens.
- Invalid command structure.

### 16.3 Semantic Tests

Test cases shall include:

- Undeclared identifier.
- Duplicate declaration.
- Invalid type passed to `MOVE`.
- Invalid power range.
- Negative movement.
- Image transmission before capture.
- Capture when the camera is off.
- Invalid repetition count.
- Non-boolean condition.
- Unknown command.

### 16.4 IR Tests

Test cases shall verify:

- Basic command translation.
- Expression translation.
- Temporary generation.
- Label generation.
- Conditional jumps.
- Repetition control flow.

### 16.5 Optimization Tests

Test cases shall verify:

- Constant folding.
- Dead code elimination.
- Redundant camera command removal.
- Consecutive movement merging where supported.
- Preservation of program meaning.

### 16.6 Runtime Tests

Test cases shall verify:

- Power updates.
- Movement updates.
- Camera state transitions.
- Image capture.
- Image transmission.
- Wait behavior.
- Safe-mode behavior.
- Conditional execution.
- Runtime error handling.

### 16.7 Integration Tests

Integration tests shall include:

- A valid observation mission.
- A faulty mission with multiple errors.
- An optimization-focused mission.
- A mission containing conditional execution.
- A mission containing bounded repetition.
- A complete source-to-execution workflow.

---

## 17. Error and Diagnostic Requirements

Diagnostics should follow a consistent structure:

```text
[ERROR] <category> at line <line>, column <column>:
<message>
```

Example:

```text
[SEMANTIC ERROR] at line 4, column 5:
Cannot transmit IMAGE because no image has been captured.
```

The compiler should distinguish between:

- Errors that allow continued analysis.
- Errors that prevent later compiler phases.
- Warnings that do not prevent compilation.
- Runtime failures that occur only during simulated execution.

The system must not hide errors, silently skip invalid commands, or execute a program that contains unresolved fatal semantic errors.

---

## 18. Demonstration Requirements

The final demonstration shall include at least three scripts.

### 18.1 Successful Compilation

The successful script shall demonstrate:

- Lexical analysis.
- Parsing.
- AST construction.
- Semantic validation.
- IR generation.
- Target code generation.
- VM execution.
- Final simulated state.

### 18.2 Fault Detection

The faulty script shall demonstrate:

- At least one lexical, syntax, or semantic error.
- Clear diagnostic output.
- Line information.
- Recovery or continued reporting where possible.
- Prevention of unsafe execution.

### 18.3 Optimization

The optimization script shall demonstrate:

- Constant folding.
- Removal of redundant commands.
- Dead code elimination or unreachable branch removal.
- A comparison between original and optimized IR.

### 18.4 Visual Demonstration

Where implemented, the demonstration should show:

- Token stream.
- AST or parse tree.
- Symbol table.
- IR before optimization.
- IR after optimization.
- Target instructions.
- Runtime execution trace.

---

## 19. Originality and Academic Positioning

Aegis should be presented as an original academic implementation and integration of compiler concepts for a spacecraft-mission domain. The project must not claim that the general idea of spacecraft command languages, mission scripting, or domain-specific compilers is entirely new.

The originality of the prototype will be demonstrated through:

- A custom and clearly documented mission DSL.
- Mission-specific semantic rules.
- Compile-time validation of operation dependencies.
- Explainable intermediate compiler artifacts.
- Mission-specific optimization passes.
- A custom mission instruction set.
- A simulated spacecraft virtual machine.
- An end-to-end educational compiler workflow.

The project will distinguish between:

- Existing compiler concepts.
- Existing spacecraft command-language ideas.
- Features implemented directly in Aegis.
- Features simplified for academic demonstration.
- Future features that are not part of the current prototype.

---

## 20. Success Criteria

The project will be considered successful when:

- A valid Aegis mission script can be tokenized.
- The script can be parsed using the defined grammar.
- An AST can be constructed and inspected.
- A symbol table can store and retrieve relevant information.
- Semantic rules can detect invalid mission operations.
- Intermediate code can be generated.
- At least two optimization rules can be demonstrated.
- Target instructions or bytecode can be generated.
- The mission VM can execute valid compiled programs.
- Simulated spacecraft state changes are displayed.
- Lexical, syntax, semantic, and runtime errors are reported appropriately.
- Unit and integration tests are available.
- The implementation can be demonstrated through the command line.
- The project clearly satisfies the major Phase 2 compiler-design requirements.

---

## 21. Future Enhancements

Possible future enhancements include:

- More advanced variables and data types.
- Sensor-reading expressions.
- More detailed resource models.
- Thermal and power simulation.
- Fault injection and recovery commands.
- Mission scheduling constructs.
- Static resource estimation.
- More advanced optimization passes.
- Bytecode serialization.
- Interactive AST and IR visualization.
- Web-based compiler interface.
- Debugger for the mission VM.
- Multiple target instruction sets.
- Optional LLVM-based backend.
- Integration with simulated telemetry.
- Formal verification of selected mission properties.

These enhancements are not required for the initial Phase 2 prototype.

---

## 22. Final Deliverables

The final project submission shall include:

- Working Aegis source code.
- Language specification.
- Grammar definition.
- Lexer implementation.
- Parser implementation.
- AST implementation.
- Symbol table implementation.
- Semantic analyzer.
- Intermediate representation.
- Optimization passes.
- Target code generator.
- Mission VM or interpreter.
- Error-handling system.
- Unit tests.
- Integration tests.
- Example mission scripts.
- Execution outputs.
- Intermediate compiler outputs.
- Module-wise explanation.
- Implementation progress report.
- README with setup and execution instructions.
- Optional AST, IR, and execution visualizations.

---

## 23. Conclusion

Aegis is proposed as a modular domain-specific language and compiler for high-level autonomous spacecraft mission scripts. The project combines standard compiler-design phases with simplified spacecraft-domain semantics and a simulated mission virtual machine.

The product will begin with a small and clearly defined language, implement the compiler core incrementally, and validate each stage through unit and integration tests. The implementation will prioritize a functional compiler pipeline before optional visualization or web-interface features.

By completing lexical analysis, syntax analysis, AST construction, semantic analysis, symbol table management, intermediate code generation, optimization, target code generation, interpretation, and error handling, Aegis will provide a complete and demonstrable compiler-design project while maintaining a clear boundary between academic simulation and real spacecraft software.
