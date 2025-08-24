from core.ast.rootNode import ASTNode
from typing import List



class expressionNode(ASTNode):
    def __init__(self, expression: str):
        self.expression = expression

    def __repr__(self):
        return f"ExpressionNode({self.value})"
    
class BinaryOpNode(expressionNode):
    def __init__(self,  operator: str,left: ASTNode, right: ASTNode):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.operator} {self.right})"
    
class UnaryOpNode(expressionNode):
    def __init__(self, operator: str, operand: ASTNode):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOpNode({self.operator} {self.operand})"  
    

class FunctionCallNode(expressionNode):
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCallNode({self.name}({', '.join(str(arg) for arg in self.args)}))"
    
class AssignmentNode(expressionNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"AssignmentNode({self.name} = {self.value})"
    
class LiteralNode(expressionNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"LiteralNode({self.value})"

class IntNode(expressionNode):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"IntNode({self.value})"

class FloatNode(expressionNode):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"FloatNode({self.value})"

class StringNode(expressionNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"StringNode({self.value})"
    
class IdentifierNode(expressionNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode({self.name})"
    

