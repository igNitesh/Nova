from core.ast.rootNode import ASTNode
from typing import List


class Return_Statement_Node(ASTNode):
    """Node representing a return statement."""
    def __init__(self, value: ASTNode):
        self.value = value

    def __repr__(self):
        return f"ReturnNode({self.value})"

class While_Statement_Node(ASTNode):
    def __init__(self, condition: ASTNode, body: List[ASTNode]):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileNode({self.condition}) {{ {self.body} }}"

class For_Statement_Node(ASTNode):
    def __init__(self, init: ASTNode, condition: ASTNode, update: ASTNode, body: List[ASTNode]):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return f"ForNode({self.init}; {self.condition}; {self.update}) {{ {self.body} }}"

class if_Statement_Node(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: List[ASTNode], else_branch: List[ASTNode] = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfNode({self.condition}) {{ {self.then_branch} }} else {{ {self.else_branch} }}"


class Else_Statement_Node(ASTNode):
    """Node representing an else statement."""
    def __init__(self, body: List[ASTNode]):
        self.body = body

    def __repr__(self):
        return f"ElseNode({self.body})"