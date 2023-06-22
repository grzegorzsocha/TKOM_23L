from interpreter.interpreter import Interpreter
import errors.errors as e
import pytest


def test_interpreter_no_main():
    code = 'int not_a_main() { return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.MainFunctionNotFoundError):
        interpreter.run()


def test_interpreter_main_invalid_type():
    code = 'void main() { }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.MainFunctionNotFoundError):
        interpreter.run()


def test_interpreter_main_no_return():
    code = 'int main() { }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidReturnTypeError):
        interpreter.run()


def test_interpreter_two_main():
    code = 'int main() { return 0; } int main() { return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.RedefinitionError):
        interpreter.run()


def test_interpreter_many_functions(capfd):
    code = 'int main() { print(f1()); print(f2()); return 0; } '
    code += 'int f1() { return 1; } int f2() { return 2; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == '1\n2\n'


def test_interpreter_return_zero():
    code = 'int main() { return 0; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 0


def test_interpreter_return_statement():
    code = 'int main() { return 37; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 37


def test_interpreter_return_statement_code_after():
    code = 'int main() { return 37; return 42; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 37


def test_interpreter_return_statement_invalid_type():
    code = 'int main() { return True; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidReturnTypeError):
        interpreter.run()


def test_interpreter_additive_expression_add():
    code = 'int main() { return 1 + 2; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 3


def test_interpreter_additive_expression_sub():
    code = 'int main() { return 3 - 2; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 1


def test_interpreter_multiplicative_expression_mul():
    code = 'int main() { return 2 * 3; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 6


def test_interpreter_multiplicative_expression_div(capfd):
    code = 'int main() { print(6 / 3); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == '2.0\n'


def test_interpreter_comparison_expression_eq(capfd):
    code = 'int main() { print(1 == 1); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'True\n'


def test_interpreter_comparison_expression_neq(capfd):
    code = 'int main() { print(1 != 1); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'False\n'


def test_interpreter_comparison_expression_lt(capfd):
    code = 'int main() { print(1 < 2); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'True\n'


def test_interpreter_comparison_expression_gt(capfd):
    code = 'int main() { print(2 > 1); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'True\n'


def test_interpreter_comparison_expression_le(capfd):
    code = 'int main() { print(1 <= 1); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'True\n'


def test_interpreter_comparison_expression_ge(capfd):
    code = 'int main() { print(1 >= 1); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'True\n'


def test_interpreter_and_expression(capfd):
    code = 'int main() { print(True and False); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'False\n'


def test_interpreter_or_expression(capfd):
    code = 'int main() { print(False or True); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'True\n'


def test_interpreter_not_expression(capfd):
    code = 'int main() { print(!False); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'True\n'


def test_interpreter_not_expression_variable(capfd):
    code = 'int main() { bool a = False; print(!a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == 'True\n'


def test_interpreter_not_expression_minus(capfd):
    code = 'int main() { print(-1); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == '-1\n'


def test_interpreter_assignment_expression(capfd):
    code = 'int main() { int a = 1; a = 4; print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    out, err = capfd.readouterr()
    assert out == '4\n'


def test_interpreter_if_statement():
    code = 'int main() { if (True) { return 2; } }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 2


def test_interpreter_if_statement_else():
    code = 'int main() { if (False) { return 0; } else { return 1; } }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 1


def test_interpreter_if_statement_complex_condition():
    code = 'int main() { int a = 0; int b = 1;if (True and b > 0 or a + b == b) '
    code += '{ return 0; } else { return 1; } }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 0


def test_interpreter_if_statement_condition_not_bool():
    code = 'int main() { if (1) { return 0; } else { return 1; } }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidConditionError):
        interpreter.run()


def test_interpreter_if_statement_condition_assingment():
    code = 'int main() { int a = 1; if (a = 2) { return 0; } else { return 1; } }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidSyntaxError):
        interpreter.run()


def test_interpreter_while_statement():
    code = 'int main() { int a = 0; while (a < 5) { a = a + 1; } return a; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 5


def test_interpreter_while_statement_False_condition():
    code = 'int main() { int a = 0; while (False) { a = a + 1; } return a; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 0


def test_interpreter_while_statement_condition_not_bool():
    code = 'int main() { int a = 0; while (a) { a = a + 1; } return a; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidConditionError):
        interpreter.run()


def test_interpreter_int_declaration():
    code = 'int main() { int a = 5; return a; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 5


