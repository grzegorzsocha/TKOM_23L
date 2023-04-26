from lexer.tokens import Token, TokenType, Symbol
from lexer.source import FileSource, StringSource
from errors.errors import InvalidTokenError, ExceedsMaxLengthError


class Lexer:
    MAX_INT_LENGTH = 15
    MAX_FLOAT_LENGTH = 15
    MAX_STRING_LENGTH = 10 ** 5

    def __init__(self, source: FileSource | StringSource) -> None:
        self.source = source

    def get_current_char(self) -> str:
        return self.source.get_current_char()

    def get_next_char(self) -> str:
        return self.source.get_next_char()

    def get_position(self) -> tuple:
        return self.source.get_position()

    def skip_whitespaces(self) -> None:
        while self.get_current_char() == ' ':
            self.get_next_char()

    def skip_new_line(self) -> None:
        while self.get_current_char() in self.source.EOL:
            self.get_next_char()

    def try_build_identifier(self) -> Token:
        if self.get_current_char().isalpha():
            value = ''
            position = self.get_position()
            while self.get_current_char().isalnum() or self.get_current_char() == '_':
                value += self.get_current_char()
                self.get_next_char()
                if len(value) > self.MAX_STRING_LENGTH:
                    raise ExceedsMaxLengthError(self.get_position()[0], self.get_position()[1], 'Identifier')
            if value in Symbol.keywords:
                return Token(type=Symbol.keywords[value], value=value, pos=position)
            return Token(type=TokenType.IDENTIFIER, value=value, pos=position)

    def try_build_string(self) -> Token:
        if self.get_current_char() == '"':
            value = ''
            position = self.get_position()
            self.get_next_char()
            while self.get_current_char() != '"':
                value += self.get_current_char()
                self.get_next_char()
                if len(value) > self.MAX_STRING_LENGTH:
                    raise ExceedsMaxLengthError(self.get_position()[0], self.get_position()[1], 'String')
            self.get_next_char()
            return Token(type=TokenType.STRING_VALUE, value=value, pos=position)

    def try_build_comment(self) -> Token:
        if self.get_current_char() == '#':
            value = '#'
            position = self.get_position()
            self.get_next_char()
            while self.get_current_char() not in self.source.EOL and self.get_current_char() != '':
                value += self.get_current_char()
                self.get_next_char()
                if len(value) > self.MAX_STRING_LENGTH:
                    raise ExceedsMaxLengthError(self.get_position()[0], self.get_position()[1], 'Comment')
            return Token(type=TokenType.COMMENT, value=value, pos=position)

    def try_build_number(self) -> Token:
        if self.get_current_char().isdigit():
            value = ''
            position = self.get_position()
            while self.get_current_char().isdigit():
                value += self.get_current_char()
                self.get_next_char()
                if len(value) > self.MAX_INT_LENGTH:
                    raise ExceedsMaxLengthError(self.get_position()[0], self.get_position()[1], 'Integer')
            if self.get_current_char() == '.':
                value += self.get_current_char()
                self.get_next_char()
                while self.get_current_char().isdigit():
                    value += self.get_current_char()
                    self.get_next_char()
                    if len(value) > self.MAX_FLOAT_LENGTH:
                        raise ExceedsMaxLengthError(self.get_position()[0], self.get_position()[1], 'Float')
                return Token(type=TokenType.FLOAT_VALUE, value=float(value), pos=position)
            return Token(type=TokenType.INT_VALUE, value=int(value), pos=position)

    def try_build_chars(self) -> Token:
        if self.get_current_char() in Symbol.chars:
            value = self.get_current_char()
            position = self.get_position()
            if value in ['=', '!', '<', '>']:
                self.get_next_char()
                if self.get_current_char() == '=':
                    value += self.get_current_char()
                    self.get_next_char()
                    return Token(type=Symbol.double_chars[value], value=value, pos=position)
            self.get_next_char()
            return Token(type=Symbol.chars[value], value=value, pos=position)

    def try_build_eof(self) -> Token:
        if self.get_current_char() == '':
            position = (self.get_position()[0] + 1, self.get_position()[1])
            return Token(type=TokenType.EOF, value=None, pos=position)

    def get_next_token(self) -> Token:
        while (self.get_current_char() in self.source.EOL or self.get_current_char() == ' '):
            self.skip_new_line()
            self.skip_whitespaces()
        for fun in [self.try_build_identifier,
                    self.try_build_string,
                    self.try_build_comment,
                    self.try_build_number,
                    self.try_build_chars,
                    self.try_build_eof]:
            token = fun()
            if token:
                return token
        raise InvalidTokenError(self.get_position()[0], self.get_position()[1], self.get_current_char())

    def get_all_tokens(self) -> list[Token]:
        self.source.set_start_position()
        tokens = []
        token = self.get_next_token()
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        tokens.append(token)
        return tokens
