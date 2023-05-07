from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Code block
        self.lexer.add('START_SEQUENCE', r'INITIATING COUNTDOWN SEQUENCE')
        self.lexer.add('END_SEQUENCE', r'WE HAVE LIFTOFF')

        # Stage bleuprint
        self.lexer.add('STAGE', r'StageBlueprint')
        self.lexer.add('END_STAGE', r'BuildStage')
        # stage attributes
        self.lexer.add('STAGE_ATTRIBUTES', r'specificImpulse')
        self.lexer.add('STAGE_ATTRIBUTES', r'wetMass')
        self.lexer.add('STAGE_ATTRIBUTES', r'dryMass')
        self.lexer.add('STAGE_ATTRIBUTES', r'engines')
        self.lexer.add('STAGE_ATTRIBUTES', r'deltaV')

        # Program
        self.lexer.add('PROGRAM', r'Program')
        self.lexer.add('REQUIRES', r'requires')
        self.lexer.add('END_PROGRAM', r'EndProgram')

        # program call
        self.lexer.add('INITATE', r'initiate')

        # Burn loop
        self.lexer.add('BURN_START', r'beginBurn')
        self.lexer.add('FOR', r'for')
        self.lexer.add('BURN_END', r'Shutdown')

        # Conditional Statement
        self.lexer.add('STATUS_REPORT', r'flightStatusReport')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('END_REPORT', r'houstonWeReadYou')

        # BinOperators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')

        # Comparison
        self.lexer.add('GREATER_THAN', r'\>')
        self.lexer.add('LESS_THAN', r'\<')
        self.lexer.add('EQUAL_TO', r'\=\=')
        self.lexer.add('NOT_EQUAL_TO', r'\!\=')
        self.lexer.add('GREATER_THAN_OR_EQUAL_TO', r'\>\=')
        self.lexer.add('LESS_THAN_OR_EQUAL_TO', r'\<\=')

        # Unary Operators
        self.lexer.add('NOT', r'\!')

        # Time attribute
        self.lexer.add('TIME', r'seconds')
        self.lexer.add('TIME', r'minutes')
        self.lexer.add('TIME', r'hours')

        # Equal
        self.lexer.add('EQUAL', r'is')

        # Confirm
        self.lexer.add('CONFIRM', r'confirm')

        # Colon
        self.lexer.add('COLON', r'\:')

        # period
        self.lexer.add('PERIOD', r'\.')

        # newLine
        self.lexer.add('NEW_LINE', r'\n')

        # Number
        self.lexer.add('NUMBER', r'\d+')

        # Identifier name
        self.lexer.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')

        # Ignore spaces
        self.lexer.ignore(r'[ \t]+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()