def test_interpreter_int_declaration_without_assignment():
    code = 'int main() { int a; return a; }'
    interpreter = Interpreter(False, code)
    assert interpreter.run() == 0


def test_interpreter_float_declaration(capfd):
    code = 'int main() { float a = 5.5; print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "5.5\n"


def test_interpreter_float_declaration_without_assignment(capfd):
    code = 'int main() { float a; print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "0.0\n"


def test_interpreter_string_declaration(capfd):
    code = 'int main() { string a = "Hello world!"; print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Hello world!\n"


def test_interpreter_string_declaration_without_assignment(capfd):
    code = 'int main() { string a; print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "\n"


def test_interpreter_bool_declaration(capfd):
    code = 'int main() { bool a = True; print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "True\n"


def test_interpreter_bool_declaration_without_assignment(capfd):
    code = 'int main() { bool a; print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "False\n"


def test_interpreter_point_declaration(capfd):
    code = 'int main() { Point a = Point(1, 2, 1); print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Point(1, 2, 1)\n"


def test_interpreter_point_declaration_invalid_number_of_arguments():
    code = 'int main() { Point a = Point(1, 2, 1, 1); print(a); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidNumberOfArgumentsError):
        interpreter.run()


def test_interpreter_point_declaration_invalid_type_of_arguments():
    code = 'int main() { Point a = Point(1, 2, "1"); print(a); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidTypeError):
        interpreter.run()


def test_interpreter_point_declaration_with_variable(capfd):
    code = 'int main() { int x = 1; int y = 2; int z = 1;'
    code += 'Point a = Point(x, y, z); print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Point(1, 2, 1)\n"


def test_interpreter_point_declaration_with_invalid_variable(capfd):
    code = 'int main() { int x = 1; int y = 2; string z = "1";'
    code += 'Point a = Point(x, y, z); print(a); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidTypeError):
        interpreter.run()


def test_interpreter_line_declaration(capfd):
    code = 'int main() { Point a = Point(1, 2, 1); Point b = Point(2, 3, 1);'
    code += 'Line l = Line(a, b); print(l); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Line(Point(1, 2, 1), Point(2, 3, 1))\n"


def test_interpreter_line_declaration_invalid_number_of_arguments():
    code = 'int main() { Point a = Point(1, 2, 1);'
    code += 'Line l = Line(a); print(l); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidNumberOfArgumentsError):
        interpreter.run()


def test_interpreter_line_declaration_invalid_type_of_arguments():
    code = 'int main() { Point a = Point(1, 2, 1);'
    code += 'Line l = Line(a, True); print(l); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidTypeError):
        interpreter.run()


def test_interpreter_line_declaration_with_invalid_variable():
    code = 'int main() { int x = 1; int y = 2; string z = "1";'
    code += 'Point a = Point(x, y, z); print(a); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidTypeError):
        interpreter.run()


def test_interpreter_line_declaration_without_point_preassignment(capfd):
    code = 'int main() { Line l = Line(Point(1, 1, 1),'
    code += 'Point(2, 2, 2)); print(l); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Line(Point(1, 1, 1), Point(2, 2, 2))\n"


def test_interpreter_polyhedron_declaration(capfd):
    code = 'int main() { Point a = Point(0, 0, 0); Point b = Point(1, 0, 0); '
    code += 'Point c = Point(0, 1, 0); Point d = Point(0.5, 0.5, 3); '
    code += 'Line ac = Line(a, c); Line ad = Line(a, d); Line bc = Line(b, c); '
    code += 'Line bd = Line(b, d); Line cd = Line(c, d); Line ab = Line(a, b); '
    code += 'Polyhedron p = Polyhedron(ac, ad, bc, bd, cd, ab); print(p); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    result = "Polyhedron[Line(Point(0, 0, 0), Point(0, 1, 0)), Line(Point(0, 0, 0), "
    result += "Point(0.5, 0.5, 3)), Line(Point(1, 0, 0), Point(0, 1, 0)), "
    result += "Line(Point(1, 0, 0), Point(0.5, 0.5, 3)), Line(Point(0, 1, 0), "
    result += "Point(0.5, 0.5, 3)), Line(Point(0, 0, 0), Point(1, 0, 0))]\n"
    assert captured.out == result


def test_interpreter_polyhedron_declaration_invalid_number_of_arguments():
    code = 'int main() { Polyhedron p = Polyhedron(); print(p); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidNumberOfArgumentsError):
        interpreter.run()


