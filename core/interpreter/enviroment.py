class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
        self.functions = {}

    def define_variable(self, name, value):
        self.variables[name] = value
    
    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            raise NameError(f"Undefined variable '{name}'")
    
    def set_variable(self, name, value):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set_variable(name, value)
        else:
            raise NameError(f"Undefined variable '{name}'")
    
    def define_function(self, name, params, body):
        self.functions[name] = (params, body)
    
    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            raise NameError(f"Undefined function '{name}'")
