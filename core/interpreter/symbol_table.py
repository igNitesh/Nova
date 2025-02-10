class SymbolTable:
    def __init__(self):
        self.variables = {}  # Stores variable names and types
        self.functions = {}  # Stores function names, parameters, and return types

    def define_variable(self, name, type_):
        if name in self.variables:
            raise TypeError(f"Variable '{name}' is already defined.")
        self.variables[name] = type_

    def get_variable_type(self, name):
        return self.variables.get(name, None)

    def define_function(self, name, param_types, return_type):
        if name in self.functions:
            raise TypeError(f"Function '{name}' is already defined.")
        self.functions[name] = (param_types, return_type)

    def get_function_signature(self, name):
        return self.functions.get(name, None)

    def __repr__(self):
        return f"Variables: {self.variables}\nFunctions: {self.functions}"