def test_interpreter_polyhedron_declaration_invalid_type_of_arguments():
    code = 'int main() { int a = 3; Polyhedron p = Polyhedron(a);'
    code += ' print(p); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidTypeError):
        interpreter.run()


def test_interpreter_polyhedron_declaration_without_preassignment(capfd):
    code = 'int main() { Polyhedron p = Polyhedron(Line(Point(0, 0, 0), '
    code += 'Point(0, 1, 0)), Line(Point(0, 0, 0), Point(0.5, 0.5, 3)), '
    code += 'Line(Point(1, 0, 0), Point(0, 1, 0)), Line(Point(1, 0, 0), '
    code += 'Point(0.5, 0.5, 3)), Line(Point(0, 1, 0), Point(0.5, 0.5, 3)), '
    code += 'Line(Point(0, 0, 0), Point(1, 0, 0))); print(p); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    result = "Polyhedron[Line(Point(0, 0, 0), Point(0, 1, 0)), Line(Point(0, 0, 0), "
    result += "Point(0.5, 0.5, 3)), Line(Point(1, 0, 0), Point(0, 1, 0)), "
    result += "Line(Point(1, 0, 0), Point(0.5, 0.5, 3)), Line(Point(0, 1, 0), "
    result += "Point(0.5, 0.5, 3)), Line(Point(0, 0, 0), Point(1, 0, 0))]\n"
    assert captured.out == result


def test_interpreter_collection_declaration(capfd):
    code = 'int main() { Point a = Point(0, 0, 0); Point b = Point(1, 0, 0); '
    code += 'Point c = Point(0, 1, 0); Point d = Point(0.5, 0.5, 3); '
    code += 'Line ac = Line(a, c); Line ad = Line(a, d); Line bc = Line(b, c); '
    code += 'Line bd = Line(b, d); Line cd = Line(c, d); Line ab = Line(a, b); '
    code += 'Polyhedron p = Polyhedron(ac, ad, bc, bd, cd, ab); '
    code += 'Collection scene = Collection(p); print(scene); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    print(captured.out)
    result = "Collection[Polyhedron[Line(Point(0, 0, 0), Point(0, 1, 0)), "
    result += "Line(Point(0, 0, 0), Point(0.5, 0.5, 3)), Line(Point(1, 0, 0), "
    result += "Point(0, 1, 0)), Line(Point(1, 0, 0), Point(0.5, 0.5, 3)), "
    result += "Line(Point(0, 1, 0), Point(0.5, 0.5, 3)), Line(Point(0, 0, 0), "
    result += "Point(1, 0, 0))]]\n"
    assert captured.out == result


def test_interpreter_collection_declaration_no_arguments(capfd):
    code = 'int main() { Collection scene = Collection(); print(scene); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    result = "Collection[]\n"
    assert captured.out == result


def test_interpreter_collection_declaration_invalid_type_of_arguments():
    code = 'int main() { int a = 3; Collection scene = Collection(a);'
    code += ' print(scene); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidTypeError):
        interpreter.run()


def test_interpreter_collection_declaration_without_preassignment(capfd):
    code = 'int main() { Point a = Point(0, 0, 0); Point b = Point(1, 0, 0); '
    code += 'Point c = Point(0, 1, 0); Point d = Point(0.5, 0.5, 3); '
    code += 'Line ac = Line(a, c); Line ad = Line(a, d); Line bc = Line(b, c); '
    code += 'Line bd = Line(b, d); Line cd = Line(c, d); Line ab = Line(a, b); '
    code += 'Collection scene = Collection(Polyhedron(ac, ad, bc, bd, cd, ab)); '
    code += 'print(scene); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    result = "Collection[Polyhedron[Line(Point(0, 0, 0), Point(0, 1, 0)), "
    result += "Line(Point(0, 0, 0), Point(0.5, 0.5, 3)), Line(Point(1, 0, 0), "
    result += "Point(0, 1, 0)), Line(Point(1, 0, 0), Point(0.5, 0.5, 3)), "
    result += "Line(Point(0, 1, 0), Point(0.5, 0.5, 3)), Line(Point(0, 0, 0), "
    result += "Point(1, 0, 0))]]\n"
    assert captured.out == result


def test_interpreter_list_declaration(capfd):
    code = 'int main() { List l = List(); print(l); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "List[]\n"


def test_interpreter_list_declaration_with_arguments(capfd):
    code = 'int main() { List l = List(1, 2, 3); print(l); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "List[1, 2, 3]\n"


