INITIATING_COUNTDOWN_SEQUENCE

engine_specific_impulse is 150

StageBlueprint  command_module:
    specificImpulse is engine_specific_impulse
    wetMass is 1000
    dryMass is 500
    engines is 1
BuildStage

Program launch requires stage
    beginBurn for 120
        flightStatusReport stage.wetMass > stage.dryMass
            stage.wetMass is stage.wetMass - 5
        houstonWeReadYou
    Shutdown
    print(stage.wetMass)
EndProgram

initiate launch command_module

WE_HAVE_LIFTOFF
