# import pytest
import sys
import os
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.lexer.lexer import Lexer
from core.parser.parser import Parser
from core.interpreter.interpreter import Interpreter

def run_code(source: str):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.run(ast)

def test_variable_declaration(capsys):
    run_code("let x = 10; print(x);")
    assert capsys.readouterr().out == "10\n"

def test_if_statement(capsys):
    run_code("if (5 > 3) { print('Condition met'); }")
    assert capsys.readouterr().out == "Condition met\n"

