"""Handwritten recursive-descent parser for the initial AEGIS grammar."""

from __future__ import annotations

from aegis.ast import (
    BinaryExpression,
    Block,
    BooleanLiteral,
    CameraCommand,
    CaptureImageCommand,
    Expression,
    Identifier,
    IfStatement,
    Mission,
    MoveCommand,
    NumberLiteral,
    PowerCommand,
    RepeatStatement,
    SafeModeCommand,
    SourceLocation,
    Statement,
    StringLiteral,
    TransmitImageCommand,
    UnaryExpression,
    WaitCommand,
)
from aegis.lexer import Token, TokenType

from .errors import ParseFailure, ParserError, error_for_token


_STATEMENT_STARTS = {
    TokenType.POWER,
    TokenType.MOVE,
    TokenType.CAMERA,
    TokenType.CAPTURE,
    TokenType.TRANSMIT,
    TokenType.WAIT,
    TokenType.SAFE_MODE,
    TokenType.IF,
    TokenType.REPEAT,
}


class Parser:
    """Parse lexer tokens into an AEGIS AST and collect syntax errors."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.errors: list[ParserError] = []
        self._current = 0

    def parse(self) -> Mission | None:
        try:
            mission = self._parse_mission()
            if not self._check(TokenType.EOF):
                self._raise_error("Expected end of input after mission", self._peek(), "end of input")
            return mission
        except ParseFailure as failure:
            self.errors.append(failure.error)
            self._synchronize()
            return None

    def _parse_mission(self) -> Mission:
        mission_token = self._consume(TokenType.MISSION, "Expected 'MISSION' at the start of a program")
        name_token = self._consume(TokenType.IDENTIFIER, "Expected a mission name after 'MISSION'")
        body = self._parse_block()
        return Mission(name_token.lexeme, body, location=self._location(mission_token))

    def _parse_block(self) -> Block:
        opening = self._consume(TokenType.LEFT_BRACE, "Expected '{' to start a block")
        statements: list[Statement] = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._check(TokenType.EOF):
            try:
                statements.append(self._parse_statement())
            except ParseFailure as failure:
                self.errors.append(failure.error)
                self._synchronize()
        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after block")
        return Block(tuple(statements), location=self._location(opening))

    def _parse_statement(self) -> Statement:
        if self._match(TokenType.POWER):
            command_token = self._previous()
            value = self._parse_expression()
            self._consume_semicolon("POWER command")
            return PowerCommand(value, location=self._location(command_token))
        if self._match(TokenType.MOVE):
            command_token = self._previous()
            distance = self._parse_expression()
            self._consume_semicolon("MOVE command")
            return MoveCommand(distance, location=self._location(command_token))
        if self._match(TokenType.CAMERA):
            return self._parse_camera()
        if self._match(TokenType.CAPTURE):
            command_token = self._previous()
            self._consume(TokenType.IMAGE, "Expected 'IMAGE' after 'CAPTURE'")
            self._consume_semicolon("CAPTURE IMAGE command")
            return CaptureImageCommand(location=self._location(command_token))
        if self._match(TokenType.TRANSMIT):
            command_token = self._previous()
            self._consume(TokenType.IMAGE, "Expected 'IMAGE' after 'TRANSMIT'")
            self._consume_semicolon("TRANSMIT IMAGE command")
            return TransmitImageCommand(location=self._location(command_token))
        if self._match(TokenType.WAIT):
            command_token = self._previous()
            duration = self._parse_expression()
            self._consume_semicolon("WAIT command")
            return WaitCommand(duration, location=self._location(command_token))
        if self._match(TokenType.SAFE_MODE):
            command_token = self._previous()
            self._consume_semicolon("Expected ';' after SAFE_MODE command")
            return SafeModeCommand(location=self._location(command_token))
        if self._match(TokenType.IF):
            return self._parse_if(self._previous())
        if self._match(TokenType.REPEAT):
            return self._parse_repeat(self._previous())
        self._raise_error("Expected a statement", self._peek(), "a command or control-flow statement")

    def _parse_camera(self) -> CameraCommand:
        command_token = self._previous()
        if self._match(TokenType.ON):
            enabled = True
        elif self._match(TokenType.OFF):
            enabled = False
        else:
            self._raise_error("Expected 'ON' or 'OFF' after 'CAMERA'", self._peek(), "'ON' or 'OFF'")
        self._consume_semicolon("CAMERA command")
        return CameraCommand(enabled, location=self._location(command_token))

    def _parse_if(self, keyword: Token) -> IfStatement:
        condition = self._parse_expression()
        then_branch = self._parse_block()
        else_branch = self._parse_block() if self._match(TokenType.ELSE) else None
        return IfStatement(condition, then_branch, else_branch, location=self._location(keyword))

    def _parse_repeat(self, keyword: Token) -> RepeatStatement:
        count = self._parse_expression()
        body = self._parse_block()
        return RepeatStatement(count, body, location=self._location(keyword))

    def _parse_expression(self) -> Expression:
        return self._parse_equality()

    def _parse_equality(self) -> Expression:
        expression = self._parse_relational()
        while self._match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            operator = self._previous()
            expression = BinaryExpression(expression, operator.lexeme, self._parse_relational(), location=self._location(operator))
        return expression

    def _parse_relational(self) -> Expression:
        expression = self._parse_additive()
        while self._match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            operator = self._previous()
            expression = BinaryExpression(expression, operator.lexeme, self._parse_additive(), location=self._location(operator))
        return expression

    def _parse_additive(self) -> Expression:
        expression = self._parse_multiplicative()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            expression = BinaryExpression(expression, operator.lexeme, self._parse_multiplicative(), location=self._location(operator))
        return expression

    def _parse_multiplicative(self) -> Expression:
        expression = self._parse_unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous()
            expression = BinaryExpression(expression, operator.lexeme, self._parse_unary(), location=self._location(operator))
        return expression

    def _parse_unary(self) -> Expression:
        if self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            return UnaryExpression(operator.lexeme, self._parse_unary(), location=self._location(operator))
        return self._parse_primary()

    def _parse_primary(self) -> Expression:
        if self._match(TokenType.INTEGER, TokenType.DECIMAL):
            token = self._previous()
            return NumberLiteral(token.value, location=self._location(token))
        if self._match(TokenType.STRING):
            token = self._previous()
            return StringLiteral(token.value, location=self._location(token))
        if self._match(TokenType.TRUE, TokenType.FALSE):
            token = self._previous()
            return BooleanLiteral(token.type is TokenType.TRUE, location=self._location(token))
        if self._match(TokenType.IDENTIFIER):
            token = self._previous()
            return Identifier(token.lexeme, location=self._location(token))
        if self._match(TokenType.LEFT_PAREN):
            expression = self._parse_expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return expression
        self._raise_error("Expected an expression", self._peek(), "an expression")

    def _consume_semicolon(self, description: str) -> None:
        self._consume(TokenType.SEMICOLON, f"Expected ';' after {description}")

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        self._raise_error(message, self._peek(), token_type.name)

    def _raise_error(self, message: str, token: Token, expected: str | None = None) -> None:
        raise ParseFailure(error_for_token(message, token, expected))

    def _synchronize(self) -> None:
        while not self._check(TokenType.EOF):
            if self._previous().type is TokenType.SEMICOLON:
                return
            if self._peek().type in _STATEMENT_STARTS or self._peek().type is TokenType.RIGHT_BRACE:
                return
            self._advance()

    def _match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type is token_type

    def _advance(self) -> Token:
        if not self._at_end():
            self._current += 1
        return self._previous()

    def _at_end(self) -> bool:
        return self._peek().type is TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self._current]

    def _previous(self) -> Token:
        return self.tokens[self._current - 1]

    @staticmethod
    def _location(token: Token) -> SourceLocation:
        return SourceLocation(token.line, token.column)
