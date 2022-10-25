import ast
import tokenize

# dictionary to save all linear ops by annotated str
linear_ops = {}

# read file && test tokenize
with open('example_basic.py', 'r', encoding='utf8') as f: 
    src = f.read()
    token_src = tokenize.generate_tokens(f.readline)
    for token in token_src:
        print(token)

#print (type(src), src)
#print (type(token_src))

## test ast 
class GetAssignments(ast.NodeVisitor):
    def visit_Assign(self, node):
        if (node.lineno-1) in linear_ops.keys():
            if linear_ops[node.lineno-1]==node.value.func.attr:
                print('match: '+node.value.func.attr+'\n')
            



# get the annotaiton from string. 
# only print str that has 'nncp'
class ConstantVisitor(ast.NodeVisitor):
    def visit_Constant(self,node):
        #print('Node type: Constant\nFields: ', node._fields, node.value, node.kind)
        if ( isinstance(node.value, str) and 'nncp' in node.value): 
            # TODO: check this value is valid before adding to dict. check if the value is part of the linear op hard list
            linear_ops[node.lineno] = node.value.split('nncp')[1].replace(' ', '')
            
        ast.NodeVisitor.generic_visit(self, node)



tree = ast.parse(src, mode='exec')

print ("\n ---- AST TREE STARTED -----\n")
ConstantVisitor().visit(tree)
#print (type (tree) , tree, tree.lineno)
print (linear_ops)

GetAssignments().visit(tree)

print ("\n ---- AST TREE END-----\n")

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
