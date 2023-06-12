# APS Lógica da Computação

## Authored by:
Bernardo Cunha Capoferri

## Rubric achieved: B

## Objective:
This repository contains a computing language devoloped from the ground up, It is not a general use language like Python or C++, but tailored for a specific purpose. It contains basic structure like loops and conditionals, allows for the declaration of variables and functions and allows the user to call the latter.

## Idea
The language that will be developed has the intent to allow the user to build the stages of a rocketship (variables), define program plans to apply to the stages (functions), determine for how long each stage will burn it's engines (loops) and verify specific attributes to determine if the burn should be aborted, or even continue at all (conditionals). After the code is ready, it can be compiled, and the user will receive the delta V used up in the program and how far he could've reached with that much energy.

## EBNF of the language:
```
LETTER = ("A" | "B" | "C" | "D" | "E" | "F" | "G"
       | "H" | "I" | "J" | "K" | "L" | "M" | "N"
       | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
       | "V" | "W" | "X" | "Y" | "Z" | "a" | "b"
       | "c" | "d" | "e" | "f" | "g" | "h" | "i"
       | "j" | "k" | "l" | "m" | "n" | "o" | "p"
       | "q" | "r" | "s" | "t" | "u" | "v" | "w"
       | "x" | "y" | "z") ;

DIGIT = ("0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9") ;

INTEGER = DIGIT, {DIGIT};

IDENTIFIER = (LETTER | "_"), {LETTER | "_" | INTEGER};

STAGE_DECLARATION = "StageBlueprint", IDENTIFIER, ":", {(IDENTIFIER, "is", INTEGER | IDENTIFIER), "\n"},"BuildStage";

REFERENCE_STAGE_ATTRIBUTE = IDENTIFIER, ".", STAGE_ATRIBUTES;

VARIABLE_DECLARATION = IDENTIFIER | REFERENCE_STAGE_ATTRIBUTE, "is", EXPRESSION;


EXPRESSION = INTEGER | IDENTIFIER | REFERENCE_STAGE_ATTRIBUTE, {("+" | "-" | "*" | "/"), INTEGER | IDENTIFIER | REFERENCE_STAGE_ATTRIBUTE};

CONDITIONAL_OPERATION = ">" | "<" | "==" | ">=" | "<=" | "!=" | "&&" | "||";

CONDITIONAL_DECLARATION = "flightStatusReport", EXPRESSION, CONDITIONAL_OPERATION, EXPRESSION, "\n", "confirm" | {(VARIABLE_DECLARATION, "\n")}, "houstonWeReadYou";

LOOP_DECLARATION = "beginBurn for", EXPRESSION, "\n", {VARIABLE_DECLARATION | STAGE_DECLARATION | FUNCTION_DECLARATION | CALL_FUNCTION}, "\n", "engineShutOff";

FUNCTION_DECLARATION = "Program", IDENTIFIER, "requires", IDENTIFIER, "\n", {(LOOP_DECLARATION | CONDITIONAL_DECLARATION | VARIABLE_DECLARATION | "PRINT" | "RETURN" | "confirm", "\n")}, "EndProgram";

CALL_FUNCTION = "initiate", IDENTIFIER, [{IDENTIFIER}];

PRINT = "print", "(", EXPRESSION,")", "\n"

RETURN = "return", EXPRESSION, "\n"

STRUCTURE = "INITIATING COUNTDOWN SEQUENCE", {VARIABLE_DECLARATION | STAGE_DECLARATION | FUNCTION_DECLARATION | CALL_FUNCTION | PRINT}, "WE HAVE LIFTOFF";
```

## Implementation
To create the compiler for the language above, a Julia compiler made using python was repurposed to identify and interpret it. The code for it can be found in the file `compiler.py` and it was tested to run the following code to verify it's basic functionality.

## Example Code:
```
INITIATING_COUNTDOWN_SEQUENCE

engine_specific_impulse is 150

StageBlueprint  command_module:
    specificImpulse is engine_specific_impulse
    wetMass is 1000
    dryMass is 500
    engines is 1
BuildStage

Program launch requires stage
    beginBurn for 80
        flightStatusReport stage.wetMass > stage.dryMass
            stage.wetMass is stage.wetMass - 5
        houstonWeReadYou
    Shutdown
    print(stage.wetMass)
EndProgram

initiate launch command_module

WE_HAVE_LIFTOFF
```

Expected result for the code above is for it to print 600.

To test it, create a file with the extension ".apl" and run the following command:

``` bash
python3 compiler.py <fileNameHere>.jl
```
