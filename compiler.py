import sys

EOF = 1
PLUS = 2
MINUS = 3
MULT = 4
DIV = 5
OPENKEY = 6
CLOSEKEY = 7

reserved_words = ['INITIATING_COUNTDOWN_SEQUENCE', 'WE_HAVE_LIFTOFF', 'StageBlueprint', 'BuildStage', 'Program', 'requires', 'EndProgram', 'initiate', 'beginBurn', 'for', 'Shutdown', 'flightStatusReport', 'else', 'houstonWeReadYou', 'is', 'seconds', 'minutes', 'hours', 'confirm', 'end', 'Int', 'String', 'function', 'return', 'print']

class Node:
    def __init__(self, value: str, children: list):
        self.value = value
        self.children = children
    def evaluate(self, symbol_table) -> int:
        pass

class UnOp(Node):
    def evaluate(self, symbol_table) -> int:
        child = self.children[0].evaluate(symbol_table)
        type = child[0]
        val = child[1]
        if type != 'Int':
            raise Exception("Variable type mismatch")
        if self.value == '-':
            return (type, -val)
        if self.value == '!':
            return (type, not val)
        return (type, val)
    
class BinOp(Node):
    def evaluate(self, symbol_table):
        child0 = self.children[0].evaluate(symbol_table)
        child1 = self.children[1].evaluate(symbol_table)
        if self.value == '.':
            str0 = str(child0[1])
            str1 = str(child1[1])
            return ('Str' ,str0 + str1)
        if self.value == '*':
            if child0[0] != 'Int' or child1[0] != 'Int':
                raise Exception("Variable type mismatch")
            return ('Int', child0[1] * child1[1])
        if self.value == '/':
            if child0[0] != 'Int' or child1[0] != 'Int':
                raise Exception("Variable type mismatch")
            return ('Int', child0[1] // child1[1])
        if self.value == '+':
            if child0[0] != 'Int' or child1[0] != 'Int':
                raise Exception("Variable type mismatch")
            return ('Int', child0[1] + child1[1])
        if self.value == '-':
            if child0[0] != 'Int' or child1[0] != 'Int':
                raise Exception("Variable type mismatch")
            return ('Int', child0[1] - child1[1])
        if self.value == '==':
            if child0[1] == child1[1]:
               return ('Int', 1)
            return ('Int' , 0)
        if self.value == '>':
            if child0[1] > child1[1]:
               return ('Int', 1) 
            return ('Int', 0)
        if self.value == '<':
            if child0[1] < child1[1]:
               return ('Int', 1) 
            return ('Int', 0)
        if self.value == '||':
            if child0[0] != 'Int' or child1[0] != 'Int':
                raise Exception("Variable type mismatch")
            return ('Int', child0[1] or child1[1])
        if self.value == '&&':
            if child0[0] != 'Int' or child1[0] != 'Int':
                raise Exception("Variable type mismatch")
            return ('Int', child0[1] and child1[1])
        
class While(Node):
    def evaluate(self, symbol_table) -> int:
        while self.children[0].evaluate(symbol_table)[1]:
            self.children[1].evaluate(symbol_table)

class If(Node):
    def evaluate(self, symbol_table) -> int:
        if self.children[0].evaluate(symbol_table)[1]:
            self.children[1].evaluate(symbol_table)
        elif len(self.children) == 3:
            self.children[2].evaluate(symbol_table)

class IntVal(Node):
    def __init__(self, value: str):
        self.value = value
    def evaluate(self, symbol_table) -> int:
        return ('Int', self.value)
    
class StrVal(Node):
    def __init__(self, value: str):
        self.value = value
    def evaluate(self, symbol_table) -> str:
        return ('Str', self.value)
    
class Block(Node):
    def evaluate(self, symbol_table) -> int:
        for child in self.children:
            if child.value == 'return':
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)
    
class Identifier(Node):
    def __init__(self, value: str):
        self.value = value
    def evaluate(self, symbol_table) -> int:
        return symbol_table.getter(self.value)

class Print(Node):
    def evaluate(self, symbol_table) -> int:
        print(self.children[0].evaluate(symbol_table)[1])
    
