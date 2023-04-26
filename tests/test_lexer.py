from lexer.lexer import Lexer, TokenType
from lexer.source import StringSource, FileSource
from errors.errors import InvalidTokenError, ExceedsMaxLengthError
import pytest
import re


def test_source_create():
    source = StringSource("a")
    assert source.get_current_char() == 'a'
    assert source.get_position() == (1, 1)


def test_source_get_position():
    source = StringSource("a")
    assert source.get_position() == (1, 1)


def test_source_get_current_char():
    source = StringSource("a")
    assert source.get_current_char() == 'a'


def test_source_get_next_char():
    source = StringSource("a")
    assert source.get_current_char() == 'a'
    source.get_next_char()
    assert source.get_current_char() == ''


def test_source_set_start_position():
    source = StringSource("ab")
    source.get_next_char()
    assert source.get_position() == (2, 1)
    assert source.get_current_char() == 'b'
    source.set_start_position()
    assert source.get_current_char() == 'a'
    assert source.get_position() == (1, 1)


def test_source_get_line():
    source = StringSource("a\nb")
    assert source.get_line(1) == "a\n"
    assert source.get_line(2) == "b"
    assert source.get_line(3) == ""


def test_lexer_skip_spaces():
    lexer = Lexer(StringSource("              a"))
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "a"
    assert token.pos == (15, 1)


def test_lexer_skip_new_lines():
    lexer = Lexer(StringSource("\n \n \na"))
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "a"
    assert token.pos == (1, 4)


def test_lexer_skip_spaces_and_new_lines():
    lexer = Lexer(StringSource("  \n  \n  \n a"))
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "a"
    assert token.pos == (2, 4)


def test_lexer_identifier():
    lexer = Lexer(StringSource("a a_dwa a_2"))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 4
    for token in tokens[:-1]:
        assert token.type == TokenType.IDENTIFIER
    assert tokens[0].value == "a"
    assert tokens[1].value == "a_dwa"
    assert tokens[2].value == "a_2"


def test_lexer_identifier_overflow():
    lexer = Lexer(StringSource("a" * 100000000))
    with pytest.raises(ExceedsMaxLengthError):
        lexer.get_next_token()


def test_lexer_identifier_overflow_text():
    lexer = Lexer(StringSource("a" * 100000000))
    text = "Error occured in line 1, column 100002:\nIdentifier exceeds max length"
    escaped_text = re.escape(text)
    with pytest.raises(ExceedsMaxLengthError, match=escaped_text):
        lexer.get_next_token()


def test_lexer_int_values():
    lexer = Lexer(StringSource("100 0 123123412"))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 4
    for token in tokens[:-1]:
        assert token.type == TokenType.INT_VALUE
    assert tokens[0].value == 100
    assert tokens[1].value == 0
    assert tokens[2].value == 123123412


def test_lexer_int_overflow():
    lexer = Lexer(StringSource("1231234124124124124124124"))
    with pytest.raises(ExceedsMaxLengthError):
        lexer.get_next_token()


def test_lexer_int_overflow_text():
    lexer = Lexer(StringSource("1231234124124124124124124"))
    text = "Error occured in line 1, column 17:\nInteger exceeds max length"
    escaped_text = re.escape(text)
    with pytest.raises(ExceedsMaxLengthError, match=escaped_text):
        lexer.get_next_token()


def test_lexer_float_values():
    lexer = Lexer(StringSource("0.0 1.5 42.9999"))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 4
    for token in tokens[:-1]:
        assert token.type == TokenType.FLOAT_VALUE
    assert tokens[0].value == 0.0
    assert tokens[1].value == 1.5
    assert tokens[2].value == 42.9999


def test_lexer_float_overflow():
    lexer = Lexer(StringSource("0.1231234124124124124124124"))
    with pytest.raises(ExceedsMaxLengthError):
        lexer.get_next_token()


def test_lexer_float_overflow_text():
    lexer = Lexer(StringSource("0.1231234124124124124124124"))
    text = "Error occured in line 1, column 17:\nFloat exceeds max length"
    escaped_text = re.escape(text)
    with pytest.raises(ExceedsMaxLengthError, match=escaped_text):
        lexer.get_next_token()


