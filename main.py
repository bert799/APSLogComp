from lexer import Lexer
from my_parser import Parser

text_input = """
INITIATING COUNTDOWN SEQUENCE

engine_specific_impulse is 150

StageBlueprint  command_module:
    specificImpulse is engine_specific_impulse
    wetMass is 1000
    dryMass is 500
    engines is 1
BuildStage

Program launch requires stage
    beginBurn for 120 seconds stage
        flightStatusReport stage.wetMass > stage.dryMass
            confirm
        houstonWeReadYou
    Shutdown
EndProgram

initiate launch command_module

WE HAVE LIFTOFF
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)

pg = Parser()
pg.parse()
parser = pg.get_parser()

def token_generator(token_list):
    for token in token_list:
        print(token)
        yield token



try:
    result = parser.parse(tokens)
    print("Parsing successful!")
except Exception as e:
    print("Parsing failed:")
    print("Exception:", e)