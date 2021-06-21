# if type(other) == Integer:
# elif type(other) == Array:
# elif type(other) == String:
# elif type(other) == Block:

class Integer:
    def __init__(self, value):
        self.value = int(value)
        self.string = str(value)
    def __repr__(self):
        return str(self.value)
    def __add__(self, other):
        if type(other) == Integer:
            return Integer(self.value + other.value)
        elif type(other) == Array:
            return Array([self] + other.value)
        elif type(other) == String:
            return String(self.string + other.value)
        elif type(other) == Block:
            return Block(self.string + ' ' + other.value)
        else:
            return self.value + other
    def interpret(self):
        return [self.value]

class Array:
    def __init__(self, value):
        if type(value) == String:
            value = value.value
        if type(value) == str:
            self.value = interpret(value, input=None)
        else:
            self.value = list(value)
        self.string = '['+' '.join([i.string for i in self.value])+']'
    def __repr__(self):
        return ''.join([repr(i) for i in self.value])
    def __add__(self, other):
        if type(other) == Integer:
            return Array(self.value + [other])
        elif type(other) == Array:
            return Array(self.value + other.value)
        elif type(other) == String:  # NOT OFFICIAL
            return Array(self.value + [other])
        elif type(other) == Block:
            return Block(self.string[1:-1] + ' ' + other.value)
        else:
            return self.value + other
    def interpret(self):
        return self.value
    def __iter__(self):
        return iter(self.value)

class String:
    def __init__(self, value):
        self.value = str(value)
        self.string = str(self.value)
    def __repr__(self):
        return '`'+self.value+'`'
    def __add__(self, other):
        if type(other) == Integer:
            return String(self.value + str(other.value))
        elif type(other) == Array:  # NOT OFFICIAL
            return Array([self.value] + other.value)
        elif type(other) == String:
            return String(self.value + other.value)
        elif type(other) == Block:
            return Block(self.value + ' ' + other.value)
        else:
            return self.value + other
    def interpret(self):
        return interpret(self.value, input=None)

class Block:
    def __init__(self, value):
        self.value = str(value)
        self.string = '{'+self.value+'}'
    def __repr__(self):
        return '{'+self.value+'}'
    def __add__(self, other):
        if type(other) == Integer:
            return Block(self.value + ' ' + other.string)
        elif type(other) == Array:
            return Block(self.value + ' ' + other.string[1:-1])
        elif type(other) == String:
            return Block(self.value + ' ' + other.value)
        elif type(other) == Block:
            return Block(self.value + ' ' + other.value)
        else:
            return self.value + other
    def interpret(self):
        return interpret(self.value, input=None)

class UnknownTypeError(Exception):
    pass
class EmptyStackError(Exception):
    pass

def interpret(code, **kwargs):
    stk = []
    if 'input' in kwargs.keys():
        inp = kwargs['input']
        if inp != None:
            stk.append(String(inp))
    else:
        stk.append("")
     
    num=None
    i=0
    while i < len(code):
        l = code[i]
        if l == '~':
            if len(stk) < 1:
                raise EmptyStackError('tried to pop from empty stack')
            x = stk.pop()
            if type(x) == Integer:
                stk.append(Integer(-(x+1)))
            elif type(x) == Array:
                stk.extend(x.value)
            elif type(x) in [String, Block]:
                stk.extend(x.interpret())
            else:
                raise UnknownTypeError('type of x is '+str(type(x)))
        elif l == '`':
            if len(stk) < 1:
                raise EmptyStackError('tried to pop from empty stack')
            x = stk.pop()
            if type(x) not in [Integer, Array, String, Block]:
                raise UnknownTypeError('type of x is '+str(type(x)))
            stk.app/end(String(x.string))
        elif l == 'p':
            if len(stk) < 1:
                raise EmptyStackError('tried to pop from empty stack')
            x = stk.pop()
            if type(x) not in [Integer, Array, String, Block]:
                raise UnknownTypeError('type of x is '+str(type(x)))
            print(x.string)
        elif l == '+':
            if len(stk) < 2:
                raise EmptyStackError('tried to pop from empty stack')
            x = stk.pop()
            y = stk.pop()
            if type(x) not in [Integer, Array, String, Block] or type(y) not in [Integer, Array, String, Block]:
                raise UnknownTypeError('type of x is '+str(type(x)))
            stk.append(x+y)
        elif l == '[':
            end = code.find(']', i)
            if end!=-1:
                stk.append(Array(String(code[i+1:end])))
                i=end+1
        elif l == ']':
            stk.append(Array(String(code[0:i])))
        elif l == '\\':
            if len(stk) < 2:
                raise EmptyStackError('tried to pop from empty stack')
            x = stk.pop()
            y = stk.pop()
            stk.append(x)
            stk.append(y)
        elif l in '0123456789':
            if num==None:
                num=0
            num*=10
            num+=int(l)
        elif l == ' ':
            if num!=None:
                stk.append(Integer(num))
                num=None
        elif l == '#':
            end = code.find('\n', i)
            if end==-1:
                return
            else:
                i=end
        i += 1
    if num!=None:
        stk.append(Integer(num))
    return stk