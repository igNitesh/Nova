from core.interpreter.enviroment import Environment
from core.ast.rootNode import *
from core.interpreter.symbol_table import SymbolTable


class Interpreter:
    def __init__(self, symbol_table):
        self.global_env = Environment()
        self.symbol_table = symbol_table
    
    def interpret(self, ast):
        """Execute the AST and return the final expression result."""
        result = None
        for node in ast:
            result = self.execute(node)
            print(f"[DEBUG] Executed {node} → Result: {result}")  # Ensure expressions return values
        return result  # Return the last evaluated value
    
    def execute(self, node):
        if isinstance(node, VarDeclarationNode):  # Variable declaration
            value = self.evaluate_expression(node.value)
            self.global_env.define_variable(node.name, value)
            print(f"[DEBUG] Declared variable {node.name} = {value}")
            return value  # Ensure the assigned value is returned
        
        elif isinstance(node, AssignmentNode):  # Variable assignment
            value = self.evaluate_expression(node.value)
            self.global_env.set_variable(node.name, value)
            print(f"[DEBUG] Assigned variable {node.name} = {value}")
            return value
        
        elif isinstance(node, PrintNode):  # Built-in print function
            value = self.evaluate_expression(node.expression)
            print(value)
            print(f"[DEBUG] Printed value: {value}")
            return value  # Return value for testing
        
        elif isinstance(node, IfNode):  # If-else condition
            condition = self.evaluate_expression(node.condition)
            if condition:
                return self.execute(node.if_body)
            elif node.else_body:
                return self.execute(node.else_body)
        
        elif isinstance(node, WhileNode):  # While loop
            result = None
            while self.evaluate_expression(node.condition):
                result = self.execute(node.body)
            return result  # Return last loop body value
        
        elif isinstance(node, FunctionNode):  # Function declaration
            self.global_env.define_function(node.name, node.params, node.body)
            return None  # No value is returned for function declarations
        
        elif isinstance(node, FunctionCallNode):  # Function call
            func = self.global_env.get_function(node.name)
            if func is None:
                raise Exception(f"Undefined function '{node.name}'")
            
            params, body = func
            local_env = Environment(self.global_env)
            for param, arg in zip(params, node.args):
                local_env.define_variable(param, self.evaluate_expression(arg))
            
            return Interpreter(self.symbol_table).execute(body)  # Return function result
        
        elif isinstance(node, ReturnNode):  # Return statement
            return self.evaluate_expression(node.value)
        
        elif isinstance(node, BinaryOpNode) or isinstance(node, NumberNode):  
            return self.evaluate_expression(node)  # Ensure expressions return values
        
        elif isinstance(node, VariableNode):  # Variable Access
            return self.global_env.get_variable(node.name)
        
        else:
            raise Exception(f"Unknown AST node type: {node}")


    
    def evaluate_expression(self, expr):
        """Evaluate and return expressions (fixing arithmetic operations)."""
        if isinstance(expr, NumberNode):
            print(f"[DEBUG] NumberNode → {expr.value}")  # Direct number value
            return expr.value
        elif isinstance(expr, StringNode): 
            print(f"[DEBUG] StringNode → {expr.value}") # Direct string value
            return expr.value
        elif isinstance(expr, VariableNode):
            value = self.global_env.get_variable(expr.name)
            print(f"[DEBUG] VariableNode '{expr.name}' → {value}")  # Retrieve variable value
            return value
        elif isinstance(expr, BinaryOpNode):  # Arithmetic operations
            left = self.evaluate_expression(expr.left)
            right = self.evaluate_expression(expr.right)
            print(f"[DEBUG] BinaryOpNode {expr.left} {expr.operator} {expr.right} → ")
            if expr.operator == '+':
                return left + right
            elif expr.operator == '-':
                return left - right
            elif expr.operator == '*':
                return left * right
            elif expr.operator == '/':
                return left / right if right != 0 else float('inf')  # Prevent division by zero
            else:
                raise Exception(f"Unknown operator '{expr.operator}'")
        else:
            raise Exception(f"Unknown expression type: {expr}")


