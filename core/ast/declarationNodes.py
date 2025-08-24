from core.ast.rootNode import ASTNode
from typing import List

# Declaration Nodes , variable declaration node,function declaration node,class declaration node

class VarDeclarationNode(ASTNode):#variable declaration node
    def __init__(self,var_type: str, name: str, value: ASTNode):
        self.var_type = var_type  # e.g., "int", "string"
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VarDeclarationNode({self.var_type} {self.name} = {self.value})"
        
class ConstantDeclarationNode(ASTNode):  # Constant declaration node
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"ConstantDeclarationNode({self.name} = {self.value})"

class Function_Declaration_Node(ASTNode):
    def __init__(self, name: str, params: List[str], body: List[ASTNode]):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionNode({self.name}({', '.join(self.params)}) {{ {self.body} }})"
    
class Class_Declaration_Node(ASTNode):
    def __init__(self, name: str, methods: List[Function_Declaration_Node]):
        self.name = name
        self.methods = methods

    def __repr__(self):
        return f"ClassNode({self.name} {{ {', '.join(str(method) for method in self.methods)} }})"
    
 