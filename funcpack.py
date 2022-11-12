import ast

funcName = ""
def packFunc(node):
    global funcName
    if isinstance(node, ast.Name):
        if funcName == "":
            funcName = node.id
        else:
            funcName = node.id+"."+funcName
        return node.id
    else: # is an ast.Attribute
        if hasattr(node, 'attr'):
            if funcName == "":
                funcName = node.attr
            else: 
                funcName = node.attr+"."+funcName
        return packFunc(node.value)


code=['x=f()','x=g.f()','x=h.g.f()']

for i in code:
    tree=ast.parse(i,mode='exec')
    #print(ast.dump(tree.body[0].value),'\n')
    if isinstance(tree.body[0].value, ast.Call):
        packFunc(tree.body[0].value.func)
    print (funcName)
    funcName = ""

#  hasattr(node.value.func.value, "attr")

'''
Call(func=Name(id='f', ctx=Load()), args=[], keywords=[]) 

Call(func=Attribute(value=Name(id='g', ctx=Load()), attr='f', ctx=Load()), args=[], keywords=[]) 

Call(func=Attribute(value=Attribute(value=Name(id='h', ctx=Load()), attr='g', ctx=Load()), attr='f', ctx=Load()), args=[], keywords=[]) 
'''


'''

 if not hasattr(node.value.func, "attr"):
    if node.value.func.id not in linear_ops[node.lineno-c]:
        print("match not found: ",ast.dump(node.value)," on line ",node.lineno," couldn't find ",node.value.func.id," in annotation",linear_ops[node.lineno-c])
        return
    print('match: user defined function: ',node.value.func.id," on line ",node.lineno," ",ast.dump(node.value),'\n')
elif hasattr(node.value.func.value, "attr"):
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
'''