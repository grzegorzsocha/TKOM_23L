

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
