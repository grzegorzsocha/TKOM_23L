from lexer.lexer import Lexer
from lexer.tokens import TokenType, Token
from errors.errors import InvalidSyntaxError
import parser.nodes as nodes


class Parser:
    VARIABLE_TOKENS = [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING,
                       TokenType.LIST, TokenType.POINT, TokenType.LINE, TokenType.POLYHEDRON,
                       TokenType.COLLECTION]
    COMPLEX_VARIABLE_TOKENS = [TokenType.LIST, TokenType.POINT, TokenType.LINE,
                               TokenType.POLYHEDRON, TokenType.COLLECTION]
    COMPARISON_TOKENS = [TokenType.EQ, TokenType.NEQ, TokenType.LE, TokenType.GE,
                         TokenType.GREATER, TokenType.LESS]

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def get_current_token_type(self) -> TokenType:
        return self.current_token.type

    def get_current_token_value(self):
        return self.current_token.value

    def consume(self) -> Token:
        self.current_token = self.lexer.get_next_token()
        while self.get_current_token_type() == TokenType.COMMENT:
            self.current_token = self.lexer.get_next_token()
        return self.current_token

    def require_token(self, token_type: TokenType) -> bool:
        if self.get_current_token_type() != token_type:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     f"Expected {token_type}, got {self.get_current_token_type()}")
        return True

    def require_tokens(self, token_types: list[TokenType]) -> bool:
        if self.get_current_token_type() not in token_types:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     f"Expected one of {token_types}, got {self.get_current_token_type()}")
        return True

    def require_token_and_consume(self, token_type: TokenType) -> None:
        self.require_token(token_type)
        self.consume()

    def parse_program(self) -> nodes.Program:
        functions = []
        while self.get_current_token_type() != TokenType.EOF:
            functions.append(self.parse_function())
        return nodes.Program(functions)

    def parse_function(self) -> nodes.Function:
        function_type = self.parse_function_type()
        name = self.parse_identifier()
        self.require_token_and_consume(TokenType.LPAREN)
        parameters = []
        if self.get_current_token_type() != TokenType.RPAREN:
            parameters = self.parse_function_parameters()
        self.require_token_and_consume(TokenType.RPAREN)
        self.require_token_and_consume(TokenType.LBRACE)
        block = self.parse_block()
        self.require_token_and_consume(TokenType.RBRACE)
        return nodes.Function(function_type, name, parameters, block)

    def parse_function_type(self) -> nodes.FunctionType:
        self.require_tokens(self.VARIABLE_TOKENS + [TokenType.VOID])
        type = self.get_current_token_value()
        self.consume()
        return nodes.FunctionType(type)

    def parse_variable_type(self) -> nodes.VariableType:
        self.require_tokens(self.VARIABLE_TOKENS)
        type = self.get_current_token_value()
        self.consume()
        return nodes.VariableType(type)

    def parse_identifier(self) -> nodes.Identifier:
        self.require_token(TokenType.IDENTIFIER)
        identifier = self.get_current_token_value()
        self.consume()
        return nodes.Identifier(identifier)

    def parse_function_parameters(self) -> list[nodes.Parameter]:
        parameters = []
        parameters.append(self.parse_function_parameter())
        while self.get_current_token_type() == TokenType.COMMA:
            self.consume()
            parameters.append(self.parse_function_parameter())
        return parameters

    def parse_function_parameter(self) -> nodes.Parameter:
        type = self.parse_variable_type()
        identifier = self.parse_identifier()
        return nodes.Parameter(type, identifier)

    def parse_block(self) -> nodes.Block:
        statements = []
        while self.get_current_token_type() != TokenType.RBRACE:
            statements.append(self.parse_statement())
        return nodes.Block(statements)

    def parse_statement_block(self) -> nodes.Block:
        block = self.parse_block()
        self.require_token_and_consume(TokenType.RBRACE)
        return block

    def parse_statement(self):
        if self.get_current_token_type() == TokenType.RETURN:
            return self.parse_return_statement()
        elif self.get_current_token_type() == TokenType.IF:
            return self.parse_if_statement()
        elif self.get_current_token_type() == TokenType.WHILE:
            return self.parse_while_statement()
        elif self.get_current_token_type() in self.VARIABLE_TOKENS:
            return self.parse_declaration_statement()
        elif self.get_current_token_type() == TokenType.IDENTIFIER:
            identifier = self.parse_identifier()
            if self.get_current_token_type() == TokenType.DOT:
                method_call = self.parse_method_call_statement(identifier)
                self.require_token_and_consume(TokenType.SEMI)
                return method_call
            elif self.get_current_token_type() == TokenType.ASSIGN:
                self.require_token_and_consume(TokenType.ASSIGN)
                expression = self.parse_expression()
                self.require_token_and_consume(TokenType.SEMI)
                return nodes.AssignmentExpression(identifier, expression)
            elif self.get_current_token_type() == TokenType.LPAREN:
                return self.parse_function_call_statement(identifier)
        else:
            return self.parse_expression()

    def parse_return_statement(self) -> nodes.ReturnStatement:
        self.require_token_and_consume(TokenType.RETURN)
        expression = self.parse_expression()
        self.require_token_and_consume(TokenType.SEMI)
        return nodes.ReturnStatement(expression)

    def parse_if_statement(self) -> nodes.IfStatement:
        self.require_token_and_consume(TokenType.IF)
        self.require_token_and_consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.require_token_and_consume(TokenType.RPAREN)
        self.require_token_and_consume(TokenType.LBRACE)
        block = self.parse_statement_block()
        if self.get_current_token_type() == TokenType.ELSE:
            self.consume()
            self.require_token_and_consume(TokenType.LBRACE)
            else_block = self.parse_statement_block()
            return nodes.IfStatement(condition, block, else_block)
        return nodes.IfStatement(condition, block)

    def parse_while_statement(self) -> nodes.WhileStatement:
        self.require_token_and_consume(TokenType.WHILE)
        self.require_token_and_consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.require_token_and_consume(TokenType.RPAREN)
        self.require_token_and_consume(TokenType.LBRACE)
        block = self.parse_statement_block()
        return nodes.WhileStatement(condition, block)

    def parse_declaration_statement(self) -> nodes.DeclarationStatement:
        type = self.parse_variable_type()
        identifier = self.parse_identifier()
        if self.get_current_token_type() == TokenType.ASSIGN:
            self.consume()
            expression = self.parse_expression()
            self.require_token_and_consume(TokenType.SEMI)
            return nodes.DeclarationStatement(type, identifier, expression)
        self.require_token_and_consume(TokenType.SEMI)
        return nodes.DeclarationStatement(type, identifier)

    def parse_method_call_statement(self, caller: nodes.Identifier):
        method_calls = []
        while self.get_current_token_type() == TokenType.DOT:
            self.require_token_and_consume(TokenType.DOT)
            identifier = self.parse_identifier()
            self.require_token_and_consume(TokenType.LPAREN)
            arguments = []
            if self.get_current_token_type() != TokenType.RPAREN:
                arguments = self.parse_call_arguments()
            self.require_token_and_consume(TokenType.RPAREN)
            method_calls.append(nodes.MethodCall(identifier, arguments))
        return nodes.MethodCallExpression(caller, method_calls)

    def parse_function_call_statement(self, identifier: nodes.Identifier):
        self.require_token_and_consume(TokenType.LPAREN)
        arguments = []
        if self.get_current_token_type() != TokenType.RPAREN:
            arguments = self.parse_call_arguments()
        self.require_token_and_consume(TokenType.RPAREN)
        self.require_token_and_consume(TokenType.SEMI)
        return nodes.FunctionCallStatement(identifier, arguments)

    def parse_call_arguments(self) -> list:
        arguments = []
        arguments.append(self.parse_expression())
        while self.get_current_token_type() == TokenType.COMMA:
            self.consume()
            arguments.append(self.parse_expression())
        return arguments

    def parse_expression(self):
        return self.parse_or_expression()

    def parse_or_expression(self):
        left = self.parse_and_expression()
        while self.get_current_token_type() == TokenType.OR:
            self.consume()
            right = self.parse_and_expression()
            left = nodes.OrExpression(left, right)
        return left

    def parse_and_expression(self):
        left = self.parse_comparison_expression()
        while self.get_current_token_type() == TokenType.AND:
            self.consume()
            right = self.parse_comparison_expression()
            left = nodes.AndExpression(left, right)
        return left

    def parse_comparison_expression(self):
        left = self.parse_additive_expression()
        while self.get_current_token_type() in self.COMPARISON_TOKENS:
            operator = self.get_current_token_value()
            self.consume()
            right = self.parse_additive_expression()
            left = nodes.ComparisonExpression(left, operator, right)
        return left

    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()
        while self.get_current_token_type() in [TokenType.PLUS, TokenType.MINUS]:
            operator = self.get_current_token_value()
            self.consume()
            right = self.parse_multiplicative_expression()
            left = nodes.AdditiveExpression(left, operator, right)
        return left

    def parse_multiplicative_expression(self):
        left = self.parse_negation_expression()
        while self.get_current_token_type() in [TokenType.MUL, TokenType.DIV]:
            operator = self.get_current_token_value()
            self.consume()
            right = self.parse_negation_expression()
            left = nodes.MultiplicativeExpression(left, operator, right)
        return left

    def parse_negation_expression(self):
        negated = False
        if (self.get_current_token_type() == TokenType.NOT or
                self.get_current_token_type() == TokenType.MINUS):
            operator = self.get_current_token_value()
            self.consume()
            negated = True
        expression = self.parse_method_call_expression()
        if negated:
            return nodes.NegationExpression(operator, expression)
        else:
            return expression

    def parse_method_call_expression(self):
        expression = self.parse_factor()
        method_calls = []
        while self.get_current_token_type() == TokenType.DOT:
            self.consume()
            identifier = self.parse_identifier()
            self.require_token_and_consume(TokenType.LPAREN)
            arguments = []
            if self.get_current_token_type() != TokenType.RPAREN:
                arguments = self.parse_call_arguments()
            self.require_token_and_consume(TokenType.RPAREN)
            method_calls.append(nodes.MethodCall(identifier, arguments))
        if method_calls:
            return nodes.MethodCallExpression(expression, method_calls)
        else:
            return expression

    def parse_factor(self):
        expression = self.parse_literal()
        if expression is not None:
            return expression
        elif self.get_current_token_type() == TokenType.LPAREN:
            self.consume()
            expression = self.parse_expression()
            self.require_token_and_consume(TokenType.RPAREN)
            return expression
        elif self.get_current_token_type() == TokenType.IDENTIFIER:
            identifier = self.parse_identifier()
            if self.get_current_token_type() == TokenType.LPAREN:
                self.consume()
                return self.parse_function_call_in_expression(identifier)
            return identifier
        elif self.get_current_token_type() in self.COMPLEX_VARIABLE_TOKENS:
            self.require_tokens(self.COMPLEX_VARIABLE_TOKENS)
            identifier = self.get_current_token_value()
            self.consume()
            if self.get_current_token_type() == TokenType.LPAREN:
                self.consume()
                return self.parse_function_call_in_expression(identifier)
        else:
            raise InvalidSyntaxError(self.current_token.pos[0], self.current_token.pos[1],
                                     "Unrecognized expression")

    def parse_function_call_in_expression(self, identifier: nodes.Identifier):
        arguments = []
        if self.get_current_token_type() != TokenType.RPAREN:
            arguments = self.parse_call_arguments()
        self.require_token_and_consume(TokenType.RPAREN)
        return nodes.FunctionCallStatement(identifier, arguments)

    def parse_literal(self):
        if self.get_current_token_type() == TokenType.INT_VALUE:
            value = self.get_current_token_value()
            self.consume()
            return nodes.IntValue(value)
        elif self.get_current_token_type() == TokenType.FLOAT_VALUE:
            value = self.get_current_token_value()
            self.consume()
            return nodes.FloatValue(value)
        elif self.get_current_token_type() == TokenType.STRING_VALUE:
            value = self.get_current_token_value()
            self.consume()
            return nodes.StringValue(value)
        elif self.get_current_token_type() in [TokenType.TRUE, TokenType.FALSE]:
            value = self.get_current_token_value()
            if value == "True":
                value = True
            else:
                value = False
            self.consume()
            return nodes.BoolValue(value)
        else:
            return None
