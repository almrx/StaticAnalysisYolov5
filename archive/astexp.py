import ast, tokenize, csv, sys

class GetAssignments(ast.NodeVisitor):
    def visit_Assign(self, node):
        print(ast.dump(node.value))

code = "a = np.array(2)"

tree=ast.parse(code,mode='exec')

#print(ast.dump(tree.body[0]))

GetAssignments().visit(tree)

'''
parse of : A = np.dot(np.array(1), np.array(2))

Call(
    func=Attribute(
        value=Name(id='np', ctx=Load()), 
        attr='dot', 
        ctx=Load()
    ), 
    args=[
        Call(func=Attribute(
                value=Name(id='np', ctx=Load()), 
                attr='array', 
                ctx=Load()
            ), 
            args=[Constant(value=1)], 
            keywords=[]), 
        Call(func=Attribute(
                value=Name(id='np', ctx=Load()), 
                attr='array', 
                ctx=Load()
            ), 
            args=[Constant(value=2)], 
            keywords=[])], 
            keywords=[]
)
'''