class Readln(Node):
    def __init__(self):
        pass
    def evaluate(self, symbol_table) -> int:
        return ('Int',int(input()))

class Assignment(Node):
    def evaluate(self, symbol_table) -> int:
        symbol_table.setter(self.children[0].value, self.children[1].evaluate(symbol_table))

class VarDec(Node):
    def evaluate(self, symbol_table) -> int:
        if len(self.children) == 2:
            if self.value == 'String' and self.children[1].evaluate(symbol_table)[0] == 'String':
                symbol_table.create(self.children[0].value, self.children[1].evaluate(symbol_table))
            elif self.value == 'Int' and self.children[1].evaluate(symbol_table)[0] == 'Int':
                symbol_table.create(self.children[0].value, self.children[1].evaluate(symbol_table))
            else:
                raise Exception("Variable type mismatch")
        else:
            if self.value == 'String':
                symbol_table.create(self.children[0].value, ('Str', ''))
            elif self.value == 'Int':
                symbol_table.create(self.children[0].value, ('Int', 0))

class Return(Node):
    def evaluate(self, symbol_table) -> int:
        return self.children[0].evaluate(symbol_table)

class FuncDec(Node):
    def evaluate(self, symbol_table) -> int:
        Func_table.create(self.children[0].value, self)

class FuncCall(Node):
    def evaluate(self, symbol_table) -> int:
        func = Func_table.getter(self.value)
        stage = symbol_table.getter(self.children[0].value)
        new_symbol_table = Symbol_table()
        new_symbol_table.create(func.children[1].value, stage)
        result = func.children[-1].evaluate(new_symbol_table)
        return result

class StageDec(Node):
    def evaluate(self, symbol_table) -> int:
        new_symbol_table = Symbol_table()
        for i in range(len(self.children)-1):
            new_symbol_table.create(self.children[i+1].children[0].value, self.children[i+1].children[1].evaluate(symbol_table))
        symbol_table.create(self.children[0].value, new_symbol_table)
        
class StageIdentifier(Node):
    def evaluate(self, symbol_table) -> int:
        stage_symbol_table = symbol_table.getter(self.value)
        return stage_symbol_table.getter(self.children[1].value)
    
class StageAssignment(Node):
    def evaluate(self, symbol_table) -> int:
        stage_symbol_table = symbol_table.getter(self.value)
        stage_symbol_table.setter(self.children[0].value, self.children[1].evaluate(symbol_table))
        symbol_table.setter(self.value, stage_symbol_table)

class Burn(Node): 
    def evaluate(self, symbol_table) -> int:
        for i in range(self.children[0].evaluate(symbol_table)[1]):
            self.children[1].evaluate(symbol_table)

class NoOp(Node):
    pass

class Symbol_table():
    def __init__(self):
        self.var_dict = {}
    def getter(self, key):
        if key in self.var_dict:
            return self.var_dict[key]
        else:
            raise Exception(f"Variable {key} not defined")
    def setter(self, key, value):
        self.var_dict[key] = value
    def create(self, key, value):
        if key in self.var_dict:
            raise Exception(f'Variable {key} already defined')
        self.var_dict[key] = value

class Func_table():
    var_dict = {}
    @staticmethod
    def getter(key):
        if key in Func_table.var_dict:
            return Func_table.var_dict[key]
        else:
            raise Exception("Variable not defined")
    @staticmethod
    def create(key, value):
        if key in Func_table.var_dict:
            raise Exception("Variable already defined")
        Func_table.var_dict[key] = value

class Token:
    def __init__(self, value, type):
        self.value  = value
        self.type   = type

class PrePro():
    source_code = ""
    @staticmethod
    def filter():
        comment_start = PrePro.source_code.find('#')
        while(comment_start != -1):
            t = PrePro.source_code[comment_start:-1]
            comment_end = PrePro.source_code[comment_start:-1].find('\n')
            if comment_end == -1:
                comment_end = len(PrePro.source_code)
            else:
                comment_end += comment_start
            PrePro.source_code = PrePro.source_code.replace(PrePro.source_code[comment_start:comment_end+1], '')
            comment_start = PrePro.source_code.find('#')

        return PrePro.source_code

