import errors.errors as e


class Context:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.return_value = None
        self.variables = {}
        self.functions = {}

    def add_variable(self, name: str, value, type):
        self.variables[name] = (value, type)

    def get_variable(self, name: str):
        if name in self.variables.keys():
            return self.variables[name]
        if self.parent:
            return self.parent.get_variable(name)
        raise e.UndeclaredVariableError(name)

    def get_variable_in_current_context(self, name: str):
        if name in self.variables.keys():
            return self.variables[name]
        raise e.UndeclaredVariableError(name)

    def add_function(self, function):
        self.functions[function.identifier.name] = function

    def get_function(self, name: str):
        if name in self.functions.keys():
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise e.UndeclaredVariableError(name)

    def set_return_value(self, value):
        self.return_value = value

    def get_return_value(self):
        return self.return_value


class ContextManager:
    BUILT_IN = {
        'List': ['add', 'remove', 'get', 'length'],
        'Point': ['get_x', 'get_y', 'get_z', 'set_x', 'set_y', 'set_z'],
        'Line': ['get_start', 'get_end', 'set_start', 'set_end', 'length'],
        'Polyhedron': ['points', 'lines'],
        'Collection': ['add', 'remove', 'display', 'empty']
    }

    def __init__(self):
        self.current_context = Context('global')

    def add_variable(self, name: str, value, type):
        self.current_context.add_variable(name, value, type)

    def get_variable_value(self, name: str):
        return self.current_context.get_variable(name)[0]

    def get_variable_type(self, name: str):
        return self.current_context.get_variable(name)[1]

    def set_variable_value(self, name: str, value):
        self.current_context.variables[name] = (value, self.get_variable_type(name))

    def is_variable_exists(self, name: str) -> bool:
        try:
            self.get_variable_value(name)
            return True
        except e.UndeclaredVariableError:
            return False

    def is_variable_exists_in_current_context(self, name: str) -> bool:
        try:
            self.current_context.get_variable_in_current_context(name)
            return True
        except e.UndeclaredVariableError:
            return False

    def add_function(self, function):
        self.current_context.add_function(function)

    def get_function(self, name: str):
        return self.current_context.get_function(name)

    def is_function_exists(self, name: str) -> bool:
        if name in self.BUILT_IN.keys() or name == 'print':
            return True
        try:
            self.get_function(name)
            return True
        except e.UndeclaredVariableError:
            return False

    def get_return_value(self):
        return self.current_context.get_return_value()

    def set_return_value(self, value):
        self.current_context.set_return_value(value)

    def enter_context(self, name: str):
        self.current_context = Context(name, self.current_context)

    def exit_context(self):
        if self.current_context.parent:
            self.current_context = self.current_context.parent
        else:
            raise e.ContextNotFoundError(self.current_context.name)
