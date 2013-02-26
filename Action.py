class Action:
    def __init__(self,name,preC,eff):
        self.name = name
        self.preC = []
        if type( preC ) == list:
            self.preC.extend(preC)
        else:
            self.preC.append(preC)
        self.eff  = []
        if type(eff) == list:
            self.eff.extend(eff)
        else:
            self.eff.append(eff)
        
    def __negates(self,action_param1,action_param2):
        for i in action_param1:
            for j in action_param2:
                if i.negate(j):
                    return True;
        return False              
    
    def negate_preC(self,arg):
        return self.__negates(self.preC,arg)
    
    def negate_eff(self,arg):
        return self.__negates(self.eff, arg)
    
    def member_in_preC(self,literal):
        if list(filter(lambda x:x.eq(literal),self.preC)):
            return True
        else:
            return False 
    def member_in_eff(self,literal):
        if list(filter(lambda x:x.eq(literal),self.eff)):
            return True
        else:
            return False 
        
    def eq(self,action_to_cmp):
        return self.name == action_to_cmp.name
    
    def print_action(self):
        print(self.name)
        print("preC:")
        for i in self.preC:
            i.print_literal()
        print("eff:")
        for i in self.eff:
            i.print_literal()
            
        
        
        
       
