from core.ast.rootNode import ASTNode, ErrorNode
from core.ast.statementNodes import Else_Statement_Node, For_Statement_Node, if_Statement_Node
from core.parser.base_parser import BaseParser


class StatementParser(BaseParser):
    def __init__(self, lexer):
        super().__init__(lexer)

    def parse_if_statement(self) -> ASTNode:
        """
        Parses an if statement.
        Example: if (condition) { ... }
        """
        if_token = self.expect("KEYWORD") # Expecting 'if'
        if if_token.value != "if":
            return ErrorNode("Expected 'if' keyword")
        
        open_paren = self.expect("PUNCTUATION")
        if open_paren.value != "(":
            return ErrorNode("Expected '(' after 'if'") 
        
        condition = self.parse_expression()  # Parse the condition expression
        close_paren = self.expect("PUNCTUATION")
        if close_paren.value != ")":
            return ErrorNode("Expected ')' after condition")
        
        open_brace = self.expect("PUNCTUATION")
        if open_brace.value != "{":     
            return ErrorNode("Expected '{' to start if block") 
        then_branch = []
        while not self.is_at_end() and self.peek().value != "}":
            stmt = self.parse_statement()
            if stmt is not None:
                then_branch.append(stmt)
            # Optionally, skip stray semicolons
            while self.peek().type == "PUNCTUATION" and self.peek().value == ";":
                self.advance()
        close_brace = self.expect("PUNCTUATION")
        if close_brace.value != "}":
            return ErrorNode("Expected '}' to end if block")
        
        # Check for optional else statement
        else_branch = None
        if self.peek().type == "KEYWORD" and self.peek().value == "else":
            else_branch = self.parse_else_statement()
    
        return if_Statement_Node(condition, then_branch, else_branch.body if isinstance(else_branch, Else_Statement_Node) else None)
    
    def parse_else_statement(self) -> ASTNode:
        """
        Parses an else statement.
        Example: else { ... }
        """
        else_token = self.expect("KEYWORD")
        if else_token.value != "else":
            return ErrorNode("Expected 'else' keyword")
        
        open_brace = self.expect("PUNCTUATION")
        if open_brace.value != "{":
            return ErrorNode("Expected '{' to start else block")
        
        body = []
        while not self.is_at_end() and self.peek().value != "}":
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
            # Optionally, skip stray semicolons
            while self.peek().type == "PUNCTUATION" and self.peek().value == ";":
                self.advance()
        
        close_brace = self.expect("PUNCTUATION")
        if close_brace.value != "}":
            return ErrorNode("Expected '}' to end else block")
        
        return Else_Statement_Node(body)    
    
    def parse_for_statement(self) -> ASTNode:
        for_token = self.expect("KEYWORD")
        if for_token.value != "for":
            return ErrorNode("Expected 'for' keyword")

        open_paren = self.expect("PUNCTUATION")
        if open_paren.value != "(":
            return ErrorNode("Expected '(' after 'for'")

        # --- Initialization ---
        if self.peek().type == "KEYWORD" and self.peek().value in ("int", "string", "boolean", "float"):
            init = self.parse_variable_declaration() # variable declaration consume ; token so i am checking it
        elif self.peek().type == "IDENTIFIER":
            init = self.parse_statement()  # assignment or function call or expr
        else:
            init = None


        # --- Condition ---
        condition = None
        if not (self.peek().type == "PUNCTUATION" and self.peek().value == ";"):
            condition = self.parse_expression() # parse_expression will not consume the semicolon(;) so we can check it

        semicoln2 = self.expect("PUNCTUATION")
        if semicoln2.value != ";":
            return ErrorNode("Expected ';' after for loop condition")
        # --- Increment ---f
        increment = None
        if not (self.peek().type == "PUNCTUATION" and self.peek().value == ")"):
            increment = self.parse_expression()
            print(f"Increment parsed: {increment}")

        # Close parenthesis
        print(f"increment parsed: {self.peek().value}")
        close_paren = self.expect("PUNCTUATION")
        if close_paren.value != ")":
            return ErrorNode("Expected ')' after for loop components")

        # --- Body ---
        open_brace = self.expect("PUNCTUATION")
        if open_brace.value != "{":
            return ErrorNode("Expected '{' to start for loop body")

        body = []
        while not self.is_at_end() and self.peek().value != "}":
            print(f"Parsing statement in for loop body: {self.peek().value}")
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
            while self.peek().type == "PUNCTUATION" and self.peek().value == ";":
                self.advance()

        close_brace = self.expect("PUNCTUATION")
        if close_brace.value != "}":
            return ErrorNode("Expected '}' to end for loop body")

        return For_Statement_Node(init, condition, increment, body)
