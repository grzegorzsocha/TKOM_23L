

class InvalidTokenError(Exception):
    """Exception raised when lexer meets invalid token

    Attributes:
        column -- column where error occured
        line -- line where error occured
        char -- invalid character
    """

    def __init__(self, column, line, char):
        text = f'Error occured in line {line}, column {column}:'
        text += f'\nInvalid character \'{char}\''
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ExceedsMaxLengthError(Exception):
    """Exception raised when created number or string is too long

    Attributes:
        column -- column where error occured
        line -- line where error occured
        message -- type of value
    """

    def __init__(self, column, line, message=""):
        text = f'Error occured in line {line}, column {column}:'
        text += f'\n{message} exceeds max length'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidSyntaxError(Exception):
    """Exception raised when parser meets invalid syntax

    Attributes:
        column -- column where error occured
        line -- line where error occured
        message -- type of value
    """

    def __init__(self, column, line, message=""):
        text = f'Error occured in line {line}, column {column}:'
        text += '\nInvalid syntax: ' + message
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class MainFunctionNotFoundError(Exception):
    """Exception raised when visitor doesn't find main function

    Attributes:
        message -- text to display
    """

    def __init__(self):
        self.message = "Main function not found"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class RedefinitionError(Exception):
    """Exception raised when visitor finds redefinition of variable or function

    Attributes:
        message -- variable or function name
    """

    def __init__(self, message=""):
        text = 'Redefinition oocured:'
        text += f'\n\'{message}\' already exists'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class UndeclaredVariableError(Exception):
    """Exception raised when visitor finds undeclared variable

    Attributes:
        message -- variable name
    """

    def __init__(self, message=""):
        text = 'Variable undeclared:'
        text += f'\nVariable \'{message}\' is not declared'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class UndeclaredFunctionError(Exception):
    """Exception raised when visitor finds undeclared function

    Attributes:
        message -- function name
    """

    def __init__(self, message=""):
        text = 'Function undeclared:'
        text += f'\nFunction \'{message}\' is not declared'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ContextNotFoundError(Exception):
    """Exception raised when context manager doesn't find parent context

    Attributes:
        message -- context name
    """

    def __init__(self, message=""):
        text = 'Context not found:'
        text += f'While exiting \'{message}\', parent context not found'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidConditionError(Exception):
    """Exception raised when visitor finds invalid condition

    Attributes:
        message -- condition
    """

    def __init__(self, message=""):
        text = 'Invalid condition:'
        text += f'\n\'{message}\' is not a valid bool-type condition'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class TypeMismatchError(Exception):
    """Exception raised when visitor finds type mismatch

    Attributes:
        message -- type of value
    """

    def __init__(self, message=""):
        text = 'Type mismatch:'
        text += f'\n{message} is not a valid type'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidNumberOfArgumentsError(Exception):
    """Exception raised when visitor finds invalid number of arguments

    Attributes:
        message -- function name
    """

    def __init__(self, message=""):
        text = 'Invalid number of arguments:'
        text += f'\nFunction \'{message}\' called with invalid number of arguments'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidMethodCallError(Exception):
    """Exception raised when visitor finds invalid method call

    Attributes:
        message -- method name
    """

    def __init__(self, object, method_name):
        text = 'Invalid method call:'
        text += f'\nYou cannot call method \'{method_name}\' on object of type \'{object}\''
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidReturnTypeError(Exception):
    """Exception raised when visitor finds invalid return type

    Attributes:
        return_type -- type of return type
        expected_type -- expected type of return type
    """

    def __init__(self, expected_type, return_type):
        text = 'Invalid return type:'
        text += f'\nExxpected type \'{expected_type}\', got \'{return_type}\''
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidTypeError(Exception):
    """Exception raised when visitor finds invalid type

    Attributes:
        message -- type of value
    """

    def __init__(self, message=""):
        text = 'Invalid type:'
        text += f'\n{message}'
        self.message = text
        super().__init__(self.message)

    def __str__(self):
        return self.message
