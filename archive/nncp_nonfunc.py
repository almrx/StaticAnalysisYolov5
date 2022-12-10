import ast, tokenize, csv, sys

# get hard list linear operations from file
#hardList_linearOps = list(csv.reader(open('linear_op_list.csv','r'), delimiter=','))[0]

#print (hardList_linearOps)
# dictionary to save all linear ops by annotated str
linear_ops = {}
blank_lines = []

#print(str(sys.argv[1]))

'''
spec = open(str(sys.argv[1]), 'r')
spec_lines = spec.readlines()
spec_lines = [x.replace('\n', '').replace(' ', '') for x in spec_lines]
#print(spec_lines)
'''

# read file && test tokenize
with open(str(sys.argv[1]), 'r', encoding='utf8') as f: 
    src = f.read()
'''
flag=True
c=0

with tokenize.open(str(sys.argv[1])) as f:
    token_src = tokenize.generate_tokens(f.readline)
    for token in token_src:
        #print(token)
        if token.type==60 and 'nncp' in token.string:
            #print(token.string.split('nncp'))
            tmpstr=token.string.split('nncp')[1].replace(' ', '')
            if spec_lines[c]!=tmpstr:
                print("Specification ",c+1,": ",spec_lines[c]," does not match annotation ",tmpstr," on line ",token.start[0])
                exit()
            c+=1
            linear_ops[token.start[0]] = tmpstr
            flag=False
            continue
        if token.type==61 and flag:
            blank_lines.append(token.start[0])
        flag=True

print(blank_lines)
'''
#print (type(src), src)
#print (type(token_src))

## test ast 
class GetAssignments(ast.NodeVisitor):
    def visit_Assign(self, node):
        if isinstance(node.value, ast.Constant):
            return
        print(ast.dump(node.value))
        '''
        if hasattr(node.value.func.value, "attr"):
            #print(node.value.func.value.value.id," ",node.value.func.value.attr," ",node.value.func.attr)
            if node.value.func.value.value.id not in hardList_linearOps or node.value.func.value.attr not in hardList_linearOps or node.value.func.attr not in hardList_linearOps:
                return
        else:
            #print(node.value.func.value.id," ",node.value.func.attr)
            if node.value.func.value.id not in hardList_linearOps or node.value.func.attr not in hardList_linearOps:
                return
        c=1
        while (node.lineno-c) in blank_lines:
            c+=1
            if c>=6:
                print("match not found: ",ast.dump(node.value)," on line ",node.lineno," more than 5 blank lines")
                return
        if (node.lineno-c) in linear_ops.keys():
            if hasattr(node.value.func.value, "attr"):
                if node.value.func.value.value.id not in linear_ops[node.lineno-c]:
                    print("match not found: ",ast.dump(node.value)," on line ",node.lineno," couldn't find ",node.value.func.value.value.id," in annotation",linear_ops[node.lineno-c])
                    return
                if node.value.func.value.attr not in linear_ops[node.lineno-c]:
                    print("match not found: ",ast.dump(node.value)," on line ",node.lineno," couldn't find ",node.value.func.value.attr," in annotation",linear_ops[node.lineno-c])
                    return
                if node.value.func.attr not in linear_ops[node.lineno-c]:
                    print("match not found: ",ast.dump(node.value)," on line ",node.lineno," couldn't find ",node.value.func.attr," in annotation",linear_ops[node.lineno-c])
                    return
                print('match: ',node.value.func.attr," on line ",node.lineno," ",ast.dump(node.value),'\n')
            else:
                if node.value.func.value.id not in linear_ops[node.lineno-c]:
                    print("match not found: ",ast.dump(node.value)," on line ",node.lineno," couldn't find ",node.value.func.value.id," in annotation",linear_ops[node.lineno-c])
                    return
                if node.value.func.attr not in linear_ops[node.lineno-c]:
                    print("match not found: ",ast.dump(node.value)," on line ",node.lineno," couldn't find ",node.value.func.attr," in annotation",linear_ops[node.lineno-c])
                    return
                print('match: ',node.value.func.attr," on line ",node.lineno," ",ast.dump(node.value),'\n')
        else:
            print("match not found: ",ast.dump(node.value)," on line ",node.lineno," annotation not found")
        '''
            



# get the annotaiton from string. 
# only print str that has 'nncp'
'''
class ConstantVisitor(ast.NodeVisitor):
    def visit_Constant(self,node):
        #print('Node type: Constant\nFields: ', node._fields, node.value, node.kind)
        if ( isinstance(node.value, str) and 'nncp' in node.value): 
            # TODO: check this value is valid before adding to dict. check if the value is part of the linear op hard list
            linear_ops[node.lineno] = node.value.split('nncp')[1].replace(' ', '')
            
        ast.NodeVisitor.generic_visit(self, node)
'''


tree = ast.parse(src, mode='exec')

#print ("\n ---- AST TREE STARTED -----\n")
#ConstantVisitor().visit(tree)
#print (type (tree) , tree, tree.lineno)
#print (linear_ops)

GetAssignments().visit(tree)

#print ("\n ---- AST TREE END-----\n")

#print (ast.dump(tree))

'''
Module(
    body=[
        Expr(value=Constant(value='\nThis file services as an example of liner operation\n\n', kind=None)), 
        Import(names=[alias(name='numpy', asname='np')]), 
        Assign(targets=[Name(id='a', ctx=Store())], value=Constant(value=3, kind=None), type_comment=None), 
        Assign(targets=[Name(id='b', ctx=Store())], value=Constant(value=4, kind=None), type_comment=None), 
        Assign(targets=[Name(id='output', ctx=Store())], value=Call(func=Attribute(value=Name(id='np', ctx=Load()), attr='dot', ctx=Load()), args=[Name(id='a', ctx=Load()), Name(id='b', ctx=Load())], keywords=[]), type_comment=None), 
        Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Name(id='output', ctx=Load())], keywords=[]))
        ], 
    type_ignores=[]
    )
'''

