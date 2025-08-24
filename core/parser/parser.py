from core.ast.expressionNodes import AssignmentNode, IdentifierNode, UnaryOpNode
from core.ast.rootNode import ErrorNode
from core.parser.expression_parser import ExpressionParser
from core.parser.declaration_parser import DecalarationParser
from core.parser.statement_parser import StatementParser


class Parser(ExpressionParser, DecalarationParser,StatementParser):
    def __init__(self, lexer):
        super().__init__(lexer)
    

    def parse_statement(self):
        """
        Parses a single statement, which can be a variable declaration or an expression.
        """
        if self.peek().type == "KEYWORD" and self.peek().value in ("int", "string", "boolean", "float"):
            return self.parse_variable_declaration()
        elif self.peek().type == "KEYWORD" and self.peek().value == "if":
            return self.parse_if_statement()
        elif self.peek().type == "KEYWORD" and self.peek().value == "for":
            return self.parse_for_statement()
        elif self.peek().type == "KEYWORD" and self.peek().value == "while":
            pass
        elif self.peek().type == "IDENTIFIER":
            identifier_token = self.advance()
            next_token = self.peek()
            # Check for a++ or a--
            if next_token.type == "OPERATOR" and next_token.value in ("++", "--"):
                op_token = self.advance()
                semicolon = self.expect("PUNCTUATION")
                if semicolon.value != ";":
                    return ErrorNode("Expected ';' after increment/decrement")
                return UnaryOpNode(op_token.value, IdentifierNode(identifier_token.value))

            elif next_token.type == "OPERATOR" and next_token.value == "=":
                self.advance()  # consume '='
                expr = self.parse_expression()
                semicolon = self.expect("PUNCTUATION")
                if semicolon.value != ";":
                    return ErrorNode("Expected ';' after assignment")
                return AssignmentNode(identifier_token.value, expr)
            elif next_token.type == "PUNCTUATION" and next_token.value == "(":
                return self.parse_function_call(identifier_token.value)
            else:
                # Fallback: parse as expression
                return IdentifierNode(identifier_token.value)

        else:
            return self.parse_expression()
        

    def parse_program(self):
        """
        Parses the entire program, which consists of multiple statements.
        """
        statements = []
        while not self.is_at_end():
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            # Optionally, skip stray semicolons
            while self.peek().type == "PUNCTUATION" and self.peek().value == ";":
                self.advance()
        return statements