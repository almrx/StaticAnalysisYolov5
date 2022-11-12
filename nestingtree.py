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
treedic={}

def addArgs(somenode, args):
    for i in args:
        if isinstance(i, ast.Constant):
            somenode.args.append(i.value)
            continue
        elif isinstance(i, ast.Name):
            if i.id in treedic:
                somenode.args.append(treedic[i.id])
            else:
                somenode.args.append(i.id)
            continue
        #print(ast.dump(i))
        nodeobj=Node(i.func.value.id+'.'+i.func.attr, [])
        addArgs(nodeobj, i.args)
        somenode.args.append(nodeobj)

class GetAssignments(ast.NodeVisitor):
    def visit_Assign(self, node):
        #print(ast.dump(node.value))
        global root
        root=Node('null',[])
        if isinstance(node.value, ast.Constant):
            root.func=node.value.value
            return
        root.func=node.value.func.value.id+'.'+node.value.func.attr
        addArgs(root, node.value.args)

        treedic[node.targets[0].id]=root


#code='A = np.dot(np.array(1), np.array(2))'
#code='A = np.array(2)'
with open('example_nest.py', 'r', encoding='utf8') as f: 
    src = f.read()
    
tree=ast.parse(src,mode='exec')

#print(ast.dump(tree.body[0]))
'''
Assign(targets=[Name(id='A', ctx=Store())], value=Call(func=Attribute(value=Name(id='np', ctx=Load()), attr='dot', ctx=Load()), args=[Call(func=Attribute(value=Name(id='np', ctx=Load()), attr='array', ctx=Load()), args=[Constant(value=1, kind=None)], keywords=[]), Call(func=Attribute(value=Name(id='np', ctx=Load()), attr='array', ctx=Load()), args=[Constant(value=2, kind=None)], keywords=[])], keywords=[]), type_comment=None)
'''

GetAssignments().visit(tree)

for key in treedic:
    print(key, ': ', treedic[key].ExpString())

