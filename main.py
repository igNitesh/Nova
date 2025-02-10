# main.py
import sys
import os
import unittest
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.lexer.lexer import Lexer
from core.parser.parser import Parser
from core.interpreter.interpreter import Interpreter
from core.interpreter.symbol_table import SymbolTable
from core.interpreter.type_checker import TypeChecker
from core.ast.nodes import *

# # Initialize symbol table and type checker
# symbol_table = SymbolTable()
# type_checker = TypeChecker(symbol_table)

# def test_case(description, node):
#     try:
#         result = type_checker.check(node)
#         print(f"✅ {description}: PASSED - Type: {result}")
#     except Exception as e:
#         print(f"❌ {description}: FAILED - {e}")

# # Test cases
# print("Running Type Checker Tests...\n")

# test_case("Variable Declaration (int)", VarDeclarationNode("x", NumberNode(10)))
# test_case("Variable Declaration (float)", VarDeclarationNode("y", NumberNode(10.5)))
# test_case("String Declaration", VarDeclarationNode("msg", StringNode("Hello")))
# test_case("Binary Operation (int + int)", BinaryOpNode(NumberNode(5), "+", NumberNode(3)))
# test_case("Binary Operation (float + float)", BinaryOpNode(NumberNode(2.5), "+", NumberNode(1.5)))
# test_case("Binary Operation (int + string, should fail)", BinaryOpNode(NumberNode(5), "+", StringNode("text")))

# test_case("Function Declaration", FunctionNode("add", [("a", "int"), ("b", "int")], BinaryOpNode(VariableNode("a"), "+", VariableNode("b"))))
# test_case("Function Call (valid)", FunctionCallNode("add", [NumberNode(4), NumberNode(6)]))
# test_case("Function Call (mismatched types, should fail)", FunctionCallNode("add", [StringNode("hello"), NumberNode(5)]))

# test_case("Return Statement", ReturnNode(NumberNode(42)))

# print("\nAll test cases completed.")

# class TestTypeChecker(unittest.TestCase):
#     def setUp(self):
#         self.symbol_table = SymbolTable()
#         self.type_checker = TypeChecker(self.symbol_table)

#     def test_variable_declaration(self):
#         var_decl = VarDeclarationNode("x", NumberNode(10))
#         self.assertEqual(self.type_checker.check(var_decl), "int")
#         self.assertEqual(self.symbol_table.get_variable_type("x"), "int")

#     def test_string_declaration(self):
#         var_decl = VarDeclarationNode("s", StringNode("Hello"))
#         self.assertEqual(self.type_checker.check(var_decl), "string")
#         self.assertEqual(self.symbol_table.get_variable_type("s"), "string")
    
#     def test_binary_operation_valid(self):
#         expr = BinaryOpNode(NumberNode(5), "+", NumberNode(10))
#         self.assertEqual(self.type_checker.check(expr), "int")
    
#     def test_binary_operation_invalid(self):
#         expr = BinaryOpNode(NumberNode(5), "+", StringNode("text"))
#         with self.assertRaises(TypeError):
#             self.type_checker.check(expr)
    
#     def test_function_declaration(self):
#         func_decl = FunctionNode("add", [("a", "int"), ("b", "int")],
#                                 BinaryOpNode(VariableNode("a"), "+", VariableNode("b")))
#         self.assertEqual(self.type_checker.check(func_decl), "int")
#         self.assertEqual(self.symbol_table.get_function_signature("add"), (["int", "int"], "int"))
    
#     def test_function_call_valid(self):
#         func_decl = FunctionNode("add", [("a", "int"), ("b", "int")],
#                                 BinaryOpNode(VariableNode("a"), "+", VariableNode("b")))
#         self.type_checker.check(func_decl)
#         func_call = FunctionCallNode("add", [NumberNode(2), NumberNode(3)])
#         self.assertEqual(self.type_checker.check(func_call), "int")
    
#     def test_function_call_invalid(self):
#         func_decl = FunctionNode("add", [("a", "int"), ("b", "int")],
#                                 BinaryOpNode(VariableNode("a"), "+", VariableNode("b")))
#         self.type_checker.check(func_decl)
#         func_call = FunctionCallNode("add", [NumberNode(2), StringNode("error")])
#         with self.assertRaises(TypeError):
#             self.type_checker.check(func_call)
    
#     def test_return_statement(self):
#         return_stmt = ReturnNode(NumberNode(42))
#         self.assertEqual(self.type_checker.check(return_stmt), "int")

# if __name__ == "__main__":
#     print("Running Type Checker Tests...\n")
#     unittest.main()
#     print("\nAll test cases completed.")

def run_test_case(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()  # Ensure the method name matches!

    print("ast:- ",ast)
    interpreter = Interpreter(symbol_table={})
    result = interpreter.interpret(ast)
    
    return result

# Test Cases
test_cases = [
    ("5 + 3", 8),
    ("10 - 2 * 3", 4),
    ("20 / 4 + 1", 6.0),
    ("var x = 10\nx + 5", 15),
    ("""
    func add(a, b) {
        return a + b
    }
    add(5, 3)
    """, 8),
    ("""
    var y = 2
    func multiply(a) {
        return a * y
    }
    multiply(4)
    """, 8),
]

print("\nRunning Interpreter Tests...\n")

for code, expected in test_cases:
    try:
        result = run_test_case(code)
        if result == expected:
            print(f"✅ Test PASSED: {code.strip()} → {result}")
        else:
            print(f"❌ Test FAILED: {code.strip()} → Expected {expected}, got {result}")
    except Exception as e:
        print(f"❌ Test ERROR: {code.strip()} → {e}")

print("\nAll tests completed.")