def test_interpreter_list_declaration_different_types(capfd):
    code = 'int main() { List l = List(1, 2.5, "string"); print(l); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "List[1, 2.5, string]\n"


def test_interpreter_execute_print(capfd):
    code = 'int main() { print("Hello world!"); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Hello world!\n"


def test_interpreter_execute_print_with_variable(capfd):
    code = 'int main() { int a = 5; print(a); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "5\n"


def test_interpreter_execute_print_without_parameters():
    code = 'int main() { print(); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidNumberOfArgumentsError):
        interpreter.run()


def test_interpreter_call_function(capfd):
    code = 'int add(int a, int b) { return a + b; }int main() '
    code += '{ int a = 5; int b = 3; int c = add(a, b); print(c); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "8\n"


def test_interpreter_call_function_with_wrong_number_of_arguments():
    code = 'int add(int a, int b) { return a + b; }int main() '
    code += '{ int a = 5; int b = 3; int c = add(a); print(c); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidNumberOfArgumentsError):
        interpreter.run()


def test_interpreter_call_function_with_wrong_type_of_arguments():
    code = 'int add(int a, int b) { return a + b; }int main() '
    code += '{ int a = 5; float b = 3.5; int c = add(a, b); print(c); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.TypeMismatchError):
        interpreter.run()


def test_interpreter_call_function_void_type(capfd):
    code = 'void printHello() { print("Hello world!"); }int main() '
    code += '{ printHello(); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Hello world!\n"


def test_interpreter_call_function_void_type_with_return():
    code = 'void printHello() { print("Hello world!"); return 1; }int main() '
    code += '{ printHello(); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidReturnTypeError):
        interpreter.run()


def test_interpreter_call_function_complex_type(capfd):
    code = 'Point create_point(int x, int y, int z) { return Point(x, y, z); } '
    code += 'int main() { Point p = create_point(1, 2, 3); print(p); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Point(1, 2, 3)\n"


def test_interpreter_void_function(capfd):
    code = 'void printHello() { print("Hello world!"); } int main() '
    code += '{ printHello(); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Hello world!\n"


def test_interpreter_void_function_with_return():
    code = 'void printHello() { return "Hello world!"; } int main() '
    code += '{ printHello(); return 1; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidReturnTypeError):
        interpreter.run()


def test_interpreter_method_calls_list(capfd):
    code = 'int main() { List a = List(); a.add(1); print(a.get(0)); print(a.length());'
    code += 'a.remove(0); print(a.length()); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "1\n1\n0\n"


def test_interpreter_method_calls_list_with_wrong_number_of_arguments():
    code = 'int main() { List a = List(); a.add(); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(TypeError):
        interpreter.run()


def test_interpreter_method_calls_list_remove_out_of_bounds():
    code = 'int main() { List a = List(); a.remove(0); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(IndexError):
        interpreter.run()


def test_interpreter_method_calls_point(capfd):
    code = 'int main() { Point a = Point(1, 2, 3); print(a.get_x()); print(a.get_y());'
    code += 'print(a.get_z()); a.set_x(5); a.set_y(6); a.set_z(7); print(a.get_x());'
    code += 'print(a.get_y()); print(a.get_z()); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "1\n2\n3\n5\n6\n7\n"


def test_interpreter_method_calls_point_with_wrong_number_of_arguments():
    code = 'int main() { Point a = Point(1, 2, 3); a.get_x(1); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(TypeError):
        interpreter.run()


def test_interpreter_method_calls_point_with_wrong_type_of_arguments():
    code = 'int main() { Point a = Point(1, 2, 3); a.set_x(True); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.TypeMismatchError):
        interpreter.run()


def test_interpreter_method_calls_point_with_wrong_method():
    code = 'int main() { Point a = Point(1, 2, 3); a.get_w(); return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidMethodCallError):
        interpreter.run()


def test_interpreter_method_calls_line(capfd):
    code = 'int main() { Line a = Line(Point(1, 2, 3), Point(4, 5, 6)); '
    code += 'print(a.get_start()); print(a.get_end()); a.set_start(Point(7, 8, 9));'
    code += 'a.set_end(Point(10, 11, 12)); print(a.get_start()); print(a.get_end());'
    code += 'return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == "Point(1, 2, 3)\nPoint(4, 5, 6)\nPoint(7, 8, 9)\nPoint(10, 11, 12)\n"


