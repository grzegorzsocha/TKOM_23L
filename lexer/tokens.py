from enum import auto, Enum


class TokenType(Enum):
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    LIST = auto()
    POINT = auto()
    LINE = auto()
    POLYHEDRON = auto()
    COLLECTION = auto()
    WHILE = auto()
    IF = auto()
    ELSE = auto()
    OR = auto()
    AND = auto()
    TRUE = auto()
    FALSE = auto()
    VOID = auto()
    RETURN = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    ASSIGN = auto()
    GREATER = auto()
    LESS = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    DOT = auto()
    COMMA = auto()
    SEMI = auto()
    NOT = auto()
    COMMENT = auto()

    EQ = auto()
    NEQ = auto()
    LE = auto()
    GE = auto()

    IDENTIFIER = auto()
    INT_VALUE = auto()
    FLOAT_VALUE = auto()
    STRING_VALUE = auto()
    EOF = auto()


class Token:
    def __init__(self, type: TokenType, value: str | int | float | None, pos: tuple) -> None:
        self.type = type
        self.value = value
        self.pos = pos

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value}, {self.pos[0]}, {self.pos[1]})'


class Symbol:
    keywords = {
        'int': TokenType.INT,
        'float': TokenType.FLOAT,
        'bool': TokenType.BOOL,
        'string': TokenType.STRING,
        'List': TokenType.LIST,
        'Point': TokenType.POINT,
        'Line': TokenType.LINE,
        'Polyhedron': TokenType.POLYHEDRON,
        'Collection': TokenType.COLLECTION,
        'while': TokenType.WHILE,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'or': TokenType.OR,
        'and': TokenType.AND,
        'True': TokenType.TRUE,
        'False': TokenType.FALSE,
        'void': TokenType.VOID,
        'return': TokenType.RETURN
    }

    chars = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MUL,
        '/': TokenType.DIV,
        '=': TokenType.ASSIGN,
        '>': TokenType.GREATER,
        '<': TokenType.LESS,
        '(': TokenType.LPAREN,
        ')': TokenType.RPAREN,
        '{': TokenType.LBRACE,
        '}': TokenType.RBRACE,
        '.': TokenType.DOT,
        ',': TokenType.COMMA,
        ';': TokenType.SEMI,
        '!': TokenType.NOT,
        '#': TokenType.COMMENT
    }

    double_chars = {
        '==': TokenType.EQ,
        '!=': TokenType.NEQ,
        '<=': TokenType.LE,
        '>=': TokenType.GE,
    }
