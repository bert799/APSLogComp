from rply import ParserGenerator


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['START_SEQUENCE', 'END_SEQUENCE', 'STAGE', 'END_STAGE', 'STAGE_ATTRIBUTES',
             'PROGRAM', 'REQUIRES', 'END_PROGRAM', 'INITATE', 'BURN_START', 'FOR', 'BURN_END',
             'STATUS_REPORT', 'ELSE', 'END_REPORT', 'SUM', 'SUB', 'MUL', 'DIV', 'GREATER_THAN',
             'LESS_THAN', 'EQUAL_TO', 'NOT_EQUAL_TO', 'LESS_THAN_OR_EQUAL_TO', 'GREATER_THAN_OR_EQUAL_TO', 'NOT', 'TIME', 'EQUAL', 'CONFIRM', 'COLON', 'PERIOD',
             'NEW_LINE', 'NUMBER', 'IDENTIFIER']
        )

    def parse(self):
        # BLOCK
        @self.pg.production('program : NEW_LINE program')
        @self.pg.production('program : NEW_LINE')
        @self.pg.production('program : START_SEQUENCE NEW_LINE block')
        @self.pg.production('program : START_SEQUENCE NEW_LINE block NEW_LINE')
        def program(p):
            return p[1]
        @self.pg.production('block : END_SEQUENCE')
        def block_end(p):
            return p[0]
        @self.pg.production('block : build block')
        def block_statement(p):
            return p[0]
        
        # BUILD
        @self.pg.production('build : NEW_LINE')
        def build_newline(p):
            return p[0]
        @self.pg.production('build : IDENTIFIER EQUAL NUMBER NEW_LINE')
        def build_iden(p):
            return p[2]
        @self.pg.production('build : STAGE IDENTIFIER COLON NEW_LINE stage NEW_LINE')
        def build_stage(p):
            return p[4]
        @self.pg.production('build : PROGRAM IDENTIFIER REQUIRES IDENTIFIER NEW_LINE statement END_PROGRAM NEW_LINE')
        def build_program(p):
            return p[5]
        @self.pg.production('build : INITATE IDENTIFIER expression NEW_LINE')
        @self.pg.production('build : INITATE IDENTIFIER NEW_LINE')
        def build_initiate(p):
            if len(p) == 3:
                return p[1]
            return p[2]
        
        # STAGE
        @self.pg.production('stage : stage_attribute NEW_LINE stage')
        @self.pg.production('stage : END_STAGE')
        def stage_statement(p):
            return p[0]
        
        # STAGE ATTRIBUTE
        @self.pg.production('stage_attribute : STAGE_ATTRIBUTES EQUAL expression')
        def stage_attribute(p):
            return p[2]
        
        # STATEMENT
        @self.pg.production('statement : BURN_START FOR NUMBER TIME IDENTIFIER NEW_LINE statement BURN_END NEW_LINE')
        def statement_burn(p):
            return p[6]
        @self.pg.production('statement : STATUS_REPORT relational_expression NEW_LINE statement END_REPORT NEW_LINE')
        def statement_report(p):
            return p[4]
        @self.pg.production('statement : STATUS_REPORT relational_expression NEW_LINE statement ELSE NEW_LINE statement END_REPORT NEW_LINE')
        def statement_report_else(p):
            return p[4]
        @self.pg.production('statement : CONFIRM NEW_LINE')
        def statement_confirm(p):
            return p[0]
        
        # RELATIONAL EXPRESSION
        @self.pg.production('relational_expression : expression')
        def relational_expression_expression(p):
            return p[0]
        @self.pg.production('relational_expression : expression GREATER_THAN expression')
        @self.pg.production('relational_expression : expression LESS_THAN expression')
        @self.pg.production('relational_expression : expression EQUAL_TO expression')
        @self.pg.production('relational_expression : expression NOT_EQUAL_TO expression')
        @self.pg.production('relational_expression : expression GREATER_THAN_OR_EQUAL_TO expression')
        @self.pg.production('relational_expression : expression LESS_THAN_OR_EQUAL_TO expression')
        def relational_expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'GREATER_THAN':
                return operator
            elif operator.gettokentype() == 'LESS_THAN':
                return operator
            elif operator.gettokentype() == 'EQUAL_TO':
                return operator
            elif operator.gettokentype() == 'NOT_EQUAL_TO':
                return operator
            elif operator.gettokentype() == 'GREATER_THAN_OR_EQUAL_TO':
                return operator
            elif operator.gettokentype() == 'LESS_THAN_OR_EQUAL_TO':
                return operator
        
        # EXPRESSION
        @self.pg.production('expression : term')
        def expression_term(p):
            return p[0]
        @self.pg.production('expression : term SUM term')
        @self.pg.production('expression : term SUB term')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'SUM':
                return operator
            elif operator.gettokentype() == 'SUB':
                return operator
            
        # TERM
        @self.pg.production('term : factor')
        def term_factor(p):
            return p[0]
        @self.pg.production('term : factor MUL factor')
        @self.pg.production('term : factor DIV factor')
        def term(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'MUL':
                return operator
            elif operator.gettokentype() == 'DIV':
                return operator
        
        # FACTOR
        @self.pg.production('factor : NUMBER')
        def factor_number(p):
            return p[0].value
        
        @self.pg.production('factor : IDENTIFIER')
        def factor_identifier(p):
            return p[0].value
        
        @self.pg.production('factor : NOT factor')
        def factor_not(p):
            return p[0]
        
        @self.pg.production('factor : CONFIRM')
        def factor_confirm(p):
            return p[0]
        
        @self.pg.production('factor : IDENTIFIER PERIOD STAGE_ATTRIBUTES')
        def factor_stage_attribute(p):
            return p[2]
        

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()