class Tokenizer:
    def __init__(self, source_code):
        self.source_code    = source_code
        self.position       = 0
        self.next_token     = ''
    def selectNext(self):
        self.token = ''
        while True:
            if (len(self.source_code) <= self.position):
                if(self.token == ''):
                    self.next_token = Token('EOF', EOF)
                    self.position += 1
                    return self.next_token
                else:
                    return self.next_token

            char = self.source_code[self.position]    
            if char == '+' and self.token == '':
                self.next_token = Token('+', PLUS)
                self.position += 1
                return self.next_token
            elif char == '-' and self.token == '':
                self.next_token = Token('-', MINUS)
                self.position += 1
                return self.next_token
            elif char == '*' and self.token == '':
                self.next_token = Token('*', MULT)
                self.position += 1
                return self.next_token
            elif char == '/' and self.token == '':
                self.next_token = Token('/', DIV)
                self.position += 1
                return self.next_token
            elif char == '(' and self.token == '':
                self.next_token = Token('(', OPENKEY)
                self.position += 1
                return self.next_token    
            elif char == ')' and self.token == '':
                self.next_token = Token(')', CLOSEKEY)
                self.position += 1
                return self.next_token
            elif char == '=' and self.token == '':
                if(self.source_code[self.position+1] == '='):
                    self.next_token = Token('==', 'comparison')
                    self.position += 2
                    return self.next_token
                raise Exception("Invalid character")
            elif char == '\n' and self.token == '':
                self.next_token = Token('\n', 'newline')
                self.position += 1
                return self.next_token
            elif char == '.' and self.token == '':
                self.next_token = Token('.', 'dot')
                self.position += 1
                return self.next_token     
            elif char == '>' and self.token == '':
                self.next_token = Token('>', 'comparison')
                self.position += 1
                return self.next_token
            elif char == '<' and self.token == '':
                self.next_token = Token('<', 'comparison')
                self.position += 1
                return self.next_token
            elif char == '!' and self.token == '':
                self.next_token = Token('!', 'not')
                self.position += 1
                return self.next_token
            elif char == ':' and self.token == '':
                self.next_token = Token(':', 'colon')
                self.position += 1
                return self.next_token
            elif char == '|' and self.token == '':
                if(self.source_code[self.position+1] == '|'):
                    self.next_token = Token('||', 'or')
                    self.position += 2
                    return self.next_token
                raise Exception("Invalid character")
            elif char == '&' and self.token == '':
                if(self.source_code[self.position+1] == '&'):
                    self.next_token = Token('&&', 'and')
                    self.position += 2
                    return self.next_token            
                raise Exception("Invalid character")                                               
            elif char.isdigit() and self.token == '':
                while char.isdigit():
                    self.token  += char
                    self.position += 1
                    char = self.source_code[self.position]
                self.next_token = Token(int(self.token), int)
                return self.next_token
            elif char.isalpha() or char.isdigit() or char == '_' and self.token == '':
                while char.isalpha() or char.isdigit() or char == '_':
                    self.token  += char
                    self.position += 1
                    char = self.source_code[self.position]
                self.next_token = Token(self.token, 'identifier')
            elif char == ' ' and self.token == '':
                self.position += 1
            else:
                if self.token in reserved_words:
                    if self.token == 'INITIATING_COUNTDOWN_SEQUENCE':
                        self.next_token = Token(self.token, 'start_sequence')
                    elif self.token == 'WE_HAVE_LIFTOFF':
                        self.next_token = Token(self.token, 'end_sequence')
                    elif self.token == 'StageBlueprint':
                        self.next_token = Token(self.token, 'start_stage')
                    elif self.token == 'BuildStage':
                        self.next_token = Token(self.token, 'end_stage')
                    elif self.token == 'Program':
                        self.next_token = Token(self.token, 'start_program')
                    elif self.token == 'requires':
                        self.next_token = Token(self.token, 'requires')
                    elif self.token == 'EndProgram':
                        self.next_token = Token(self.token, 'end_program')
                    elif self.token == 'initiate':
                        self.next_token = Token(self.token, 'initiate')
                    elif self.token == 'beginBurn':
                        self.next_token = Token(self.token, 'begin_burn')
                    elif self.token == 'for':
                        self.next_token = Token(self.token, 'for')
                    elif self.token == 'Shutdown':
                        self.next_token = Token(self.token, 'end_burn')
                    elif self.token == 'flightStatusReport':
                        self.next_token = Token(self.token, 'if')
                    elif self.token == 'houstonWeReadYou':
                        self.next_token = Token(self.token, 'end_if')
                    elif self.token == 'is':
                        self.next_token = Token(self.token, 'assignment')
                    elif self.token == 'seconds':
                        self.next_token = Token(self.token, 'time')
                    elif self.token == 'minutes':
                        self.next_token = Token(self.token, 'time')
                    elif self.token == 'hours':
                        self.next_token = Token(self.token, 'time')
                    elif self.token == 'confirm':
                        self.next_token = Token(self.token, 'NOP')
                    elif self.token == 'print':
                        self.next_token = Token(self.token, 'print')
                return self.next_token