def test_lexer_string_values():
    lexer = Lexer(StringSource('"a" "a b" "a $^#2D c"'))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 4
    for token in tokens[:-1]:
        assert token.type == TokenType.STRING_VALUE
    assert tokens[0].value == "a"
    assert tokens[1].value == "a b"
    assert tokens[2].value == "a $^#2D c"


def test_lexer_string_values_with_escape_chars():
    lexer = Lexer(StringSource(' "a\t" "a\n" "a\\\\" "a \r"  "\'a\'" '))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 6
    for token in tokens[:-1]:
        assert token.type == TokenType.STRING_VALUE
    assert tokens[0].value == "a\t"
    assert tokens[1].value == "a\n"
    assert tokens[2].value == "a\\\\"
    assert tokens[3].value == "a \r"
    assert tokens[4].value == "'a'"


def test_lexer_chars():
    lexer = Lexer(StringSource("+ * { ( , ; "))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 7
    assert tokens[0].type == TokenType.PLUS
    assert tokens[1].type == TokenType.MUL
    assert tokens[2].type == TokenType.LBRACE
    assert tokens[3].type == TokenType.LPAREN
    assert tokens[4].type == TokenType.COMMA
    assert tokens[5].type == TokenType.SEMI


def test_lexer_double_chars():
    lexer = Lexer(StringSource("== != >= <="))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 5
    assert tokens[0].type == TokenType.EQ
    assert tokens[1].type == TokenType.NEQ
    assert tokens[2].type == TokenType.GE
    assert tokens[3].type == TokenType.LE


def test_lexer_keywords():
    lexer = Lexer(StringSource("int float List Point Line Collection true and void return"))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 11
    assert tokens[0].type == TokenType.INT
    assert tokens[1].type == TokenType.FLOAT
    assert tokens[2].type == TokenType.LIST
    assert tokens[3].type == TokenType.POINT
    assert tokens[4].type == TokenType.LINE
    assert tokens[5].type == TokenType.COLLECTION
    assert tokens[6].type == TokenType.TRUE
    assert tokens[7].type == TokenType.AND
    assert tokens[8].type == TokenType.VOID
    assert tokens[9].type == TokenType.RETURN


def test_lexer_some_code():
    lexer = Lexer(StringSource("int a = 1;\n while (a < 10) { a = a + 1; }"))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 20
    assert tokens[0].type == TokenType.INT
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[2].type == TokenType.ASSIGN
    assert tokens[3].type == TokenType.INT_VALUE
    assert tokens[4].type == TokenType.SEMI
    assert tokens[5].type == TokenType.WHILE
    assert tokens[6].type == TokenType.LPAREN
    assert tokens[7].type == TokenType.IDENTIFIER
    assert tokens[8].type == TokenType.LESS
    assert tokens[9].type == TokenType.INT_VALUE
    assert tokens[10].type == TokenType.RPAREN
    assert tokens[11].type == TokenType.LBRACE
    assert tokens[12].type == TokenType.IDENTIFIER
    assert tokens[13].type == TokenType.ASSIGN
    assert tokens[14].type == TokenType.IDENTIFIER
    assert tokens[15].type == TokenType.PLUS
    assert tokens[16].type == TokenType.INT_VALUE
    assert tokens[17].type == TokenType.SEMI
    assert tokens[18].type == TokenType.RBRACE
    assert tokens[19].type == TokenType.EOF


def test_lexer_comment_value():
    lexer = Lexer(StringSource("# some comment"))
    token = lexer.get_next_token()
    assert token.type == TokenType.COMMENT
    assert token.value == "# some comment"


def test_lexer_comment_overflow():
    lexer = Lexer(StringSource("#" * 100000000))
    with pytest.raises(ExceedsMaxLengthError):
        lexer.get_next_token()


def test_lexer_comment_overflow_text():
    lexer = Lexer(StringSource("#" * 100000000))
    text = "Error occured in line 1, column 100002:\nComment exceeds max length"
    escaped_text = re.escape(text)
    with pytest.raises(ExceedsMaxLengthError, match=escaped_text):
        lexer.get_next_token()


