from abc import ABC, abstractmethod


tree_depth = 0


class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Identifier(Node):
    def __init__(self, name: str) -> None:
        self.name = name

    def accept(self, visitor) -> None:
        return visitor.visit_identifier(self)

    def __repr__(self) -> str:
        return f"IdentifierName = {self.name}"


class BoolValue(Node):
    def __init__(self, value: bool) -> None:
        self.value = value

    def accept(self, visitor) -> None:
        return visitor.visit_bool_value(self)

    def __repr__(self) -> str:
        return f"BoolValue = {self.value}"


class IntValue(Node):
    def __init__(self, value: int) -> None:
        self.value = value

    def accept(self, visitor) -> None:
        return visitor.visit_int_value(self)

    def __repr__(self) -> str:
        return f"IntValue = {self.value}"


class FloatValue(Node):
    def __init__(self, value: float) -> None:
        self.value = value

    def accept(self, visitor) -> None:
        return visitor.visit_float_value(self)

    def __repr__(self) -> str:
        return f"FloatValue = {self.value}"


class StringValue(Node):
    def __init__(self, value: str) -> None:
        self.value = value

    def accept(self, visitor) -> None:
        return visitor.visit_string_value(self)

    def __repr__(self) -> str:
        return f"StringValue = \"{self.value}\""


class FunctionType(Node):
    def __init__(self, type: str) -> None:
        self.type = type

    def accept(self, visitor) -> None:
        return visitor.visit_function_type(self)

    def __repr__(self) -> str:
        return f"FunctionType = {self.type}"


class VariableType(Node):
    def __init__(self, type: str) -> None:
        self.type = type

    def accept(self, visitor) -> None:
        return visitor.visit_variable_type(self)

    def __repr__(self) -> str:
        return f"VariableType = {self.type}"


class Parameter(Node):
    def __init__(self, type: VariableType, identifier: Identifier) -> None:
        self.identifier = identifier
        self.type = type

    def accept(self, visitor) -> None:
        return visitor.visit_parameter(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"Parameter: {self.identifier}, {self.type}"
        tree_depth -= 3
        return r


class AssignmentExpression(Node):
    def __init__(self, identifier: Identifier, expression) -> None:
        self.identifier = identifier
        self.expression = expression

    def accept(self, visitor) -> None:
        return visitor.visit_assignment_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} AssignmentExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Identifier: {self.identifier}"
        r += f"\n{' ' * tree_depth} Expression: {self.expression}"
        tree_depth -= 6
        return r


class OrExpression(Node):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor) -> None:
        return visitor.visit_or_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} OrExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} LeftOperand: {self.left}"
        r += f"\n{' ' * tree_depth} RightOperand: {self.right}"
        tree_depth -= 6
        return r


class AndExpression(Node):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor) -> None:
        return visitor.visit_and_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} AndExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} LeftOperand: {self.left}"
        r += f"\n{' ' * tree_depth} RightOperand: {self.right}"
        tree_depth -= 6
        return r


class ComparisonExpression(Node):
    def __init__(self, left, operator: str, right) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor) -> None:
        return visitor.visit_comparison_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} ComparisonExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} LeftOperand: {self.left}"
        r += f"\n{' ' * tree_depth} Operator: {self.operator}"
        r += f"\n{' ' * tree_depth} RightOperand: {self.right}"
        tree_depth -= 6
        return r


class AdditiveExpression(Node):
    def __init__(self, left, operator: str, right) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor) -> None:
        return visitor.visit_additive_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} AdditiveExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} LeftOperand: {self.left}"
        r += f"\n{' ' * tree_depth} Operator: {self.operator}"
        r += f"\n{' ' * tree_depth} RightOperand: {self.right}"
        tree_depth -= 6
        return r


class MultiplicativeExpression(Node):
    def __init__(self, left, operator: str, right) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor) -> None:
        return visitor.visit_multiplicative_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} MultiplicativeExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} LeftOperand: {self.left}"
        r += f"\n{' ' * tree_depth} Operator: {self.operator}"
        r += f"\n{' ' * tree_depth} RightOperand: {self.right}"
        tree_depth -= 6
        return r


class NegationExpression(Node):
    def __init__(self, operator, expression) -> None:
        self.operator = operator
        self.expression = expression

    def accept(self, visitor) -> None:
        return visitor.visit_negation_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} NegationExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Operand: {self.operator}"
        tree_depth -= 6
        return r