class Parser:
    tknzr = 0

    @staticmethod
    def parseBlock():
        node = Block('', [])
        Parser.tknzr.selectNext()
        if Parser.tknzr.next_token.type != 'start_sequence':
            raise Exception("Syntax error, program should start with INITIATING COUNTDOWN SEQUENCE")
        Parser.tknzr.selectNext()
        while Parser.tknzr.next_token.type != 'end_sequence':
            node.children.append(Parser.parseStatement())
            if Parser.tknzr.next_token.type == EOF:
                raise Exception("Syntax error, program should end with WE HAVE LIFTOFF")
        return node

    @staticmethod
    def parseStatement():
        if Parser.tknzr.next_token.type == 'identifier':
            identifier = Identifier(Parser.tknzr.next_token.value)
            id = Parser.tknzr.next_token.value
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type == 'dot':
                Parser.tknzr.selectNext()
                if Parser.tknzr.next_token.type == 'identifier':
                    identifier2 = Identifier(Parser.tknzr.next_token.value)
                    Parser.tknzr.selectNext()
                    if Parser.tknzr.next_token.type == 'assignment':
                        Parser.tknzr.selectNext()
                        node = StageAssignment(id, [identifier2, Parser.parseExpression()])
                        if Parser.tknzr.next_token.type != 'newline':
                            raise Exception("Syntax error")
                        Parser.tknzr.selectNext()
                        return node
                    else:
                        raise Exception("Syntax error")
            if Parser.tknzr.next_token.type == 'assignment':
                Parser.tknzr.selectNext()
                node = Assignment("", [identifier, Parser.parseExpression()])
                if Parser.tknzr.next_token.type != 'newline':
                    raise Exception("Syntax error")
                Parser.tknzr.selectNext()
                return node
            else:
                raise Exception("Syntax error")
            
        elif Parser.tknzr.next_token.type == 'start_stage':
            node = StageDec(Parser.tknzr.next_token.value, [])
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'identifier':
                raise Exception("Syntax error")
            identifier = Identifier(Parser.tknzr.next_token.value)
            node.children.append(identifier)
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'colon':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            while Parser.tknzr.next_token.type != 'end_stage':
                if Parser.tknzr.next_token.type == 'newline':
                    raise Exception("Syntax error")
                if Parser.tknzr.next_token.type == 'identifier':
                    identifier = Identifier(Parser.tknzr.next_token.value)
                    Parser.tknzr.selectNext()
                    if Parser.tknzr.next_token.type != 'assignment':
                        raise Exception("Syntax error")
                    Parser.tknzr.selectNext()
                    node.children.append(Assignment('', [identifier, Parser.parseExpression()]))
                if Parser.tknzr.next_token.type == 'newline':
                    Parser.tknzr.selectNext()
                else:
                    raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            return node
        
        elif Parser.tknzr.next_token.type == 'return':
            Parser.tknzr.selectNext()
            node = Return("return", [Parser.parseRelationalExpression()])
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            return node

        elif Parser.tknzr.next_token.type == 'start_program':
            node = FuncDec(Parser.tknzr.next_token.value, [])
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'identifier':
                raise Exception("Syntax error")
            identifier = Identifier(Parser.tknzr.next_token.value)
            node.children.append(identifier)
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'requires':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'identifier':
                raise Exception("Syntax error")
            identifier = Identifier(Parser.tknzr.next_token.value)
            node.children.append(StageDec(Parser.tknzr.next_token.value, []))
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            nodeBlock = Block('', [])
            while Parser.tknzr.next_token.type != 'end_program':
                nodeBlock.children.append(Parser.parseStatement())
            node.children.append(nodeBlock)
            if Parser.tknzr.next_token.type != 'end_program':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            return node
        
        elif Parser.tknzr.next_token.type == 'initiate':
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'identifier':
                raise Exception("Syntax error")
            node = FuncCall(Parser.tknzr.next_token.value, [])
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'identifier':
                raise Exception("Syntax error")
            identifier = Identifier(Parser.tknzr.next_token.value)
            node.children.append(identifier)
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            return node
        
        elif Parser.tknzr.next_token.type == 'begin_burn':
            node = Burn(Parser.tknzr.next_token.value, [])
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'for':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            node.children.append(Parser.parseExpression())
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            nodeBlock = Block('', [])
            while Parser.tknzr.next_token.type != 'end_burn':
                nodeBlock.children.append(Parser.parseStatement())
            node.children.append(nodeBlock)
            if Parser.tknzr.next_token.type != 'end_burn':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            return node
    
        elif Parser.tknzr.next_token.type == 'if':
            Parser.tknzr.selectNext()
            nodeRelExp = Parser.parseRelationalExpression()
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            nodeIf = Block('', [])
            while(Parser.tknzr.next_token.type != 'end_if'):
                nodeIf.children.append(Parser.parseStatement())
            if Parser.tknzr.next_token.type != 'end_if':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            node = If("", [nodeRelExp, nodeIf])
            return node
        
        elif Parser.tknzr.next_token.type == 'print':
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type == OPENKEY:
                Parser.tknzr.selectNext()
                node = Print("", [Parser.parseRelationalExpression()])
                if Parser.tknzr.next_token.type == CLOSEKEY:
                    Parser.tknzr.selectNext()
                    if Parser.tknzr.next_token.type != 'newline':
                        raise Exception("Syntax error")
                    Parser.tknzr.selectNext()
                    return node
                else:
                    raise Exception("Syntax error")
            else:
                raise Exception("Syntax error")
        
        elif Parser.tknzr.next_token.type == 'NOP':
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            return NoOp("", [])

        elif Parser.tknzr.next_token.type == 'newline':
            Parser.tknzr.selectNext()
            node = NoOp("", [])
            return node
        
        else:
            print(Parser.tknzr.next_token.value)
            raise Exception("Syntax error")

    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()
        while Parser.tknzr.next_token.type == PLUS or Parser.tknzr.next_token.type == MINUS or Parser.tknzr.next_token.type == 'or' or Parser.tknzr.next_token.type == 'concat':
            if Parser.tknzr.next_token.type == PLUS:
                op = Parser.tknzr.next_token.value
                Parser.tknzr.selectNext()
                node = BinOp(op,[node, Parser.parseTerm()])
            if Parser.tknzr.next_token.type == MINUS:
                op = Parser.tknzr.next_token.value
                Parser.tknzr.selectNext()
                node = BinOp(op,[node, Parser.parseTerm()])
            if Parser.tknzr.next_token.type == 'or':
                op = Parser.tknzr.next_token.value
                Parser.tknzr.selectNext()
                node = BinOp(op,[node, Parser.parseTerm()])
        return node
    
    @staticmethod
    def parseRelationalExpression():
        node = Parser.parseExpression()
        while Parser.tknzr.next_token.type == 'comparison':
            if Parser.tknzr.next_token.value == '<':
                op = Parser.tknzr.next_token.value
                Parser.tknzr.selectNext()
                node = BinOp(op,[node, Parser.parseExpression()])
            if Parser.tknzr.next_token.value == '>':
                op = Parser.tknzr.next_token.value
                Parser.tknzr.selectNext()
                node = BinOp(op,[node, Parser.parseExpression()])
            if Parser.tknzr.next_token.value == '==':
                op = Parser.tknzr.next_token.value
                Parser.tknzr.selectNext()
                node = BinOp(op,[node, Parser.parseExpression()])
        return node

    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()
        while Parser.tknzr.next_token.type == MULT or Parser.tknzr.next_token.type == DIV or Parser.tknzr.next_token.type == 'and':
            if Parser.tknzr.next_token.type == MULT:
                op = Parser.tknzr.next_token.value
                Parser.tknzr.selectNext()
                node = BinOp(op,[node, Parser.parseFactor()])
            if Parser.tknzr.next_token.type == DIV:
                op = Parser.tknzr.next_token.value
                Parser.tknzr.selectNext()
                node = BinOp(op,[node, Parser.parseFactor()])
            if Parser.tknzr.next_token.type == 'and':
                op = Parser.tknzr.next_token.value
                Parser.tknzr.selectNext()
                node = BinOp(op,[node, Parser.parseFactor()])
        return node
    
    @staticmethod
    def parseFactor():
        #Parser.tknzr.selectNext()
        if Parser.tknzr.next_token.type == int:
            node = IntVal(Parser.tknzr.next_token.value)
            Parser.tknzr.selectNext()
            return node
        
        elif Parser.tknzr.next_token.type == 'identifier':
            node = Identifier(Parser.tknzr.next_token.value)
            iden = Parser.tknzr.next_token.value
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type == 'dot':
                Parser.tknzr.selectNext()
                if Parser.tknzr.next_token.type == 'identifier':
                    node = StageIdentifier(iden, [node, Identifier(Parser.tknzr.next_token.value)])
                    Parser.tknzr.selectNext()
                    return node
                else:
                    raise Exception("Syntax error")    
            return node
        
        elif Parser.tknzr.next_token.type == 'initiate':
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'identifier':
                raise Exception("Syntax error")
            node = FuncCall(Parser.tknzr.next_token.value, [])
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'identifier':
                raise Exception("Syntax error")
            identifier = Identifier(Parser.tknzr.next_token.value)
            node.children.append(identifier)
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != 'newline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            return node
        
        elif Parser.tknzr.next_token.type == PLUS or Parser.tknzr.next_token.type == MINUS or Parser.tknzr.next_token.type == 'not':
            op = Parser.tknzr.next_token.value
            Parser.tknzr.selectNext()
            node = UnOp(op, [Parser.parseFactor()])   
            return node
        
        elif Parser.tknzr.next_token.type == OPENKEY:
            Parser.tknzr.selectNext()
            node = Parser.parseRelationalExpression()
            if Parser.tknzr.next_token.type == CLOSEKEY:
                Parser.tknzr.selectNext()
                return node
            else:
                raise Exception
            
        elif Parser.tknzr.next_token.type == 'reserved':
            if Parser.tknzr.next_token.value != 'readline':
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != OPENKEY:
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            if Parser.tknzr.next_token.type != CLOSEKEY:
                raise Exception("Syntax error")
            Parser.tknzr.selectNext()
            node = Readln()
            return node
        else:
            print(Parser.tknzr.next_token.value)
            raise Exception

    @staticmethod
    def run(code):
        pre_pro = PrePro()
        PrePro.source_code = code
        code = pre_pro.filter()
        Parser.tknzr = Tokenizer(code)
        root_node = Parser.parseBlock()
        if Parser.tknzr.next_token.type == 'end_sequence':
            general_symbol_table = Symbol_table()
            root_node.evaluate(general_symbol_table)
        else:
            raise Exception
        return None    

def main():
    #operation = open('test.apl').read()
    operation = open(sys.argv[1]).read()
    engine = Parser()
    engine.run(operation)


if __name__ == "__main__":
    main()