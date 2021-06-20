class Integer:
    def __init__(self, value):
        self.value = int(value)
    def __repr__(self):
        return str(self.value)
    def stringify(self):
        return str(self.value)

class Array:
    def __init__(self, value):
        self.value = list(value)
    def __repr__(self):
        return '['+' '.join([str(i) for i in self.value])+']'
    def stringify(self):
        return '['+' '.join([str(i) for i in self.value])+']'
    def __iter__(self):
        return iter(self.value)

class String:
    def __init__(self, value):
        self.value = str(value)
    def __repr__(self):
        return self.value
    def stringify(self):
        return '"'+str(self.value)+'"'

class Block:
    def __init__(self, value):
        self.value = str(value)
    def __repr__(self):
        return '{'+str(self.value)+'}'
    def stringify(self):
        return '{'+str(self.value)+'}'

def interpret(code, **kwargs):
    stk = []
    if 'input' in kwargs.keys():
        inp = kwargs['input']
        if all([i in '0123456789 ' for i in inp]):
            stk.append(Array(map(Integer,inp.strip().split(' '))))
        else:
            stk.append(inp)
    
    for l in code:
        if l=='~':
            x = stk.pop()
            if type(x) == Integer:
                stk.append(-(x+1))
            elif type(x) == Array:
                for i in x:
                    stk.append(i)
            elif type(x) in [String, Block]:
                stk.append(interpret(x))
        elif l=='`':
            x = stk.pop()
            stk.append(x.stringify())
    return stk