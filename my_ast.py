class Node:
    def __init__(self, value: str, children: list):
        self.value = value
        self.children = children
    def evaluate(self) -> int:
        pass

class UnOp(Node):
    def evaluate(self) -> int:
        if self.value == '-':
            return -self.children[0].evaluate()
        if self.value == '!':
            return not self.children[0].evaluate()
        return self.children[0].evaluate()
    
class BinOp(Node):
    def evaluate(self) -> int:
        if self.value == '*':
            return self.children[0].evaluate() * self.children[1].evaluate()
        if self.value == '/':
            return self.children[0].evaluate() // self.children[1].evaluate()
        if self.value == '+':
            return self.children[0].evaluate() + self.children[1].evaluate()
        if self.value == '-':
            return self.children[0].evaluate() - self.children[1].evaluate()
        if self.value == '==':
            return self.children[0].evaluate() == self.children[1].evaluate()
        if self.value == '>':
            return self.children[0].evaluate() > self.children[1].evaluate()
        if self.value == '<':
            return self.children[0].evaluate() < self.children[1].evaluate()
        if self.value == '||':
            return self.children[0].evaluate() or self.children[1].evaluate()
        if self.value == '&&':
            return self.children[0].evaluate() and self.children[1].evaluate()
        
class While(Node):
    def evaluate(self) -> int:
        while self.children[0].evaluate():
            self.children[1].evaluate()

class If(Node):
    def evaluate(self) -> int:
        if self.children[0].evaluate():
            self.children[1].evaluate()
        elif len(self.children) == 3:
            self.children[2].evaluate()

class IntVal(Node):
    def __init__(self, value: str):
        self.value = value
    def evaluate(self) -> int:
        return self.value
    
class Block(Node):
    def evaluate(self) -> int:
        for child in self.children:
            child.evaluate()
    
class Identifier(Node):
    def __init__(self, value: str):
        self.value = value
    def evaluate(self) -> int:
        return Symbol_table.getter(self.value)
        

class Println(Node):
    def evaluate(self) -> int:
        print(self.children[0].evaluate())
    
class Readln(Node):
    #make empty init
    def __init__(self):
        pass
    def evaluate(self) -> int:
        return int(input())

class Assignment(Node):
    def evaluate(self) -> int:
        Symbol_table.setter(self.children[0].value, self.children[1].evaluate())

class Symbol_table():
    var_dict = {}
    @staticmethod
    def getter(value):
        if value in Symbol_table.var_dict:
            return Symbol_table.var_dict[value]
        else:
            raise Exception("Variable not defined")
    @staticmethod
    def setter(key, value):
        Symbol_table.var_dict[key] = value

class NoOp(Node):
    pass