def test_lexer_invalid_token():
    lexer = Lexer(StringSource("$"))
    with pytest.raises(InvalidTokenError):
        lexer.get_next_token()


def test_lexer_invalid_token_text():
    lexer = Lexer(StringSource("$"))
    text = "Error occured in line 1, column 1:\nInvalid character '$'"
    escaped_text = re.escape(text)
    with pytest.raises(InvalidTokenError, match=escaped_text):
        lexer.get_next_token()


def test_lexer_invalid_token_get_all_text():
    lexer = Lexer(StringSource("int a = 14;\nstri%ng b = \"hello\";"))
    text = "Error occured in line 2, column 5:\nInvalid character '%'"
    escaped_text = re.escape(text)
    with pytest.raises(InvalidTokenError, match=escaped_text):
        lexer.get_all_tokens()


def test_lexer_string_source_empty():
    lexer = Lexer(StringSource(""))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF
    assert tokens[0].value is None
    assert tokens[0].pos == (1, 1)


def test_lexer_string_source_all_tokens():
    lexer = Lexer(StringSource("int a = 1; int b = 2;"))
    token_types = [token.type for token in lexer.get_all_tokens()]
    assert token_types == [
        TokenType.INT,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.INT_VALUE,
        TokenType.SEMI,
        TokenType.INT,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.INT_VALUE,
        TokenType.SEMI,
        TokenType.EOF,
    ]


def test_lexer_file_source_empty_file():
    lexer = Lexer(FileSource("tests/test_cases/empty_file.txt"))
    tokens = lexer.get_all_tokens()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF
    assert tokens[0].value is None
    assert tokens[0].pos == (1, 1)


def test_lexer_file_source_all_tokens():
    lexer = Lexer(FileSource("tests/test_cases/all_tokens.txt"))
    token_types = [token.type for token in lexer.get_all_tokens()]
    assert token_types == [
        TokenType.INT,
        TokenType.FLOAT,
        TokenType.BOOL,
        TokenType.STRING,
        TokenType.LIST,
        TokenType.POINT,
        TokenType.LINE,
        TokenType.POLYHEDRON,
        TokenType.COLLECTION,
        TokenType.WHILE,
        TokenType.IF,
        TokenType.ELSE,
        TokenType.OR,
        TokenType.AND,
        TokenType.TRUE,
        TokenType.FALSE,
        TokenType.VOID,
        TokenType.RETURN,
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.MUL,
        TokenType.DIV,
        TokenType.ASSIGN,
        TokenType.GREATER,
        TokenType.LESS,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
        TokenType.RBRACE,
        TokenType.DOT,
        TokenType.COMMA,
        TokenType.SEMI,
        TokenType.NOT,
        TokenType.COMMENT,
        TokenType.EQ,
        TokenType.NEQ,
        TokenType.LE,
        TokenType.GE,
        TokenType.IDENTIFIER,
        TokenType.INT_VALUE,
        TokenType.FLOAT_VALUE,
        TokenType.EOF
    ]


def test_lexer_file_source_simple_code():
    lexer = Lexer(FileSource("tests/test_cases/simple_code.txt"))
    token_types = [token.type for token in lexer.get_all_tokens()]
    assert token_types == [
        TokenType.INT,
        TokenType.IDENTIFIER,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
        TokenType.COMMENT,
        TokenType.POLYHEDRON,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.POLYHEDRON,
        TokenType.LPAREN,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.RPAREN,
        TokenType.SEMI,
        TokenType.COLLECTION,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN,
        TokenType.COLLECTION,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.SEMI,
        TokenType.IDENTIFIER,
        TokenType.DOT,
        TokenType.IDENTIFIER,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.SEMI,
        TokenType.IDENTIFIER,
        TokenType.LPAREN,
        TokenType.STRING_VALUE,
        TokenType.RPAREN,
        TokenType.SEMI,
        TokenType.RBRACE,
        TokenType.EOF
    ]
