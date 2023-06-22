from interpreter.context import ContextManager
import interpreter.classes as c
import parser.nodes as nodes
import errors.errors as e


class Visitor:
    def __init__(self):
        self.context_manager = ContextManager()

    def is_variable(self, identifier: str):
        return self.context_manager.is_variable_exists(identifier)

    def visit_identifier(self, identifier: nodes.Identifier):
        return identifier.name

    def visit_bool_value(self, bool_value: nodes.BoolValue) -> bool:
        return bool_value.value

    def visit_int_value(self, int_value: nodes.IntValue) -> int:
        return int_value.value

    def visit_float_value(self, float_value: nodes.FloatValue) -> float:
        return float_value.value

    def visit_string_value(self, string_value: nodes.StringValue) -> str:
        return string_value.value

    def visit_function_type(self, function_type: nodes.FunctionType) -> str:
        return function_type.type

    def visit_variable_type(self, variable_type: nodes.VariableType) -> str:
        return variable_type.type

    def visit_parameter(self, parameter: nodes.Parameter):
        return (parameter.type.accept(self), parameter.identifier.accept(self))

    def visit_negation_expression(self, negation_expression: nodes.NegationExpression):
        operator = negation_expression.operator
        expression = negation_expression.expression.accept(self)
        if self.is_variable(expression):
            expression = self.context_manager.get_variable_value(expression)
        if operator == '-':
            return -expression
        elif operator == '!':
            return not expression

    def visit_method_call_expression(self, method_call_expression: nodes.MethodCallExpression):
        caller = method_call_expression.caller.accept(self)
        if not self.is_variable(caller):
            raise e.UndeclaredVariableError(caller)
        for method in method_call_expression.methods:
            caller = method.accept(self, caller)
        return caller

    def visit_method_call(self, method_call: nodes.MethodCall, caller):
        accepted_arguments = []
        for argument in method_call.arguments:
            accepted_arguments.append(argument.accept(self))
        method_name = method_call.name.accept(self)
        return self.execute_method(caller, method_name, accepted_arguments)

    def visit_additive_expression(self, additive_expression: nodes.AdditiveExpression):
        left = additive_expression.left.accept(self)
        right = additive_expression.right.accept(self)
        if self.is_variable(left):
            left = self.context_manager.get_variable_value(left)
        if self.is_variable(right):
            right = self.context_manager.get_variable_value(right)
        if additive_expression.operator == '+':
            return left + right
        elif additive_expression.operator == '-':
            return left - right

    def visit_multiplicative_expression(self, multiplicative_expression: nodes.MultiplicativeExpression):
        left = multiplicative_expression.left.accept(self)
        right = multiplicative_expression.right.accept(self)
        if self.is_variable(left):
            left = self.context_manager.get_variable_value(left)
        if self.is_variable(right):
            right = self.context_manager.get_variable_value(right)
        if multiplicative_expression.operator == '*':
            return left * right
        elif multiplicative_expression.operator == '/':
            return left / right

    def visit_comparison_expression(self, comparison_expression: nodes.ComparisonExpression):
        left = comparison_expression.left.accept(self)
        right = comparison_expression.right.accept(self)
        if self.is_variable(left):
            left = self.context_manager.get_variable_value(left)
        if self.is_variable(right):
            right = self.context_manager.get_variable_value(right)
        if comparison_expression.operator == '<':
            return left < right
        elif comparison_expression.operator == '>':
            return left > right
        elif comparison_expression.operator == '<=':
            return left <= right
        elif comparison_expression.operator == '>=':
            return left >= right
        elif comparison_expression.operator == '==':
            return left == right
        elif comparison_expression.operator == '!=':
            return left != right

    def visit_and_expression(self, and_expression: nodes.AndExpression):
        left = and_expression.left.accept(self)
        right = and_expression.right.accept(self)
        if self.is_variable(left):
            left = self.context_manager.get_variable_value(left)
        if self.is_variable(right):
            right = self.context_manager.get_variable_value(right)
        return left and right

    def visit_or_expression(self, or_expression: nodes.OrExpression):
        left = or_expression.left.accept(self)
        right = or_expression.right.accept(self)
        if self.is_variable(left):
            left = self.context_manager.get_variable_value(left)
        if self.is_variable(right):
            right = self.context_manager.get_variable_value(right)
        return left or right

    def visit_assignment_expression(self, assignment_expression: nodes.AssignmentExpression):
        identifier = assignment_expression.identifier.accept(self)
        if not self.is_variable(identifier):
            raise e.UndeclaredVariableError(identifier)
        new_value = assignment_expression.expression.accept(self)
        if eval(self.context_manager.get_variable_type(identifier)) == type(new_value):
            self.context_manager.set_variable_value(identifier, new_value)
        else:
            raise e.TypeMismatchError(identifier)

    def visit_function_call(self, function_call_statement: nodes.FunctionCallStatement):
        if (function_call_statement.identifier in self.context_manager.BUILT_IN or
           function_call_statement.identifier == 'print'):
            identifier = function_call_statement.identifier
        else:
            if not self.context_manager.is_function_exists(function_call_statement.identifier.name):
                raise e.UndeclaredFunctionError(function_call_statement.identifier)
            identifier = function_call_statement.identifier.accept(self)
        accepted_arguments = []
        for argument in function_call_statement.arguments:
            accepted_arguments.append(argument.accept(self))
        return self.execute_function(identifier, accepted_arguments)

    def visit_if_statement(self, if_statement: nodes.IfStatement):
        condition = if_statement.condition.accept(self)
        if not isinstance(condition, bool):
            raise e.InvalidConditionError(condition)
        if condition:
            if_statement.block.accept(self)
        elif if_statement.else_block:
            if_statement.else_block.accept(self)

    def visit_while_statement(self, while_statement: nodes.WhileStatement):
        condition = while_statement.condition.accept(self)
        if not isinstance(condition, bool):
            raise e.InvalidConditionError(condition)
        while condition:
            while_statement.block.accept(self)
            condition = while_statement.condition.accept(self)

    def visit_declaration_statement(self, declaration: nodes.DeclarationStatement):
        variable_type = declaration.variable_type.accept(self)
        identifier = declaration.identifier.accept(self)
        if declaration.expression:
            value = declaration.expression.accept(self)
        else:
            if variable_type == 'int':
                value = 0
            elif variable_type == 'float':
                value = 0.0
            elif variable_type == 'string':
                value = ''
            elif variable_type == 'bool':
                value = False
        if self.context_manager.is_variable_exists_in_current_context(identifier):
            raise e.RedefinitionError(identifier)
        self.context_manager.add_variable(identifier, value, variable_type)

    def visit_return_statement(self, return_statement: nodes.ReturnStatement):
        return return_statement.expression.accept(self)

    def visit_block(self, block: nodes.Block):
        for statement in block.statements:
            if self.context_manager.get_return_value() is not None:
                return self.context_manager.get_return_value()
            if isinstance(statement, nodes.ReturnStatement):
                self.context_manager.set_return_value(statement.accept(self))
            if self.context_manager.get_return_value() is not None:
                return self.context_manager.get_return_value()
            else:
                statement.accept(self)
        if self.context_manager.get_return_value() is not None:
            return self.context_manager.get_return_value()

    def visit_function(self, function: nodes.Function):
        if function.block.statements:
            function.block.accept(self)

    def visit_program(self, program: nodes.Program):
        main_function = None
        for function in program.functions:
            if (function.identifier.name == 'main' and function.function_type.type == 'int' and
               function.parameters == []):
                if main_function:
                    raise e.RedefinitionError(function.identifier)
                main_function = function
            elif function.identifier.name == 'print':
                raise e.RedefinitionError(function.identifier)
            elif not self.context_manager.is_function_exists(function.identifier.name):

                self.context_manager.add_function(function)
            else:
                raise e.RedefinitionError(function.identifier)
        if not main_function:
            raise e.MainFunctionNotFoundError()
        else:
            self.context_manager.add_function(main_function)
            self.context_manager.enter_context(main_function.identifier.name)
            return_value = self.execute_function(main_function.identifier.name, [])
        return return_value

    def execute_print(self, arguments):
        if len(arguments) != 1:
            raise e.InvalidNumberOfArgumentsError('print')
        if self.is_variable(arguments[0]):
            print(self.context_manager.get_variable_value(arguments[0]))
        else:
            print(arguments[0])

    def create_list(self, arguments):
        if arguments:
            return c.List(arguments)
        else:
            return c.List()

    def create_collection(self, arguments):
        if arguments:
            new_arguments = []
            for argument in arguments:
                if self.context_manager.is_variable_exists_in_current_context(argument):
                    argument = self.context_manager.get_variable_value(argument)
                if not isinstance(argument, c.Polyhedron):
                    raise e.InvalidTypeError("Collection can only contains Polyhedrons")
                new_arguments.append(argument)
            return c.Collection(new_arguments)
        else:
            return c.Collection()

    def create_polyhedron(self, arguments):
        if arguments:
            new_arguments = []
            for argument in arguments:
                if self.context_manager.is_variable_exists_in_current_context(argument):
                    argument = self.context_manager.get_variable_value(argument)
                    if not isinstance(argument, c.Line):
                        raise e.InvalidTypeError("Polyhedron can only be created from Lines")
                    new_arguments.append(argument)
                elif not isinstance(argument, c.Line):
                    raise e.InvalidTypeError("Polyhedron can only be created from Lines")
                else:
                    new_arguments.append(argument)
            polyhedron = c.Polyhedron(new_arguments)
            points = polyhedron.points()
            for point in points:
                occurence = 0
                for line in polyhedron.lines():
                    if point.x == line.start.x and point.y == line.start.y and point.z == line.start.z:
                        occurence += 1
                    if point.x == line.end.x and point.y == line.end.y and point.z == line.end.z:
                        occurence += 1
                if occurence < 3:
                    message = "In order to create polyhedron, each point must "
                    raise e.InvalidTypeError(message + "connected to at least 3 lines")
            return polyhedron
        else:
            raise e.InvalidNumberOfArgumentsError('Polyhedron')

    def create_line(self, arguments):
        if len(arguments) == 2:
            new_arguments = []
            for argument in arguments:
                if self.context_manager.is_variable_exists_in_current_context(argument):
                    argument = self.context_manager.get_variable_value(argument)
                    if not isinstance(argument, c.Point):
                        raise e.InvalidTypeError("Line can only be created from Points")
                    new_arguments.append(argument)
                elif not isinstance(argument, c.Point):
                    raise e.InvalidTypeError("Line can only be created from Points")
                else:
                    new_arguments.append(argument)
            return c.Line(new_arguments[0], new_arguments[1])
        else:
            raise e.InvalidNumberOfArgumentsError('Line')

    def create_point(self, arguments):
        if len(arguments) == 3:
            new_arguments = []
            for argument in arguments:
                if self.context_manager.is_variable_exists_in_current_context(argument):
                    argument_type = self.context_manager.get_variable_type(argument)
                    argument = self.context_manager.get_variable_value(argument)
                    if argument_type not in ['int', 'float']:
                        raise e.InvalidTypeError("Point arguments must be \'int\' or \'float\'")
                    new_arguments.append(argument)
                elif type(argument) not in [int, float]:
                    raise e.InvalidTypeError("Point arguments must be \'int\' or \'float\'")
                else:
                    new_arguments.append(argument)
            return c.Point(new_arguments[0], new_arguments[1], new_arguments[2])
        else:
            raise e.InvalidNumberOfArgumentsError('Point')

    def execute_function(self, function_name: str, arguments: list):
        if function_name == 'print':
            self.execute_print(arguments)
            return
        elif function_name == 'List':
            return self.create_list(arguments)
        elif function_name == 'Collection':
            return self.create_collection(arguments)
        elif function_name == 'Polyhedron':
            return self.create_polyhedron(arguments)
        elif function_name == 'Line':
            return self.create_line(arguments)
        elif function_name == 'Point':
            return self.create_point(arguments)
        elif function_name == 'main':
            function = self.context_manager.get_function(function_name)
            return_value = function.block.accept(self)
            if self.context_manager.is_variable_exists(return_value):
                return_value = self.context_manager.get_variable_value(return_value)
            if function.function_type.type == 'void' and return_value is not None:
                raise e.InvalidReturnTypeError(function.function_type.type, return_value)
            elif eval(function.function_type.type) != type(return_value):
                raise e.InvalidReturnTypeError(function.function_type.type, return_value)
            self.context_manager.exit_context()
            return return_value
        else:
            self.context_manager.enter_context(function_name)
            function = self.context_manager.get_function(function_name)
            function_type = function.function_type.type
            if len(function.parameters) != len(arguments):
                raise e.InvalidNumberOfArgumentsError(function_name)
            for parameter, argument in zip(function.parameters, arguments):
                name = parameter.identifier.name
                parameter_type = parameter.type.type
                if self.is_variable(argument):
                    value = self.context_manager.get_variable_value(argument)
                else:
                    value = argument
                if eval(parameter_type) != type(value):
                    raise e.TypeMismatchError(parameter.identifier)
                self.context_manager.add_variable(name, value, parameter_type)
            return_value = function.block.accept(self)
            if function_type == 'void':
                if return_value is not None:
                    raise e.InvalidReturnTypeError(function_type, return_value)
            elif function_type in self.context_manager.BUILT_IN.keys():
                if not return_value.__class__.__name__ == function_type:
                    raise e.InvalidReturnTypeError(function_type, return_value)
            elif eval(function_type) != type(return_value):
                raise e.InvalidReturnTypeError(function_type, return_value)
            self.context_manager.exit_context()
            return return_value

    def execute_method(self, name, method_name: str, arguments: list):
        argument_values = []
        for argument in arguments:
            if self.is_variable(argument):
                argument_values.append(self.context_manager.get_variable_value(argument))
            else:
                argument_values.append(argument)
        if self.context_manager.is_variable_exists(name):
            value = self.context_manager.get_variable_value(name)
            type = self.context_manager.get_variable_type(name)
            if type in self.context_manager.BUILT_IN:
                for method in self.context_manager.BUILT_IN[type]:
                    if method_name == method:
                        if method_name in ['lines', 'points']:
                            return c.List(getattr(value, method_name)(*argument_values))
                        return getattr(value, method_name)(*argument_values)
                raise e.InvalidMethodCallError(type, method_name)
        elif name.__class__.__name__ in self.context_manager.BUILT_IN:
            for method in self.context_manager.BUILT_IN[name.__class__.__name__]:
                if method_name == method:
                    if method_name in ['lines', 'points']:
                        return c.List(getattr(name, method_name)(*argument_values))
                    return getattr(name, method_name)(*argument_values)
            raise e.InvalidMethodCallError(name.__class__.__name__, method_name)
        else:
            raise e.UndeclaredVariableError(name)
