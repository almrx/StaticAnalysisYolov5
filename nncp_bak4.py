import ast, tokenize, csv, sys

# read specifiction 
with open(str(sys.argv[1]), 'r') as f: 
    spec = f.read()

# read code from file 
with open(str(sys.argv[2]), 'r', encoding='utf8') as f: 
    src = f.read()

# Node structure: used for the function representation.  
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

# temp vars
root=Node('null',[])
spec_vars_list=[]

#create dictionary
spec_treedic={}
src_treedic={}

# use the tokenize to annotation in the specification file 
# The target annotation is used to ma 
with tokenize.open(str(sys.argv[1])) as f:
    token_src = tokenize.generate_tokens(f.readline)
    for token in token_src:
        #print(token)
        if token.type==60 and 'check' in token.string:
            tmpvars=token.string.split('check')[1].split(' ')
            spec_vars_list.extend(tmpvars)
            del spec_vars_list[0]

# populate args
def addArgsSpec(somenode, args):
    global spec_treedic
    for i in args:
        if isinstance(i, ast.Constant):
            somenode.args.append(i.value)
            continue
        elif isinstance(i, ast.Name):
            if i.id in spec_treedic:
                somenode.args.append(spec_treedic[i.id])
            else:
                somenode.args.append(i.id)
            continue
        #print(ast.dump(i))
        nodeobj=Node(i.func.value.id+'.'+i.func.attr, [])
        addArgsSpec(nodeobj, i.args)
        somenode.args.append(nodeobj)

def addArgsSrc(somenode, args):
    global src_treedic
    for i in args:
        if isinstance(i, ast.Constant):
            somenode.args.append(i.value)
            continue
        elif isinstance(i, ast.Name):
            if i.id in src_treedic:
                somenode.args.append(src_treedic[i.id])
            else:
                somenode.args.append(i.id)
            continue
        #print(ast.dump(i))
        nodeobj=Node(i.func.value.id+'.'+i.func.attr, [])
        addArgsSrc(nodeobj, i.args)
        somenode.args.append(nodeobj)

# visit assignments
class GetAssignmentsSpec(ast.NodeVisitor):
    def visit_Assign(self, node):
        #print(ast.dump(node.value))
        global root, spec_treedic
        root=Node('null',[])
        if isinstance(node.value, ast.Constant):
            root.func=node.value.value
            return
        elif isinstance(node.value, ast.Name):
            if node.value.id in spec_treedic:
                root.args.append(spec_treedic[node.value.id])
            else:
                root.args.append(node.value.id)
            return
        root.func=node.value.func.value.id+'.'+node.value.func.attr
        addArgsSpec(root, node.value.args)

        spec_treedic[node.targets[0].id]=root

class GetAssignmentsSrc(ast.NodeVisitor):
    def visit_Assign(self, node):
        if node.targets[0].id not in spec_treedic:
            return
        #print(ast.dump(node.value))
        global root, src_treedic
        root=Node('null',[])
        if isinstance(node.value, ast.Constant):
            root.func=node.value.value
            return
        elif isinstance(node.value, ast.Name):
            if node.value.id in src_treedic:
                root.args.append(src_treedic[node.value.id])
            else:
                root.args.append(node.value.id)
            return
        root.func=node.value.func.value.id+'.'+node.value.func.attr
        addArgsSrc(root, node.value.args)

        src_treedic[node.targets[0].id]=root

#execute
# parse the specification file and build the spec_treeDict 
spec_tree=ast.parse(spec,mode='exec')
GetAssignmentsSpec().visit(spec_tree)

for i in spec_vars_list:
    if i not in spec_treedic:
        print("Error: Variable ",i," specified for checking is not defined in the specification.")
        sys.exit(0)

# parse and build the src tree and its dicationary 
src_tree=ast.parse(src,mode='exec')
GetAssignmentsSrc().visit(src_tree)

#check for incompatibilities
for key in spec_vars_list:
    if key not in src_treedic:
        print("Warning: Variable ", key, " is not defined in the code.")
        continue
    if not spec_treedic[key].ExpString() == src_treedic[key].ExpString():
        print("Warning: Variable ", key, "does not match specification. Details: Specification: ",spec_treedic[key].ExpString(),". Code: ",src_treedic[key].ExpString(),".")
        continue
    print("Match: Variable ",key," matches specification. Details: ",spec_treedic[key].ExpString(),".")

