/* =====================================
 * Clear Window
 *
 * The following function clear the main
 * window of the gui by setting the
 * visibility of all the objects to
 * "false"
 *
 * Fluvio L. Lobo Fenoglietto 02/15/2016
 ==================================== */

public void clearWindow(int Nscenarios) {
  
  // Hide all the current objects
  // cp5.get(Button.class,"exitApplication").setVisible(false); // Exit Button
  cp5.get(Textlabel.class,"studentIDLabel").setVisible(false); // Student ID Label/Title
  
  cp5.get(Textfield.class,"userID").setVisible(false); // User ID input
  
  cp5.get(Textlabel.class,"currentInput").setVisible(false); // Current user input 
  
  for (int i = 0; i < Nscenarios; i ++) {
    int counter = i+1;
    String buttonNamePrefix = "sc";
    String buttonName = singleDigitCorrection(buttonNamePrefix, counter);
    cp5.get(Button.class,buttonName).setVisible(false); // Scenario buttons
  } // End of for-loop "Scenario Buttons"
  
  scenario3ImageSwitch = 0;
  scenario4VideoSwitch = 0;
  try {
    ophvid.stop();
  } catch (NullPointerException e) {
  }
  
  cp5.get(Textarea.class,"scenarioDetails").setVisible(false); // Scenario details
  
  cp5.get(Button.class,"confirmSelection").setVisible(false); // Selection confirmation button
  
  cp5.get(Textlabel.class,"confirmCurrentInput").setVisible(false); // Current user input label


  
}