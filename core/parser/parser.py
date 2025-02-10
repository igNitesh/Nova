from typing import List
from core.lexer.lexer import Token
from core.ast.nodes import *

class Parser:
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

    def parse_variable_declaration(self) -> ASTNode:
        var_token = self.expect("KEYWORD")
        if var_token.value != "var":
            return ErrorNode("Expected 'var' keyword")

        identifier = self.expect("IDENTIFIER")
        if identifier.type == "ERROR":
            return ErrorNode(identifier.value)

        equal_sign = self.expect("OPERATOR")
        if equal_sign.value != "=":
            return ErrorNode("Expected '=' in variable declaration")

        value = self.parse_expression()
        semicolon = self.expect("PUNCTUATION")
        if semicolon.value != ";":
            return ErrorNode("Expected ';' at end of statement")
        
        return VarDeclarationNode(identifier.value, value)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_binary_expression()
    
    def parse_binary_expression(self) -> ASTNode:
        left = self.parse_primary()
        while self.peek().type == "OPERATOR":
            operator = self.advance().value
            right = self.parse_primary()
            left = BinaryOpNode(left, operator, right)
        return left
    
    def parse_primary(self) -> ASTNode:
        token = self.peek()
        if token.type == "NUMBER":
            return NumberNode(float(self.advance().value))
        elif token.type == "STRING":
            return StringNode(self.advance().value)
        elif token.type == "IDENTIFIER":
            if self.position + 1 < len(self.tokens) and self.tokens[self.position + 1].value == "(":
                return self.parse_function_call()
            return VariableNode(self.advance().value)
        return ErrorNode("Invalid expression")
    
    def parse_function(self) -> ASTNode:
        func_token = self.expect("KEYWORD")
        if func_token.value != "func":
            return ErrorNode("Expected 'func' keyword")

        name = self.expect("IDENTIFIER")
        if name.type == "ERROR":
            return ErrorNode(name.value)

        self.expect("PUNCTUATION")
        params = []
        while self.peek().type == "IDENTIFIER":
            params.append(self.advance().value)
            if self.peek().value == ",":
                self.advance()
        self.expect("PUNCTUATION")

        self.expect("PUNCTUATION")
        body = []
        while self.peek().value != "}":
            body.append(self.parse_expression())
        self.expect("PUNCTUATION")
        
        return FunctionNode(name.value, params, body)
    
    def parse_function_call(self) -> ASTNode:
        name = self.expect("IDENTIFIER")
        self.expect("PUNCTUATION")
        args = []
        while self.peek().type != "PUNCTUATION" or self.peek().value != ")":
            args.append(self.parse_expression())
            if self.peek().value == ",":
                self.advance()
        self.expect("PUNCTUATION")
        return FunctionCallNode(name.value, args)
    
    def parse_return_statement(self) -> ASTNode:
        return_token = self.expect("KEYWORD")
        if return_token.value != "return":
            return ErrorNode("Expected 'return' keyword")
        value = self.parse_expression()
        self.expect("PUNCTUATION")
        return ReturnNode(value)
    
    def parse_control_flow(self) -> ASTNode:
        keyword = self.expect("KEYWORD")
        if keyword.value == "if":
            self.expect("PUNCTUATION")
            condition = self.parse_expression()
            self.expect("PUNCTUATION")
            self.expect("PUNCTUATION")
            body = []
            while self.peek().value != "}":
                body.append(self.parse_expression())
            self.expect("PUNCTUATION")
            
            else_body = None
            if self.peek().value == "else":
                self.advance()
                self.expect("PUNCTUATION")
                else_body = []
                while self.peek().value != "}":
                    else_body.append(self.parse_expression())
                self.expect("PUNCTUATION")
            
            return IfNode(condition, body, else_body)
        elif keyword.value == "while":
            self.expect("PUNCTUATION")
            condition = self.parse_expression()
            self.expect("PUNCTUATION")
            self.expect("PUNCTUATION")
            body = []
            while self.peek().value != "}":
                body.append(self.parse_expression())
            self.expect("PUNCTUATION")
            
            return WhileNode(condition, body)
        elif keyword.value == "for":
            self.expect("PUNCTUATION")
            init = self.parse_variable_declaration()
            condition = self.parse_expression()
            self.expect("PUNCTUATION")
            update = self.parse_expression()
            self.expect("PUNCTUATION")
            self.expect("PUNCTUATION")
            body = []
            while self.peek().value != "}":
                body.append(self.parse_expression())
            self.expect("PUNCTUATION")
            
            return ForNode(init, condition, update, body)
        
        return ErrorNode("Invalid control flow statement")
    
    def parse(self):
        """Parse tokens into an AST."""
        ast = []
        while self.current_token is not None:
            node = self.parse_statement()
            if node:
                ast.append(node)
        print(f"[DEBUG] Generated AST: {ast}")  # ✅ Debugging output
        return ast

    def parse_statements(self):
        statements = []
        while self.current_token is not None:
            statements.append(self.parse_statement())
            self.advance()
        return statements