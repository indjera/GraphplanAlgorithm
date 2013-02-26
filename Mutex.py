class Mutex:
    def __init__(self,object1,object2,level,mutex_type):
        self.obj1=object1
        self.obj2=object2
        self.level = level
        self.type ="" 
        self.type=mutex_type
        
    def eq(self,mutex_to_cmp):
        ok1 = self.obj1.eq(mutex_to_cmp.obj1) and self.obj2.eq(mutex_to_cmp.obj2)
        ok2 = self.obj1.eq(mutex_to_cmp.obj2) and self.obj2.eq(mutex_to_cmp.obj1)
        return (ok1 or ok2) and self.level == mutex_to_cmp.level
    
    def eq_string(self,str_to_cmp):
        return (self.obj1.name + self.obj2.name) == str_to_cmp or (self.obj2.name + self.obj1.name)
    
    def print_mutex(self):
        if self.type == "literalInconsistent":
            self.obj1.print_literal()
            self.obj2.print_literal()
            print(self.level)
        else:
            self.obj1.print_action()
            self.obj2.print_action()
            print(self.level)
        print(self.type)
        