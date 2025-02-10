import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from core.interpreter.interpreter import Interpreter
from core.interpreter.symbol_table import SymbolTable
from core.interpreter.type_checker import TypeChecker
from core.ast.nodes import *

class TestTypeChecker(unittest.TestCase):
    def setUp(self):
        self.symbol_table = SymbolTable()
        self.type_checker = TypeChecker(self.symbol_table)

    def test_variable_declaration(self):
        var_decl = VarDeclarationNode("x", NumberNode(10))
        self.assertEqual(self.type_checker.check(var_decl), "int")
        self.assertEqual(self.symbol_table.get_variable_type("x"), "int")

    def test_string_declaration(self):
        var_decl = VarDeclarationNode("s", StringNode("Hello"))
        self.assertEqual(self.type_checker.check(var_decl), "string")
        self.assertEqual(self.symbol_table.get_variable_type("s"), "string")
    
    def test_binary_operation_valid(self):
        expr = BinaryOpNode(NumberNode(5), "+", NumberNode(10))
        self.assertEqual(self.type_checker.check(expr), "int")
    
    def test_binary_operation_invalid(self):
        expr = BinaryOpNode(NumberNode(5), "+", StringNode("text"))
        with self.assertRaises(TypeError):
            self.type_checker.check(expr)
    
    def test_function_declaration(self):
        func_decl = FunctionNode("add", [("a", "int"), ("b", "int")],
                                BinaryOpNode(VariableNode("a"), "+", VariableNode("b")))
        self.assertEqual(self.type_checker.check(func_decl), "int")
        self.assertEqual(self.symbol_table.get_function_signature("add"), (["int", "int"], "int"))
    
    def test_function_call_valid(self):
        func_decl = FunctionNode("add", [("a", "int"), ("b", "int")],
                                BinaryOpNode(VariableNode("a"), "+", VariableNode("b")))
        self.type_checker.check(func_decl)
        func_call = FunctionCallNode("add", [NumberNode(2), NumberNode(3)])
        self.assertEqual(self.type_checker.check(func_call), "int")
    
    def test_function_call_invalid(self):
        func_decl = FunctionNode("add", [("a", "int"), ("b", "int")],
                                BinaryOpNode(VariableNode("a"), "+", VariableNode("b")))
        self.type_checker.check(func_decl)
        func_call = FunctionCallNode("add", [NumberNode(2), StringNode("error")])
        with self.assertRaises(TypeError):
            self.type_checker.check(func_call)
    
    def test_return_statement(self):
        return_stmt = ReturnNode(NumberNode(42))
        self.assertEqual(self.type_checker.check(return_stmt), "int")

if __name__ == "__main__":
    unittest.main()
