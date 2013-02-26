import itertools
from Literal import * 
from Action import *
from Mutex  import *      
class Graph_Plan:
    def __init__(self,initial,goal,actions):
        self.Goal =[]
        self.Goal.extend(goal)
        self.Initial =[] 
        self.Initial.extend(initial)
        self.list_of_action =[] 
        self.list_of_action.extend(actions)
        self._graph_plan = []
        self._graph_plan.append(initial)
        self._action_mutex=[]
        self._literal_mutex=[]
        
    def get_mutexs_by_level(self,level):
        if level >= 0:
            if (level%2) == 0:
                return filter(lambda x:x.level==level,self._literal_mutex)
            else:
                return filter(lambda x:x.level==level,self._action_mutex)
            
    def get_elements_by_level(self,level):
        return self._graph_plan[level]
     
    def _add_trivial_actions(self,level):
        elements = self.get_elements_by_level(level-1)
        for i in elements:
            action = Action(i.name+"NoOP",i,i)
            self._graph_plan[level].append(action)
            
    def _add_trivial_literal_mutex(self,level):
        if level > 1 and level%2 == 0:
            elements =self.get_elements_by_level(level) 
            for i in itertools.combinations(elements,2):
                if i[0].negate(i[1]):
                    self._literal_mutex.append(Mutex(i[0],i[1],level,"literalInconsistent"))
        
    def check_for_mutex(self):
        level = len(self._graph_plan) - 2
        actions = self.get_elements_by_level(-2)
        for pair_action in itertools.combinations(actions,2):
            if pair_action[0].negate_eff(pair_action[1].eff):
                self._action_mutex.append(Mutex(pair_action[0],pair_action[1],level,"Inconsistent"))
            elif pair_action[0].negate_eff(pair_action[1].preC):
                self._action_mutex.append(Mutex(pair_action[0],pair_action[1],level,"Interference"))
            elif pair_action[0].negate_preC(pair_action[1].preC):
                self._action_mutex.append(Mutex(pair_action[0],pair_action[1],level,"CompetingNeeds"))                
            
    def expand_graph(self):        
        level_actions= []
        level_literals = []
        level_literals.extend(self._graph_plan[-1])
        for i in self.list_of_action:
            for j in self._graph_plan[-1]:
                if i.member_in_preC(j):
                    level_actions.append(i)          
                    level_literals.extend(filter(lambda x:not self.member_in_graph(x,len(self._graph_plan)-1),i.eff)) 
        self._graph_plan.append(level_actions)
        self._add_trivial_actions(len(self._graph_plan)-1)
        self._graph_plan.append(level_literals)
        self._add_trivial_literal_mutex(len(self._graph_plan)-1)
        self.check_for_mutex()
        
    def member_in_graph(self,elem,level):
        return list(filter(lambda x:x.eq(elem),self.get_elements_by_level(level)))
            
    def _goal_all_in(self):
        for i in self.Goal:
            if not list(filter(lambda x:x.eq(i),self._graph_plan[-1])):
                return False
        return True
    
    def _goal_without_mutex(self,level):
        for i in itertools.combinations(self.Goal,2): 
            if self.member_in_literal_mutex(i[0],i[1], level):
                return False
        return True
    
    def goal_ok(self,level):
        return self._goal_all_in() and self._goal_without_mutex(level)
    
    def member_in_action_mutex(self,act1,act2,level):
        return list(filter(lambda x:x.eq(Mutex(act1,act2,level,"")),self.get_mutexs_by_level(level)))
    
    def member_in_literal_mutex(self,act1,act2,level):
        return list(filter(lambda x:x.eq(Mutex(act1,act2,level,"")),self.get_mutexs_by_level(level)))
    def __new_filter(self,tmp4,z):
        list_to_return=[]
        for n in itertools.combinations(tmp4,z):
            list_to_return.append(n)
        return list_to_return 
        
    def __myfilter(self,list1,list2,k):
        list3 = []
        list1 = map(lambda x:(1,x),list1)
        list2 = map(lambda x:(2,x),list2)
        list3.extend(list1)
        list3.extend(list2)
        print(list3)
        list_to_return = []
        for i in itertools.combinations(list3,k):
            for j in i:
                ok = len(list(filter(lambda x:x[0]==j[0],i))) == 1
            if ok:
                list_to_return.append(list(map(lambda x:x[1],i)))
        return list_to_return
    def extract_solution(self):
        stack = []
        stack.append(list(map(lambda x:("end",x),self.Goal)))
#        stack.append(self.Goal)
        actions = []
        level = len(self._graph_plan) -1
        solution = []
        while len(stack)>0 and level > 0:
            actions = self._graph_plan[level - 1]
            curr_actions = []
            success = stack.pop()
            for i in success:
                for j in actions:
                    if j.member_in_eff(i[1]):
                        curr_actions.append((i[1].name,j))
            without_mutex = []
            for i in itertools.combinations(curr_actions, len(success)):
                for j in itertools.combinations(i,2):
                    if not self.member_in_action_mutex(j[0][1],j[1][1],level-1):
                        without_mutex.append(i)                        
            unique_without_mutex = []
            ok = False
            for i in without_mutex:
                for j in i:
                    ok = len(list(filter(lambda x:x[0]==j[0],i))) == 1
                if ok:
                    unique_without_mutex.append(i)
            if unique_without_mutex:
                level = level -2
                solution.append(success)    
#                for i in unique_without_mutex:
#                    stack.extend(self.__myfilter(i[0][1].preC,i[1][1].preC,len(success)))
                tmp4 = []
                for i in unique_without_mutex:
                    for k in i:
                        tmp4.extend(map(lambda x:(k[1].name,x),k[1].preC))
                
                stack.extend(self.__new_filter(tmp4,len(success)))
        if len(stack)>0:
            solution.append(stack.pop())
        return solution 
    def end_of_plan(self):
        if len(self._graph_plan)>2:
            if len(self._graph_plan[-1]) == len(self._graph_plan[-3]):
                return -1
    def make_graph_plan(self):
        while True:
            if self.goal_ok(len(self._graph_plan)-1):
                solution = self.extract_solution()
                if solution :
                    return solution
                elif -1 == self.end_of_plan():
                    return None
            self.expand_graph()
                
            
                
            