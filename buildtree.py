import ast, tokenize, csv, sys

class Node:
    def __init__(self, func, args):
        self.func=func
        self.args=args

    def ExpString(self):
        if not isinstance(self.func, str):
            s=str(self.func)
            return s
        s=self.func+'('
        for i in self.args:
            if isinstance(i, Node):
                s+=i.ExpString()
            else:
                s+=str(i)
            if not i is self.args[-1]:
                s+=','
        s+=')'
        return s

#a=Node('dot',['b','c'])
#print(a.ExpString())

root=Node('null',[])

def addArgs(somenode, args):
    for i in args:
        if isinstance(i, ast.Constant):
            somenode.args.append(i.value)
            continue
        #print(ast.dump(i))
        nodeobj=Node(i.func.value.id+'.'+i.func.attr, [])
        addArgs(nodeobj, i.args)
        somenode.args.append(nodeobj)

class GetAssignments(ast.NodeVisitor):
    def visit_Assign(self, node):
        #print(ast.dump(node.value))
        global root
        if isinstance(node.value, ast.Constant):
            root.func=node.value.value
            return
        root.func=node.value.func.value.id+'.'+node.value.func.attr
        addArgs(root, node.value.args)


code='A = np.dot(np.array(1), np.array(2))'
#code='A = np.array(2)'

tree=ast.parse(code,mode='exec')

#print(ast.dump(tree.body[0]))
'''
Call(func=Attribute(value=Name(id='np', ctx=Load()), attr='dot', ctx=Load()), 
args=[Call(func=Attribute(value=Name(id='np', ctx=Load()), attr='array', ctx=Load()), 
args=[Constant(value=1, kind=None)], keywords=[]), Call(func=Attribute(value=Name(id='np', 
ctx=Load()), attr='array', ctx=Load()), args=[Constant(value=2, kind=None)], keywords=[])], 
keywords=[])
'''

GetAssignments().visit(tree)

print(root.ExpString())
