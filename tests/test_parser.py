from lexer.lexer import Lexer
from errors.errors import InvalidSyntaxError
from lexer.source import StringSource, FileSource
from parser.parser import Parser
import parser.nodes as nodes
import pytest


def test_parser_file_source_empty_file():
    lexer = Lexer(FileSource("tests/test_cases/empty_file.txt"))
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 0


def test_parser_function_declaration():
    source = StringSource('int main() { }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert program.functions[0].function_type.type == "int"
    assert program.functions[0].identifier.name == 'main'


def test_parser_function_declaration_with_parameters():
    source = StringSource('int main(int a, Collection b) { }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions[0].parameters) == 2
    assert program.functions[0].parameters[0].type.type == "int"
    assert program.functions[0].parameters[0].identifier.name == 'a'
    assert program.functions[0].parameters[1].type.type == "Collection"
    assert program.functions[0].parameters[1].identifier.name == 'b'


def test_parser_no_funtion_declaration():
    source = StringSource('print("Hello World")')
    lexer = Lexer(source)
    parser = Parser(lexer)
    with pytest.raises(InvalidSyntaxError):
        parser.parse_program()


def test_parser_return_statement():
    source = StringSource('int main() { return 7; }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.ReturnStatement)
    assert program.functions[0].block.statements[0].expression.value == 7


def test_parser_if_statement():
    source = StringSource('int main() { if (True) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.IfStatement)
    assert program.functions[0].block.statements[0].condition.value is True
    assert isinstance(program.functions[0].block.statements[0].block.statements[0], nodes.ReturnStatement)
    assert program.functions[0].block.statements[0].else_block is None


def test_parser_if_else_statement():
    source = StringSource('int main() { if (True) { return 7; } else { return 8; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.IfStatement)
    assert program.functions[0].block.statements[0].condition.value is True
    assert isinstance(program.functions[0].block.statements[0].block.statements[0], nodes.ReturnStatement)
    assert program.functions[0].block.statements[0].else_block is not None
    assert isinstance(program.functions[0].block.statements[0].else_block.statements[0], nodes.ReturnStatement)


def test_parser_while_statement():
    source = StringSource('int main() { while (True) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.WhileStatement)
    assert program.functions[0].block.statements[0].condition.value is True
    assert isinstance(program.functions[0].block.statements[0].block.statements[0], nodes.ReturnStatement)


def test_parser_declaration_statement():
    source = StringSource('int main() { int a = 7; }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.DeclarationStatement)
    assert program.functions[0].block.statements[0].variable_type.type == "int"
    assert program.functions[0].block.statements[0].identifier.name == 'a'
    assert program.functions[0].block.statements[0].expression.value == 7


def test_parser_declaration_without_initialization():
    source = StringSource('int main() { Collection a; }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.DeclarationStatement)
    assert program.functions[0].block.statements[0].variable_type.type == "Collection"
    assert program.functions[0].block.statements[0].identifier.name == 'a'
    assert program.functions[0].block.statements[0].expression is None


def test_parser_function_call():
    source = StringSource('int main() { print(); }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.FunctionCallStatement)
    assert program.functions[0].block.statements[0].identifier.name == 'print'
    assert len(program.functions[0].block.statements[0].arguments) == 0


def test_parser_function_call_with_arguments():
    source = StringSource('int main() { add(7, 5); }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.FunctionCallStatement)
    assert program.functions[0].block.statements[0].identifier.name == 'add'
    assert len(program.functions[0].block.statements[0].arguments) == 2
    assert program.functions[0].block.statements[0].arguments[0].value == 7
    assert program.functions[0].block.statements[0].arguments[1].value == 5


def test_parser_function_call_with_expression_arguments():
    source = StringSource('int main() { add(7 + 5, 5); }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.FunctionCallStatement)
    assert program.functions[0].block.statements[0].identifier.name == 'add'
    assert len(program.functions[0].block.statements[0].arguments) == 2
    assert isinstance(program.functions[0].block.statements[0].arguments[0], nodes.AdditiveExpression)
    assert program.functions[0].block.statements[0].arguments[0].left.value == 7
    assert program.functions[0].block.statements[0].arguments[0].right.value == 5
    assert program.functions[0].block.statements[0].arguments[1].value == 5


def test_parser_or_expression():
    source = StringSource('int main() { if (a > b or c < d) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.OrExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.left, nodes.ComparisonExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.right, nodes.ComparisonExpression)


def test_parser_and_expression():
    source = StringSource('int main() { if (a > c and True) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.AndExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.left, nodes.ComparisonExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.right, nodes.BoolValue)


def test_parser_comparison_expression():
    source = StringSource('int main() { if (a >= c) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.ComparisonExpression)
    assert program.functions[0].block.statements[0].condition.left.name == 'a'
    assert program.functions[0].block.statements[0].condition.right.name == 'c'
    assert program.functions[0].block.statements[0].condition.operator == ">="


def test_parser_arithmetic_expression():
    source = StringSource('int main() { if (a + c) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.AdditiveExpression)
    assert program.functions[0].block.statements[0].condition.left.name == 'a'
    assert program.functions[0].block.statements[0].condition.right.name == 'c'
    assert program.functions[0].block.statements[0].condition.operator == "+"


def test_parser_arithmetic_paretheis():
    source = StringSource('int main() { if ((a + c)) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.AdditiveExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.left, nodes.Identifier)
    assert isinstance(program.functions[0].block.statements[0].condition.right, nodes.Identifier)
    assert program.functions[0].block.statements[0].condition.operator == "+"


def test_parser_arithmetic_expression_with_precedence():
    source = StringSource('int main() { if (a + c + 7) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.AdditiveExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.left, nodes.AdditiveExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.right, nodes.IntValue)
    assert program.functions[0].block.statements[0].condition.left.operator == "+"


def test_parser_arithmetic_expression_with_precedence_and_parenthersis():
    source = StringSource('int main() { if ((a + c) + 7) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.AdditiveExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.left, nodes.AdditiveExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.right, nodes.IntValue)
    assert program.functions[0].block.statements[0].condition.left.operator == "+"


def test_parser_arithmetic_expression_with_precedence_with_parenthesis_not_in_order():
    source = StringSource('int main() { if (a + (c + 7)) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.AdditiveExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.left, nodes.Identifier)
    assert isinstance(program.functions[0].block.statements[0].condition.right, nodes.AdditiveExpression)
    assert program.functions[0].block.statements[0].condition.right.operator == "+"


def test_parser_arithmetic_expression_with_precedence_with_multiplication():
    source = StringSource('int main() { if (a + c * 7) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.AdditiveExpression)
    assert isinstance(program.functions[0].block.statements[0].condition.left, nodes.Identifier)
    assert isinstance(program.functions[0].block.statements[0].condition.right, nodes.MultiplicativeExpression)
    assert program.functions[0].block.statements[0].condition.operator == "+"
    assert program.functions[0].block.statements[0].condition.right.operator == "*"


def test_parser_multiplicative_expression():
    source = StringSource('int main() { if (a * c) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.MultiplicativeExpression)
    assert program.functions[0].block.statements[0].condition.left.name == 'a'
    assert program.functions[0].block.statements[0].condition.right.name == 'c'
    assert program.functions[0].block.statements[0].condition.operator == "*"


def test_parser_negation_expression():
    source = StringSource('int main() { if (!a) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.NegationExpression)
    assert program.functions[0].block.statements[0].condition.expression.name == 'a'


def test_parser_negation_expression_minus():
    source = StringSource('int main() { if (-a) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.NegationExpression)
    assert program.functions[0].block.statements[0].condition.expression.name == 'a'


def test_parser_negation_expression_with_parenthesis():
    source = StringSource('int main() { if (!(a)) { return 7; } }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].condition, nodes.NegationExpression)
    assert program.functions[0].block.statements[0].condition.expression.name == 'a'


def test_parser_method_call_expression():
    source = StringSource('int main() { return a.length(); }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].expression, nodes.MethodCallExpression)
    assert program.functions[0].block.statements[0].expression.caller.name == 'a'
    assert isinstance(program.functions[0].block.statements[0].expression.methods[0], nodes.MethodCall)
    assert program.functions[0].block.statements[0].expression.methods[0].name.name == 'length'


def test_parser_method_call_in_method_call():
    source = StringSource('int main() { return a.length().get(); }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert isinstance(program.functions[0].block.statements[0].expression, nodes.MethodCallExpression)
    assert program.functions[0].block.statements[0].expression.caller.name == 'a'
    assert isinstance(program.functions[0].block.statements[0].expression.methods[0], nodes.MethodCall)
    assert program.functions[0].block.statements[0].expression.methods[0].name.name == 'length'
    assert isinstance(program.functions[0].block.statements[0].expression.methods[1], nodes.MethodCall)
    assert program.functions[0].block.statements[0].expression.methods[1].name.name == 'get'
    assert len(program.functions[0].block.statements[0].expression.methods[1].arguments) == 0


def test_parser_skip_comment():
    source = StringSource('int main() { # comment\n return 7; }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions[0].block.statements) == 1
    assert isinstance(program.functions[0].block.statements[0], nodes.ReturnStatement)


def test_parser_void_function():
    source = StringSource('void foo() { print("foo"); }')
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert program.functions[0].identifier.name == 'foo'
    assert program.functions[0].function_type.type == 'void'
    assert len(program.functions[0].parameters) == 0
    assert len(program.functions[0].block.statements) == 1


def test_parser_simple_code():
    lexer = Lexer(FileSource('tests/test_cases/simple_code.txt'))
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 1
    assert program.functions[0].identifier.name == 'main'
    assert len(program.functions[0].parameters) == 0


def test_parser_simple_code_2():
    lexer = Lexer(FileSource('tests/test_cases/simple_code_2.txt'))
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 2
    assert program.functions[0].identifier.name == 'add'
    assert program.functions[1].identifier.name == 'main'
    assert len(program.functions[0].parameters) == 2
    assert program.functions[0].parameters[0].identifier.name == 'a'
    assert program.functions[0].parameters[1].identifier.name == 'b'


def test_parser_complex_code():
    lexer = Lexer(FileSource('tests/test_cases/complex_code.txt'))
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.functions) == 2
