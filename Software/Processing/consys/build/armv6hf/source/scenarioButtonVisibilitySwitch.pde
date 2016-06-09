/* =====================================
 * Scenario Button Visibility
 *
 * This function changes the visibility of the scenario buttons to "true".
 *
 * Fluvio L. Lobo Fenoglietto 01/28/2016
 ==================================== */ 
 
public void scenarioButtonVisibilitySwitch(int Nscenarios) {
   
  // Set scenario buttons visible for the user
  for (int i = 1; i <= Nscenarios; i++) {
    
    String prefix = "sc";
    String controllerName = singleDigitCorrection(prefix, i);
    // println(controllerName);
    cp5.get(Button.class,controllerName).setVisible(true);
    
  } // End of for-loop --Loop around scenario buttons
   
} // End of function scenarioButtonVisibilitySwitch