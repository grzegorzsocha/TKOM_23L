from lexer.lexer import Lexer
from lexer.source import FileSource
from parser.parser import Parser


if __name__ == '__main__':
    lexer = Lexer(FileSource('tests/test_cases/complex_code.txt'))
    parser = Parser(lexer)
    program = parser.parse_program()
    print(program)
