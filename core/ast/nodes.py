from typing import List, Optional

# Base class for all AST nodes
class ASTNode:
    def __repr__(self):
        return self.__class__.__name__

# Expression Nodes
class NumberNode(ASTNode):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"StringNode({self.value})"

class VariableNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"VariableNode({self.name})"

class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.operator} {self.right})"

# Statement Nodes
class VarDeclarationNode(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VarDeclarationNode({self.name} = {self.value})"

class AssignmentNode(ASTNode):  # ✅ Added
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"AssignmentNode({self.name} = {self.value})"

class FunctionNode(ASTNode):
    def __init__(self, name: str, params: List[str], body: List[ASTNode]):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionNode({self.name}({', '.join(self.params)}) {{ {self.body} }})"

class FunctionCallNode(ASTNode):  # ✅ Fixed missing repr
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCallNode({self.name}({', '.join(map(str, self.args))}))"

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: List[ASTNode], else_branch: Optional[List[ASTNode]] = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfNode({self.condition}) {{ {self.then_branch} }} else {{ {self.else_branch} }}"

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: List[ASTNode]):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileNode({self.condition}) {{ {self.body} }}"

class ForNode(ASTNode):
    def __init__(self, init: ASTNode, condition: ASTNode, update: ASTNode, body: List[ASTNode]):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return f"ForNode({self.init}; {self.condition}; {self.update}) {{ {self.body} }}"

class PrintNode(ASTNode):  # ✅ Added
    def __init__(self, value: ASTNode):
        self.value = value

    def __repr__(self):
        return f"PrintNode({self.value})"

class ReturnNode(ASTNode):  # ✅ Fixed missing repr
    def __init__(self, value: ASTNode):
        self.value = value

    def __repr__(self):
        return f"ReturnNode({self.value})"

class ErrorNode(ASTNode):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self):
        return f"ErrorNode(Error: {self.message})"