class MethodCall(Node):
    def __init__(self, name: Identifier, arguments: list) -> None:
        self.name = name
        self.arguments = arguments

    def accept(self, visitor, caller) -> None:
        return visitor.visit_method_call(self, caller)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} MethodCall:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} MethodName: {self.name}"
        r += f"\n{' ' * tree_depth} Arguments:"
        tree_depth += 3
        for argument in self.arguments:
            r += f"\n{' ' * tree_depth} Argument: {argument}"
        tree_depth -= 9
        return r


class MethodCallExpression(Node):
    def __init__(self, caller: Identifier, methods: list[MethodCall]) -> None:
        self.caller = caller
        self.methods = methods

    def accept(self, visitor) -> None:
        return visitor.visit_method_call_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} MethodCallExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Caller: {self.caller}"
        r += f"\n{' ' * tree_depth} Methods: {self.methods}"
        tree_depth -= 6
        return r


class FunctionCallStatement(Node):
    def __init__(self, identifier: Identifier, arguments: list) -> None:
        self.identifier = identifier
        self.arguments = arguments

    def accept(self, visitor) -> None:
        return visitor.visit_function_call(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} FunctionCallStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} FunctionName: {self.identifier}"
        r += f"\n{' ' * tree_depth} Arguments:"
        tree_depth += 3
        for argument in self.arguments:
            r += f"\n{' ' * tree_depth} Argument: {argument}"
        tree_depth -= 9
        return r


class Block(Node):
    def __init__(self, statements: list) -> None:
        self.statements = statements

    def accept(self, visitor) -> None:
        return visitor.visit_block(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} Block:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Statements:"
        tree_depth += 3
        for statement in self.statements:
            r += f"\n{' ' * tree_depth} Statement: {statement}"
        tree_depth -= 9
        return r


class IfStatement(Node):
    def __init__(self, condition, block: Block, else_block=None) -> None:
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def accept(self, visitor) -> None:
        return visitor.visit_if_statement(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} IfStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Condition: {self.condition}"
        r += f"\n{' ' * tree_depth} IfBlock:"
        r += f"{' ' * tree_depth} {self.block}"
        r += f"\n{' ' * tree_depth} ElseBlock:"
        if self.else_block is None:
            r += f"\n{' ' * (tree_depth + 3)} None"
        else:
            r += f"{' ' * tree_depth} {self.else_block}"
        tree_depth -= 6
        return r


class WhileStatement(Node):
    def __init__(self, condition, block: Block) -> None:
        self.condition = condition
        self.block = block

    def accept(self, visitor) -> None:
        return visitor.visit_while_statement(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} WhileStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Condition: {self.condition}"
        r += f"\n{' ' * tree_depth} WhileBlock:"
        r += f"{' ' * tree_depth} {self.block}"
        tree_depth -= 6
        return r


class DeclarationStatement(Node):
    def __init__(self, variable_type: VariableType, identifier: Identifier, expression=None) -> None:
        self.variable_type = variable_type
        self.identifier = identifier
        self.expression = expression

    def accept(self, visitor) -> None:
        return visitor.visit_declaration_statement(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} DeclarationStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} {self.variable_type}"
        r += f"\n{' ' * tree_depth} {self.identifier}"
        r += f"\n{' ' * tree_depth} DeclarationExpression: {self.expression}"
        tree_depth -= 6
        return r


class ReturnStatement(Node):
    def __init__(self, expression) -> None:
        self.expression = expression

    def accept(self, visitor) -> None:
        return visitor.visit_return_statement(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} ReturnStatement:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} ReturnExpression: {self.expression}"
        tree_depth -= 6
        return r


class Function(Node):
    def __init__(self, function_type: FunctionType, identifier: Identifier,
                 parameters: list, block: Block) -> None:
        self.function_type = function_type
        self.identifier = identifier
        self.parameters = parameters
        self.block = block

    def accept(self, visitor) -> None:
        return visitor.visit_function(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} Function:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} FunctionName: {self.identifier}"
        r += f"\n{' ' * tree_depth} FunctionType: {self.function_type}"
        r += f"\n{' ' * tree_depth} Parameters:"
        tree_depth += 3
        for parameter in self.parameters:
            r += f"\n{' ' * tree_depth} {parameter}"
        tree_depth -= 6
        r += f"{' ' * tree_depth} {self.block}"
        tree_depth -= 3
        return r


class Program(Node):
    def __init__(self, functions: list) -> None:
        self.functions = functions

    def accept(self, visitor) -> None:
        return visitor.visit_program(self)

    def __repr__(self) -> str:
        return f"Program:{self.functions}"
