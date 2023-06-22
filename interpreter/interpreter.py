from lexer.lexer import Lexer
from lexer.source import FileSource, StringSource
from parser.parser import Parser
from interpreter.visitor import Visitor


class Interpreter:
    def __init__(self, file: bool, source: str):
        if file:
            self.lexer = Lexer(FileSource(source))
        else:
            self.lexer = Lexer(StringSource(source))
        self.parser = Parser(self.lexer)
        self.visitor = Visitor()

    def run(self):
        program = self.parser.parse_program()
        return program.accept(self.visitor)
