class Literal:
    def __init__(self,name,bool_value=True):
        self.name = name
        self.bool_value = bool_value
    def negate(self,negate_param):
        if self.name == negate_param.name:
            return  self.bool_value != negate_param.bool_value
    def eq(self,literal_param):
        return (self.name == literal_param.name) and (self.bool_value == literal_param.bool_value)
    def print_literal(self):
        print(self.name,end=' ')
        print(self.bool_value,end=" ")
        print()
        
        