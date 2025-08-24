from core.interpreter.symbol_table import SymbolTable
from core.ast.rootNode import *

class TypeChecker:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table

    def check(self, node):
        if isinstance(node, NumberNode):
            return "int" if isinstance(node.value, int) else "float"
        
        elif isinstance(node, StringNode):
            return "string"
        
        elif isinstance(node, VariableNode):
            var_type = self.symbol_table.get_variable_type(node.name)
            if var_type is None:
                raise TypeError(f"Undefined variable '{node.name}'")
            return var_type
        
        elif isinstance(node, BinaryOpNode):
            left_type = self.check(node.left)
            right_type = self.check(node.right)
            
            if left_type != right_type:
                raise TypeError(f"Type mismatch: {left_type} {node.operator} {right_type}")
            return left_type
        
        elif isinstance(node, VarDeclarationNode):
            value_type = self.check(node.value)
            self.symbol_table.define_variable(node.name, value_type)
            return value_type
        
        elif isinstance(node, FunctionCallNode):
            func_signature = self.symbol_table.get_function_signature(node.name)
            if func_signature is None:
                raise TypeError(f"Undefined function '{node.name}'")
            param_types, return_type = func_signature
            
            if len(param_types) != len(node.args):
                raise TypeError(f"Function '{node.name}' expects {len(param_types)} arguments but got {len(node.args)}")
            
            for i, arg in enumerate(node.args):
                arg_type = self.check(arg)
                if arg_type != param_types[i]:
                    raise TypeError(f"Argument {i+1} of '{node.name}' should be {param_types[i]}, got {arg_type}")
            
            return return_type
        
        elif isinstance(node, ReturnNode):
            return self.check(node.value)
        
        elif isinstance(node, FunctionNode):
            param_types = [param[1] for param in node.params]  # Extract parameter types
            self.symbol_table.define_function(node.name, param_types, "unknown")
            
            # Register parameters in the symbol table
            for param_name, param_type in node.params:
                self.symbol_table.define_variable(param_name, param_type)
            
            return_type = self.check(node.body)  # Infer return type from function body
            self.symbol_table.functions[node.name] = (param_types, return_type)  # Update function return type
            return return_type
        
        return "unknown"


