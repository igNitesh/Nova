from core.ast.expressionNodes import *
from core.ast.rootNode import ASTNode, ErrorNode
from core.parser.base_parser import BaseParser


class ExpressionParser(BaseParser):
    """
    ExpressionParser handles parsing of expressions in the Nova language.
    It supports operator precedence, unary and binary operations, function calls,
    and postfix operators like ++ and --.
    """
    def __init__(self, lexer):
        super().__init__(lexer)

    def parse_expression(self) -> ASTNode:
        return self.parse_logical_or()

    def parse_logical_or(self) -> ASTNode:
        node = self.parse_logical_and()
        while self.peek().type == "OPERATOR" and self.peek().value == "||":
            op_token = self.advance()
            right = self.parse_logical_and()
            node = BinaryOpNode(op_token.value, node, right)
        return node

    def parse_logical_and(self) -> ASTNode:
        node = self.parse_equality()
        while self.peek().type == "OPERATOR" and self.peek().value == "&&":
            op_token = self.advance()
            right = self.parse_equality()
            node = BinaryOpNode(op_token.value, node, right)
        return node

    def parse_equality(self) -> ASTNode:
        node = self.parse_comparison()
        while self.peek().type == "OPERATOR" and self.peek().value in ("==", "!="):
            op_token = self.advance()
            right = self.parse_comparison()
            node = BinaryOpNode(op_token.value, node, right)
        return node

    def parse_comparison(self) -> ASTNode:
        node = self.parse_term()
        while self.peek().type == "OPERATOR" and self.peek().value in ("<", ">", "<=", ">="):
            op_token = self.advance()
            right = self.parse_term()
            node = BinaryOpNode(op_token.value, node, right)
        return node

    def parse_term(self) -> ASTNode:
        left = self.parse_factor()
        while self.peek().type == "OPERATOR" and self.peek().value in ("+", "-"):
            op_token = self.advance()
            right = self.parse_factor()
            left = BinaryOpNode(op_token.value, left, right)
        return left

    def parse_factor(self) -> ASTNode:
        node = self.parse_unary()
        while self.peek().type == "OPERATOR" and self.peek().value in ("*", "/", "%"):
            op_token = self.advance()
            right = self.parse_unary()
            node = BinaryOpNode(op_token.value, node, right)
        return node

    def parse_unary(self) -> ASTNode:
        """
        Handles prefix unary operators (+, -, !) and delegates to postfix.
        """
        token = self.peek()
        if token.type == "OPERATOR" and token.value in ("+", "-", "!"):
            op_token = self.advance()
            operand = self.parse_unary()
            return UnaryOpNode(op_token.value, operand)
        return self.parse_postfix()

    def parse_postfix(self) -> ASTNode:
        """
        Handles postfix operators (++, --) with highest precedence.
        """
        node = self.parse_primary()
        while self.peek().type == "OPERATOR" and self.peek().value in ("++", "--"):
            op_token = self.advance()
            node = UnaryOpNode(op_token.value, node)
        return node

    def parse_primary(self) -> ASTNode:
        token = self.peek()

        if token.type == "NUMBER":
            self.advance()
            if "." in token.value:
                return FloatNode(float(token.value))
            else:
                return IntNode(int(token.value))

        elif token.type == "STRING":
            self.advance()
            return StringNode(token.value)

        elif token.type == "IDENTIFIER":
            identifier = self.advance()
            # Handle function call
            if self.peek().value == "(":
                return self.parse_function_call(identifier.value)
            return IdentifierNode(identifier.value)

        elif token.value == "(":
            self.advance()
            expr = self.parse_expression()
            close_paren = self.expect("PUNCTUATION")
            if close_paren.value != ")":
                return ErrorNode("Expected ')' after expression")
            return expr

        elif token.type == "BOOLEAN":
            self.advance()
            return LiteralNode(token.value == "true")

        # ✅ Instead of always failing, make the error message explicit
        # and only trigger when truly invalid, not just because we hit `)` or `;`
        elif token.value in (")", ";", "}"):
            # Let higher-level rules (for/if/while) handle block or end-of-expression
            return ErrorNode(f"Unexpected end of expression at '{token.value}'")

        else:
            return ErrorNode(f"Invalid expression starting with token: {token}")
