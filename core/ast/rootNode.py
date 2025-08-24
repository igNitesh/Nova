from typing import List, Optional

# Base class for all AST nodes
class ASTNode:
    def __repr__(self):
        return self.__class__.__name__

# root node of the AST
class ProgramNode(ASTNode):
    def __init__(self, body: List[ASTNode]):
        self.body = body

    def __repr__(self):
        return f"ProgramNode({self.body})"
    

    

# error node for invalid syntax or parsing errors
class ErrorNode(ASTNode):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self):
        return f"ErrorNode({self.message})"