from abc import ABC, abstractmethod


tree_depth = 0


class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass


class Identifier(Node):
    def __init__(self, name: str) -> None:
        self.name = name

    def accept(self, visitor) -> None:
        return visitor.visit_identifier(self)

    def __repr__(self) -> str:
        return f"IdentifierName = {self.name}"

    def __eq__(self, other) -> bool:
        return isinstance(other, Identifier) and self.name == other.name


class BoolValue(Node):
    def __init__(self, value: bool) -> None:
        self.value = value

    def accept(self, visitor) -> None:
        return visitor.visit_value(self)

    def __repr__(self) -> str:
        return f"BoolValue = {self.value}"

    def __eq__(self, other) -> bool:
        return isinstance(other, BoolValue) and self.value == other.value


class IntValue(Node):
    def __init__(self, value: int) -> None:
        self.value = value

    def accept(self, visitor) -> None:
        return visitor.visit_int_value(self)

    def __repr__(self) -> str:
        return f"IntValue = {self.value}"

    def __eq__(self, other) -> bool:
        return isinstance(other, IntValue) and self.value == other.value


class FloatValue(Node):
    def __init__(self, value: float) -> None:
        self.value = value

    def accept(self, visitor) -> None:
        return visitor.visit_float_value(self)

    def __repr__(self) -> str:
        return f"FloatValue = {self.value}"

    def __eq__(self, other) -> bool:
        return isinstance(other, FloatValue) and self.value == other.value


class StringValue(Node):
    def __init__(self, value: str) -> None:
        self.value = value

    def accept(self, visitor) -> None:
        return visitor.visit_string_value(self)

    def __repr__(self) -> str:
        return f"StringValue = \"{self.value}\""

    def __eq__(self, other) -> bool:
        return isinstance(other, StringValue) and self.value == other.value


class FunctionType(Node):
    def __init__(self, type: str) -> None:
        self.type = type

    def accept(self, visitor) -> None:
        return visitor.visit_function_type(self)

    def __repr__(self) -> str:
        return f"FunctionType = {self.type}"

    def __eq__(self, other) -> bool:
        return isinstance(other, FunctionType) and self.type == other.type


class VariableType(Node):
    def __init__(self, type: str) -> None:
        self.type = type

    def accept(self, visitor) -> None:
        return visitor.visit_variable_type(self)

    def __repr__(self) -> str:
        return f"VariableType = {self.type}"

    def __eq__(self, other) -> bool:
        return isinstance(other, VariableType) and self.type == other.type


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

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Parameter) and self.identifier == other.identifier and
            self.type == other.type
        )


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

    def __eq__(self, other) -> bool:
        return isinstance(other, OrExpression) and self.left == other.left and self.right == other.right


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

    def __eq__(self, other) -> bool:
        return isinstance(other, AndExpression) and self.left == other.left and self.right == other.right


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

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, ComparisonExpression) and self.left == other.left and
            self.operator == other.operator and self.right == other.right
        )


class ArithmeticExpression(Node):
    def __init__(self, left, operator: str, right) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor) -> None:
        return visitor.visit_arithmetic_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} ArithmeticExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} LeftOperand: {self.left}"
        r += f"\n{' ' * tree_depth} Operator: {self.operator}"
        r += f"\n{' ' * tree_depth} RightOperand: {self.right}"
        tree_depth -= 6
        return r

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, ArithmeticExpression) and self.left == other.left and
            self.operator == other.operator and self.right == other.right
        )


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

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, MultiplicativeExpression) and self.left == other.left and
            self.operator == other.operator and self.right == other.right
        )


class NegationExpression(Node):
    def __init__(self, expression) -> None:
        self.expression = expression

    def accept(self, visitor) -> None:
        return visitor.visit_negation_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} NegationExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Operand: {self.left}"
        tree_depth -= 6
        return r

    def __eq__(self, other) -> bool:
        return isinstance(other, NegationExpression) and self.expression == other.expression


class MethodCallExpression(Node):
    def __init__(self, object: Identifier, method: Identifier, arguments: list) -> None:
        self.object = object
        self.method = method
        self.arguments = arguments

    def accept(self, visitor) -> None:
        return visitor.visit_method_call_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} MethodCallExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} Caller: {self.object}"
        r += f"\n{' ' * tree_depth} Method: {self.method}"
        r += f"\n{' ' * tree_depth} Arguments: {self.arguments}"
        tree_depth -= 6
        return r

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, MethodCallExpression) and self.object == other.object and
            self.method == other.method and self.arguments == other.arguments
        )


class FunctionCallExpression(Node):
    def __init__(self, function_name: Identifier, arguments: list) -> None:
        self.function_name = function_name
        self.arguments = arguments

    def accept(self, visitor) -> None:
        return visitor.visit_function_call_expression(self)

    def __repr__(self) -> str:
        global tree_depth
        tree_depth += 3
        r = f"\n{' ' * tree_depth} FunctionCallExpression:"
        tree_depth += 3
        r += f"\n{' ' * tree_depth} FunctionName: {self.function_name}"
        r += f"\n{' ' * tree_depth} Arguments: {self.arguments}"
        tree_depth -= 6
        return r

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, FunctionCallExpression) and self.function_name == other.function_name and
            self.arguments == other.arguments
        )


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

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, FunctionCallStatement) and self.identifier == other.identifier and
            self.arguments == other.arguments
        )


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

    def __eq__(self, other) -> bool:
        return isinstance(other, Block) and self.statements == other.statements


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

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, IfStatement) and self.condition == other.condition
            and self.block == other.block and self.else_block == other.else_block
        )


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

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, WhileStatement) and self.condition == other.condition
            and self.block == other.block
        )


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

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, DeclarationStatement) and self.variable_type == other.variable_type
            and self.identifier == other.identifier and self.expression == other.expression
        )


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

    def __eq__(self, other) -> bool:
        return isinstance(other, ReturnStatement) and self.expression == other.expression


class Function(Node):
    def __init__(self, function_type: FunctionType, identifier: Identifier,
                 parameters: list, block: Block) -> None:
        self.function_type = function_type
        self.identifier = identifier
        self.parameters = parameters
        self.block = block

    def accept(self, visitor) -> None:
        return visitor.visit_function_declaration(self)

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

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Function) and self.function_type == other.function_type and
            self.identifier == other.identifier and self.parameters == other.parameters and
            self.block == other.block
        )


class Program(Node):
    def __init__(self, functions: list) -> None:
        self.functions = functions

    def accept(self, visitor) -> None:
        return visitor.visit_program(self)

    def __repr__(self) -> str:
        return f"Program:{self.functions}"

    def __eq__(self, other) -> bool:
        pass
