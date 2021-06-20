class Integer:
    def __init__(self, value):
        self.value = value
class Array:
    pass
class String:
    pass
class Block:
    def __init__(self, content):
        self.content = content
    def execute(self):
        return interpret(self.content)

def stringify(code):
    pass

def interpret(code, **kwargs):
    stk = []
    if 'input' in kwargs.keys():
        inp = kwargs['input']
        if all([i in '0123456789 ' for i in inp]):
            stk.append(list(map(int,inp.strip().split(' '))))
    
    for l in code:
        if l=='~':
            x = stk.pop()
            if type(x) == int:
                stk.append(-(x+1))
            elif type(x) == str:
                stk.append(interpret(x))
            elif type(x) == Block:
                stk.append(Block.execute())
            elif type(x) == list:
                for i in x:
                    stk.append(i)
        elif l=='`':
            x = stk.pop()
            if type(x) == int:
                stk.append(str(x))
    return stk

print(interpret('~', input='1 3 5'))