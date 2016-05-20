"""
defineScenarioConfigFileName.py

The following function uses the user input from the terminal to define the name of the scenario configuration file to be loaded by the consys.py script

Fluvio L. Lobo Fenoglietto 05/20/2016
"""

def defineScenarioConfigFileName(scenarioNumber):
    num = int(scenarioNumber)
    if num < 10:
        scenarioNumber = "0" + str(num)
        print scenarioNumber

        
