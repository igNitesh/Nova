from core.ast.declarationNodes import VarDeclarationNode
from core.ast.rootNode import ASTNode, ErrorNode
from core.ast.statementNodes import For_Statement_Node, if_Statement_Node
from core.interpreter.symbol_table import SymbolTable
from core.parser.base_parser import BaseParser
from core.parser.expression_parser import ExpressionParser


class DecalarationParser(BaseParser):
    def __init__(self, lexer):
        super().__init__(lexer)
    
    def parse_variable_declaration(self) -> ASTNode:
        '''Parses a variable declaration statement. '''
        var_token = self.expect("KEYWORD")
        if var_token.value not in ("int", "string", "boolean", "float"):
            return ErrorNode("Expected 'var' keyword")

        identifier = self.expect("IDENTIFIER")
        if identifier.type == "ERROR":
            return ErrorNode(identifier.value)
        
        equal_sign = self.expect("OPERATOR")
        if equal_sign.value != "=":
            return ErrorNode("Variable declaration must have an initializer (e.g., int x = 0;)")
        
        value = self.parse_expression() 
        semicolon = self.expect("PUNCTUATION")
        if semicolon.value != ";":
            return ErrorNode("Expected ';' at end of statement",)
        return VarDeclarationNode(var_token.value,identifier.value, value)
    
    