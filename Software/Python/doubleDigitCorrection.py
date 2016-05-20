"""
defineScenarioConfigFileName.py

The following function uses the user input from the terminal to define the name of the scenario configuration file to be loaded by the consys.py script

Fluvio L. Lobo Fenoglietto 05/20/2016
"""

def doubleDigitCorrection(scenarioNumber):
    num = int(scenarioNumber)
    # print num
    if num < 10:
        scenarioNumberString = "00" + str(num)
        # print scenarioNumberString
    if num >= 10 and num < 100:
        scenarioNumberString = "0" + str(num)
        # print scenarioNumberString
    if num >= 100:
        scenarioNumberString = str(num)
        # print scenarioNumberString
    return scenarioNumberString
        

        
