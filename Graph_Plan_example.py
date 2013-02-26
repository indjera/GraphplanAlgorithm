from Graph_Plan import *
have_cake = Literal("HaveCake")
eten_cake = Literal("EatenCake",False)
init=[have_cake,eten_cake]
goal=[Literal("HaveCake"),Literal("EatenCake")]
actions=[Action("Eat",Literal("HaveCake"),[Literal("HaveCake",False),Literal("EatenCake")]),Action("Bake",Literal("HaveCake",False),Literal("HaveCake"))]
graph_plan_example = Graph_Plan(init,goal,actions)
#graph_plan_example.expand_graph()
#graph_plan_example.expand_graph()
solution = graph_plan_example.make_graph_plan()
print("---------------------------SOLUTION--------------------------")
for i in solution:
    print("___________________________________________________________")
    for j in i:
        print(j[0],end=" - ")
        j[1].print_literal()
    print("___________________________________________________________")    
print("-------------------------END_SOLUTION-------------------------")
