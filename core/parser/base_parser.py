from symtable import SymbolTable
from typing import List
from core.lexer.lexer import Token
from core.ast.rootNode import *
from core.ast.declarationNodes import VarDeclarationNode
from core.ast.expressionNodes import *

class BaseParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token = None  
        self.position = -1
        self.advance()

    def peek(self) -> Token:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return Token("EOF", "", -1, -1)

    def advance(self) -> Token:
        current = self.peek()
        self.position += 1
        return current

    def expect(self, token_type: str) -> Token:
        token = self.peek()
        if token.type == token_type:
            return self.advance()
        return Token("ERROR", f"Expected {token_type}, got {token.type}", token.line, token.column)

    def is_at_end(self):
        return self.position >= len(self.tokens) or self.peek().type == "EOF"
    
   



    def evaluate_expression(self, node: ASTNode, env=None) -> any:
        """
        Recursively evaluates an expression AST node and returns its computed value.
        Supports LiteralNode, IdentifierNode (if variable table is provided), BinaryOpNode, and function calls.
        Note: For full evaluation, you may need to pass a variable environment/context.
        """
        if env is None:
            env = {}
        if isinstance(node, LiteralNode):
            return node.value
        elif isinstance(node, IntNode):
            return node.value
        elif isinstance(node, FloatNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            # Lookup variable value in environment
            symbol_table = SymbolTable()
            if hasattr(symbol_table, 'get_value'):
                return symbol_table.get_value(node.name)
            if node.name in env:
                return env[node.name]
            else:
                raise ValueError(f"Undefined variable: {node.name}")
        elif isinstance(node, BinaryOpNode):
            left = self.evaluate_expression(node.left, env)
            right = self.evaluate_expression(node.right, env)
            op = node.operator
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
            elif op == '%':
                return left % right
            else:
                raise ValueError(f"Unknown operator: {op}")
        elif isinstance(node, FunctionCallNode):
            raise NotImplementedError("Function call evaluation not implemented.")
        else:
            raise ValueError(f"Cannot evaluate node type: {type(node).__name__}")