def test_interpreter_method_calls_line_with_wrong_number_of_arguments():
    code = 'int main() { Line a = Line(Point(1, 2, 3), Point(4, 5, 6)); a.get_start(1);'
    code += 'return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(TypeError):
        interpreter.run()


def test_interpreter_method_calls_line_with_wrong_type_of_arguments():
    code = 'int main() { Line a = Line(Point(1, 2, 3), Point(4, 5, 6)); a.set_start(True);'
    code += 'return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.TypeMismatchError):
        interpreter.run()


def test_interpreter_method_calls_line_with_wrong_method():
    code = 'int main() { Line a = Line(Point(1, 2, 3), Point(4, 5, 6)); a.get_w();'
    code += 'return 0; }'
    interpreter = Interpreter(False, code)
    with pytest.raises(e.InvalidMethodCallError):
        interpreter.run()


def test_interpreter_method_calls_polyhedron_lines(capfd):
    code = 'int main() { Point a = Point(0, 0, 0); Point b = Point(1, 0, 0); '
    code += 'Point c = Point(0, 1, 0); Point d = Point(0.5, 0.5, 3); '
    code += 'Line ac = Line(a, c); Line ad = Line(a, d); Line bc = Line(b, c); '
    code += 'Line bd = Line(b, d); Line cd = Line(c, d); Line ab = Line(a, b); '
    code += 'Polyhedron p = Polyhedron(ac, ad, bc, bd, cd, ab); print(p.lines());'
    code += ' return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    result = 'List[Line(Point(0, 0, 0), Point(0, 1, 0)), Line(Point(0, 0, 0), Point(0.5, 0.5, 3)),'
    result += ' Line(Point(1, 0, 0), Point(0, 1, 0)), Line(Point(1, 0, 0), Point(0.5, 0.5, 3)),'
    result += ' Line(Point(0, 1, 0), Point(0.5, 0.5, 3)), Line(Point(0, 0, 0), Point(1, 0, 0))]\n'
    assert captured.out == result


def test_interpreter_method_calls_polyhedron_points(capfd):
    code = 'int main() { Point a = Point(0, 0, 0); Point b = Point(1, 0, 0); '
    code += 'Point c = Point(0, 1, 0); Point d = Point(0.5, 0.5, 3); '
    code += 'Line ac = Line(a, c); Line ad = Line(a, d); Line bc = Line(b, c); '
    code += 'Line bd = Line(b, d); Line cd = Line(c, d); Line ab = Line(a, b); '
    code += 'Polyhedron p = Polyhedron(ac, ad, bc, bd, cd, ab); print(p.points());'
    code += ' return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    result = 'List[Point(0, 0, 0), Point(0, 1, 0), Point(0.5, 0.5, 3), Point(1, 0, 0)]\n'
    assert captured.out == result


def test_interpreter_method_calls_collection(capfd):
    code = 'int main() { Point a = Point(0, 0, 0); Point b = Point(1, 0, 0); '
    code += 'Point c = Point(0, 1, 0); Point d = Point(0.5, 0.5, 3); '
    code += 'Line ac = Line(a, c); Line ad = Line(a, d); Line bc = Line(b, c); '
    code += 'Line bd = Line(b, d); Line cd = Line(c, d); Line ab = Line(a, b); '
    code += 'Polyhedron p = Polyhedron(ac, ad, bc, bd, cd, ab); '
    code += 'Collection cl = Collection();  cl.add(p); cl.remove(p); print(cl);'
    code += ' return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == 'Collection[]\n'


def test_interpreter_method_call_on_method_call(capfd):
    code = 'int main() { Point a = Point(0, 0, 0); Point b = Point(1, 0, 0); '
    code += 'Line ac = Line(a, b); print(ac.get_start().get_x()); return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == '0\n'


def test_interpreter_multiple_method_call(capfd):
    code = 'int main() { Point a = Point(0, 0, 0); Point b = Point(1, 0, 0); '
    code += 'Point c = Point(0, 1, 0); Point d = Point(0.5, 0.5, 3); '
    code += 'Line ac = Line(a, c); Line ad = Line(a, d); Line bc = Line(b, c); '
    code += 'Line bd = Line(b, d); Line cd = Line(c, d); Line ab = Line(a, b); '
    code += 'Polyhedron p = Polyhedron(ac, ad, bc, bd, cd, ab); '
    code += 'print(p.lines().get(0).get_start().get_x());'
    code += ' return 0; }'
    interpreter = Interpreter(False, code)
    interpreter.run()
    captured = capfd.readouterr()
    assert captured.out == '0\n'
