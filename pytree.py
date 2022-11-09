class Node:
    def __init__(self, func, args):
        self.func=func
        self.args=args

    def PrintExp(self):
        print(self.func,'(',end="")
        for i in self.args:
            #print(type(i))
            if isinstance(i, Node):
                i.PrintExp()
            else:
                print(i, end='')
            if not i is self.args[-1]:
                print(',', end='')
        print(')', end='')

a=Node('dot',['b', 3])
a.PrintExp()
print(' ')
a.args[0]=Node('array',[2, 'c', 7])
a.PrintExp()
print(' ')
a.args[0].args[1]=Node('array',[5, 9])
a.PrintExp()
print(' ')
