import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import processing.serial.*; 
import cc.arduino.*; 
import controlP5.*; 
import processing.video.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class consys extends PApplet {

/*
 * Control System Front End
 *
 * This script represents the Front End of the Raspberry Pi-powered Control System.
 * The Front End is the only user interface in the entire process.
 * The standard patient will be the only user to interface with this Front End.
 *
 * Fluvio L. Lobo Fenoglietto
 * 01/26/2015
 *
 */

/* ========================================
 * GLOBAL VARIABLES AND LIBRARIES
 ======================================= */
 
// Import Libraries





// Execution State Variables
String executionState = "config"; // Configuration state set as default

/* ----------------------------------------
 * VARIABLES FOR CONFIGURATION STATE
 --------------------------------------- */
 
// Config Index
int configIndex = 0;

// Paths for input/output files
String timeStampFolder = timeStamp("dated-folder");
String logFile = "ExecutionLog.txt";
String exeLogFilePath = "data/output/" + timeStampFolder + "/" + logFile;

// Controllers
ControlP5 cp5;

// Media
PImage hphlogo;
PImage otoim;
int scenario3ImageSwitch = 0;
Movie ophvid;
int scenario4VideoSwitch = 0;

// GUI Layout Variables
// > GUI Dimensions
int lenX = width; // pixels
int lenY = height; // pixels
int midX = lenX/2; // pixels
int midY = lenY/2; // pixels
// > Margins
int topMargin = 25; // pixels
int rightMargin = 25; // pixels
int bottomMargin = 25; // pixels
int leftMargin = 25; // pixels
// > Colors
int black = color(0,0,0);
int gray = color(214,214,214);
int verydarkgray = color(5,5,5);
int gold = color(255,204,0);
int white = color(255,255,255);
int red = color(232,97,82);
int green = color(56,222,43);

// Number of scenarios
int Nscenarios = 12;

// Output Variables
String[] configInfo = new String[3];

/* ----------------------------------------
 * VARIABLES FOR RECORD STATE
 --------------------------------------- */

// Serial Port/Com variables
Serial comPort;

// Arduino variables
int Nardus = 1;
Arduino[] arduino = new Arduino[Nardus];
// arduPorts :: This variable will be used in case that desired rfcomm ports begin switching in the serial array

int Nports = 6;
String deviceName = "arduOTO";

// Data Acquisition/Record Index
int dataIndex = 0;

// Data File Path 
// Currently the same as userInfoFolder

// Data File Writer
PrintWriter[] dataFile = new PrintWriter[Nardus];

/* ========================================
 * VOID SETUP LOOP
 ======================================= */ 
public void setup() {
  
  executionState = "config";
  
  // Execution Log File
  exeLogFile(exeLogFilePath);
  
  // GUI size
  
  //size(800,480); // These are the dimensions of the RasPi screen
  background(black);
  cp5 = new ControlP5(this);
  
  // GUI Formatting :: Fonts
  PFont pfont_1 = createFont("Arial Rounded MT Bold",20,true);
  ControlFont titlefont = new ControlFont(pfont_1,24); // label font and size
  ControlFont labelfont = new ControlFont(pfont_1, 12); // label font and size
  ControlFont buttonfont = new ControlFont(pfont_1,12); // button font and size  
  
  PFont pfont_2 = createFont("Consolas",20,true);
  ControlFont textfont = new ControlFont(pfont_2,14); // button font and size
  
  // GUI Elements :: Images :: Logos
  hphlogo = loadImage("media/hphlogo720res.png");

  /* ----------------------------------------
   * GENERAL CONTROLS
   *
   * This section has been dedicated to the
   * creating of general purpose controls for
   * the gui. For instance, and {EXIT} button
   * to scape from the application
   *
   --------------------------------------- */
   
  // GUI Control :: Button :: Exit Application  
  int exitButtonWidth = 75;
  int exitButtonHeight = 25;
  int exitButtonXPos = width - exitButtonWidth - 10;
  int exitButtonYPos = 10;
  cp5.addButton("exitApplication")
     .setBroadcast(false) // Avoids the immediate execution of the button
     .setValue(0)
     .setPosition(exitButtonXPos,exitButtonYPos)
     .setSize(exitButtonWidth,exitButtonHeight)
     .setLabel("EXIT")
     .setColorCaptionLabel(black)
     .setColorBackground(red)
     .setColorForeground(gray)
     .setBroadcast(true)
     ;
     
  cp5.getController("exitApplication")
     .getCaptionLabel()
     .setFont(buttonfont)
     .toUpperCase(false)
     .setVisible(true)
     ;
     
     
  /* ----------------------------------------
   * RESTART
   *
   * This section creates a button for the
   * user to {RESTART} the consys application
   *
   * Fluvio L Lobo Fenoglietto 02/19/2016
   *
   --------------------------------------- */
   
  // GUI Control :: Button :: Confirm Selection  
  int restartButtonWidth = exitButtonWidth;
  int restartButtonHeight = exitButtonHeight;
  int restartButtonXPos = exitButtonXPos - exitButtonWidth - 10;
  int restartButtonYPos = exitButtonYPos;
  cp5.addButton("restartApplication")
     .setBroadcast(false)
     .setPosition(restartButtonXPos,restartButtonYPos)
     .setSize(restartButtonWidth,restartButtonHeight)
     .setLabel("RESTART")
     .setColorCaptionLabel(black)
     .setColorBackground(gold)
     .setColorForeground(green)
     .setBroadcast(true)
     ;
     
  cp5.getController("restartApplication")
     .getCaptionLabel()
     .setFont(buttonfont)
     .toUpperCase(false)
     ;
  
  /* ----------------------------------------
   * STANDARDIZE PATIENT ID
   *
   * This section creates the text field, and
   * associated labels, for the SP to input
   * his/her information
   *
   --------------------------------------- */
  
  // GUI Element :: Label :: Student ID Label
  int titleLabelWidth = 250;
  int titleLabelHeight = 50;
  int titleLabelXPos = leftMargin;
  int titleLabelYPos = topMargin;
  cp5.addTextlabel("studentIDLabel") // title object
     .setBroadcast(false)
     .setSize(titleLabelWidth,titleLabelHeight)
     .setPosition(titleLabelXPos - 5, titleLabelYPos) // set position of the title label
     .setText("Standardize Patient ID") // title text
     .setFont(titlefont) // set title font :: using lable font and size
     .setColor(gold)
     .setBroadcast(true)
     .setVisible(true)
     ;
     
  // GUI Control :: Text Field
  int txtFieldWidth = 300;
  int txtFieldHeight = 25;
  int txtFieldXPos = leftMargin;
  int txtFieldYPos = titleLabelYPos + titleLabelHeight - 10;
  cp5.addTextfield("userID") // No text to be displayed below the field
     .setBroadcast(false)
     .setPosition(txtFieldXPos,txtFieldYPos)
     .setSize(txtFieldWidth,txtFieldHeight)
     .setFont(textfont)
     .setColor(white)
     .setColorBackground(black)
     .setColorForeground(gray)
     .setBroadcast(true)
     .setVisible(true)
     ;
     
  cp5.getController("userID").getCaptionLabel().setVisible(false);
     
  // GUI Element :: Label :: Current Input
  int currentLabelWidth = 200;
  int currentLabelHeight = 25;
  int currentLabelYPos = txtFieldYPos + txtFieldHeight + 10;
  cp5.addTextlabel("currentInput") // title object
     .setBroadcast(false)
     .setSize(currentLabelWidth,currentLabelHeight)
     .setPosition(leftMargin - 5,currentLabelYPos) // set position of the title label
     .setText("Enter SP ID and press Enter/Return") // title text
     .setFont(textfont) // set title font :: using lable font and size
     .setColor(white)
     .setBroadcast(true)
     .setVisible(true)
     ; 
     
  /* ----------------------------------------
   * SCENARIO SELECTION
   *
   * This section creates the scenario buttons.
   * Each button refers to a scenario file.
   *
   --------------------------------------- */
  
  // Variables
  // int Nscenarios = 12; -- This function was made global
  int scenarioButtonWidth = 125;
  int scenarioButtonHeight = 15;
  int scenarioButtonXPos = leftMargin;
  int scenarioButtonYPos0 = currentLabelYPos + currentLabelHeight + 5;
  int[] scenarioButtonYPos = new int[Nscenarios+1];
  int buttonSpacing = 5;
  
  // Creator Loop
  for (int i = 0; i < Nscenarios; i++) {
    
    int counter = i+1;
    String buttonNamePrefix = "sc";
    String buttonLabelTextPrefix = "Scenario #";
    String buttonName = singleDigitCorrection(buttonNamePrefix, counter);
    String buttonLabelText = singleDigitCorrection(buttonLabelTextPrefix, counter);
    
    if (i == 0) {
      
      scenarioButtonYPos[i] = scenarioButtonYPos0;  

    } else if (i > 0) {
      
      scenarioButtonYPos[i] = scenarioButtonYPos[i-1] + scenarioButtonHeight + buttonSpacing;
        
    } // End of if-statement
    
    // GUI Controller :: Button :: Scenario #i
    cp5.addButton(buttonName)
        .setBroadcast(false) // Avoids the immediate execution of the button
        .setVisible(false)
        .setValue(0)
        .setPosition(scenarioButtonXPos,scenarioButtonYPos[i])
        .setSize(scenarioButtonWidth,scenarioButtonHeight)
        .setLabel(buttonLabelText)
        .setColorCaptionLabel(black)
        .setColorBackground(gold)
        .setColorForeground(gray)
        .setBroadcast(true)
        ;
         
     cp5.getController(buttonName)
        .getCaptionLabel()
        .setFont(buttonfont)
        .toUpperCase(false)
        ;
       
  } // End of for-loop --Scenario button creation
  
  /* ----------------------------------------
   * SCENARIO DETAILS
   *
   * This section creates a text area containing the details of the selected scenario.
   *
   --------------------------------------- */
  
  int txtareaXPos = leftMargin + scenarioButtonWidth + 50;
  int txtareaYPos = scenarioButtonYPos0;
  int txtareaXlen = width - txtareaXPos - 50;
  int txtareaYlen = height - txtareaYPos - 125;
  
  cp5.addTextarea("scenarioDetails")
     .setVisible(false)
     .setPosition(txtareaXPos,txtareaYPos)
     .setSize(txtareaXlen,txtareaYlen)
     .setFont(textfont)
     .setLineHeight(14)
     .setColor(white)
     .setColorBackground(black)
     .setColorForeground(white)
     ;
     
  /* ----------------------------------------
   * CONFIRMATION 
   *
   * This section creates a text label which summarizes the standardize patient information and his/her scenario selection.
   * If the user is not sure of the information, he/she can change selections at will.
   * The user will see the information changes displayed on the status label.
   *
   * Fluvio L Lobo Fenoglietto 02/01/2016
   *
   --------------------------------------- */
   
  // GUI Control :: Button :: Confirm Selection  
  int confirmSelectionButtonWidth = scenarioButtonWidth;
  int confirmSelectionButtonHeight = 20;
  int confirmSelectionButtonXPos = leftMargin;
  int confirmSelectionButtonYPos = scenarioButtonYPos[Nscenarios-1] + scenarioButtonHeight + 50;
  cp5.addButton("confirmSelection")
     .setBroadcast(false)
     .setPosition(confirmSelectionButtonXPos,confirmSelectionButtonYPos)
     .setSize(confirmSelectionButtonWidth,confirmSelectionButtonHeight)
     .setLabel("Confirm Selection")
     .setColorCaptionLabel(black)
     .setColorBackground(gold)
     .setColorForeground(gray)
     .setBroadcast(true)
     .setVisible(false)
     ;
     
  cp5.getController("confirmSelection")
     .getCaptionLabel()
     .setFont(buttonfont)
     .toUpperCase(false)
     ;

  // GUI Element :: Label :: Current Input --Confirmation
  int confirmationLabelWidth = 200;
  int confirmationLabelHeight = 25;
  //int confirmationLabelXPos = leftMargin + confirmSelectionButtonWidth + 25;
  int confirmationLabelXPos = txtareaXPos;
  int confirmationLabelYPos = confirmSelectionButtonYPos;
  // int indent4ConfirmationLabel = 5;
  cp5.addTextlabel("confirmCurrentInput") // title object
     .setBroadcast(false)
     .setSize(confirmationLabelWidth, confirmationLabelHeight)
     .setPosition(confirmationLabelXPos, confirmationLabelYPos)
     .setFont(textfont) // set title font :: using lable font and size
     .setColor(white)
     .setBroadcast(true)
     .setVisible(false)
     ;
     
  
     
} // End of void-setup loop

/* ========================================
 * VOID DRAW LOOP
 ======================================= */ 

public void draw() {
  
  // Set the background of the window
  background(black);
  
  // Execution State Switch
  switch (executionState) {
    
   case "config":
   
     // Re-define indeces for Restart
     dataIndex = 0;
    
     // Set the backgrounf of the window
     background(black);
  
     // Place Images
     image(hphlogo,width-110,height-60);
      
     /* -----------------------------
      * Scenario Media
      ---------------------------- */
      
     if (scenario3ImageSwitch == 1) {
       
       int media1XPos = leftMargin + 175;
       int media1YPos = 125;
       int media1Xlen = 500;
       int media1Ylen = 250;
       image(otoim,media1XPos,media1YPos,media1Xlen,media1Ylen);
        
     } else if (scenario4VideoSwitch == 1) {
        
       int media1XPos = leftMargin + 175;
       int media1YPos = 125;
       int media1Xlen = 500;
       int media1Ylen = 250;
       image(ophvid,media1XPos,media1YPos,media1Xlen,media1Ylen);
       ophvid.play();

     }
      
     if (configIndex == 0) {
       println("Program STATE :: Configuration");
       configIndex = 1;
     } // End of if-statement
      
     break;
      
   case "record":
    
     // Set the backgrounf of the window
     background(black);
      
     // Place Images
     image(hphlogo,width-110,height-60);
      
     waitClock();
      
     if (dataIndex == 0) {
        
       println("Program STATE :: Record");
        
       connect2Arduinos(Nardus);
       
       readAnalogData(dataIndex, Nardus, Nports);
        
       // Updating Indeces
       dataIndex = dataIndex + 1;
        
     } else {
        
       readAnalogData(dataIndex, Nardus, Nports);
       
       // Updating Indeces 
       dataIndex = dataIndex + 1;
      
     } // End of if-statement

     break;
      
  } // End of switch
  
  
} // End of void-draw loop

/* ========================================
 * CONTROL EVENTS
 ======================================= */ 

public void controlEvent(ControlEvent theEvent) {
  
  // In the case the active control is a TextField
  if(theEvent.isAssignableFrom(Textfield.class)) {
    
    // Textfield :: Variables
    String eventName = theEvent.getName();
    String textFieldInput = theEvent.getStringValue();
    
    // The following conditional statement was designed to check the viability of the user input
    String trimTextFieldInput = trim(textFieldInput);
    int stringLength = trimTextFieldInput.length();
    
    if (stringLength == 0) {
      
      // If the trimmed string has 0 length, the original string was composed of spaces (no characters).
      // In this case, the program assumes the user did not provide a viable input and send a message to the user through the current input label
      cp5.get(Textlabel.class,"currentInput").setText("Not a viable input! Enter SP ID and press Enter/Return"); 
      
    } else if (stringLength > 0) {
      
      // Textfield :: Output messages
      println("controlEvent: accessing a string from controller '" + eventName+"': " + textFieldInput);
    
      // Textfield :: Actions
      cp5.get(Textlabel.class,"currentInput").setText("Current Input = " + textFieldInput);
      scenarioButtonVisibilitySwitch(Nscenarios);
    
    } // End of if-statement
    
    configInfo[1] = textFieldInput;
    
    // The following conditional statement was built to allow for the user to view latest user id changes on the confirmation label
    if (configInfo[2] == null) {
      // Here, the array is incomplete so the program cannot update the confirmation label
    } else {
      cp5.get(Textlabel.class,"confirmCurrentInput").setText("User " + configInfo[1] + ", selected scenario " + configInfo[2]);
    } // End of if-statement
    
    // In the case the active control is a Button
  } else if (theEvent.isAssignableFrom(Button.class)) {
    
    // Reading button event information
    String eventName = theEvent.getName();
    println(eventName + " button pressed");
    
    /* ----------------------------------------
     * GENERAL PURPOSE BUTTONS
     --------------------------------------- */
    
    if (eventName.equals("exitApplication")) {     
      // This button triggers the closure of the consys program
      exit();    
    } // End of if-statement "exitApplication" --button press
    
    /* ----------------------------------------
     * SCENARIO BUTTONS
     --------------------------------------- */
     
    // Button recognition routine
    char c1 = eventName.charAt(0);
    char c2 = eventName.charAt(1);
    String buttonTypeID = str(c1) + str(c2);
     
    // Scenario Button Type Verification
    String expected = "sc";
     
    if (buttonTypeID.equals(expected)) {
      
      configInfo[2] = eventName;
       
      if (eventName.equals("sc03")) {

        cp5.get(Textarea.class,"scenarioDetails").setVisible(false); 
        String imageDir = "scenario/" + eventName + "/";
        String imageName = "oto001.jpg";
        String imagePath = imageDir + imageName;
        otoim = loadImage(imagePath);
        scenario3ImageSwitch = 1;
        scenario4VideoSwitch = 0;
        try {
          ophvid.stop();
        } catch (NullPointerException e) {
        }
         
      } else if (eventName.equals("sc04")) {
         
        cp5.get(Textarea.class,"scenarioDetails").setVisible(false);
        String videoDir = "scenario/" + eventName + "/";
        String videoName = "ophvid.mp4";
        String videoPath = videoDir + videoName;
        ophvid = new Movie(this, videoPath);
        scenario4VideoSwitch = 1;
        scenario3ImageSwitch = 0;
         
      } else {
         
        /* ----------------------------------------
        * SCENARIO DETAILS
        *
        * This section creates a text area containing the details of the selected scenario.
        * The information referring to each scenario will be imported from a configuration file.
        *
        --------------------------------------- */
        
        scenario3ImageSwitch = 0;
        scenario4VideoSwitch = 0;
        try {
          ophvid.stop();
        } catch (NullPointerException e) {
        }
    
        String descriptionFilename = "description.txt";
        String descriptionPath = "scenario/" + eventName + "/" + descriptionFilename;
         
        String[] scenarioDescription = loadStrings(descriptionPath);
        String concatDescription = join(scenarioDescription," ");
        println(concatDescription);
         
        cp5.get(Textarea.class,"scenarioDetails").setVisible(true);
        cp5.get(Textarea.class,"scenarioDetails").setText(concatDescription);
        
         
      } // End of if-statement "Specific Button Verification"
      
      // For either scenario button selection, the program sets the confirm selection button visible and provides a visial update of the must current scenario and user id input.
      cp5.get(Button.class,"confirmSelection").setVisible(true);
      cp5.get(Textlabel.class,"confirmCurrentInput").setVisible(true);
      cp5.get(Textlabel.class,"confirmCurrentInput").setText("User " + configInfo[1] + ", selected scenario " + configInfo[2]);
      
    } // End if-statement "Scenario Buttons"
    
    
    if (eventName.equals("confirmSelection")) {
      
      executionState = "record";
      userInfoFile(Nardus);
      clearWindow(Nscenarios);
      
    }
    
    if (eventName.equals("restartApplication")) {

      executionState = "config";
      restartApplication();
      
    } // End of if-statement "Restart Application Button"
    
    
  } // End of if-statemnt "Controller Type Verification"
  
} // End of Control Event Routine

public void movieEvent(Movie ophvid) {
  
  if (scenario4VideoSwitch == 1) {
    ophvid.read();
  }
  
}


/* ========================================
 * FUNCTIONS
 ======================================= */
/*
 * All the functions used for this program have been added as "tabs" to this sketch.
 * When exported as an application, these functions will be embeded within the source folder.
 *
 */


 






     
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
  
  //cp5.get(Textlabel.class,"currentInput").setText("");
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
  
  //cp5.get(Textlabel.class,"confirmCurrentInput").setText("");
  cp5.get(Textlabel.class,"confirmCurrentInput").setVisible(false); // Current user input label
  
  cp5.get(Button.class,"confirmSelection").setColorCaptionLabel(black);
  cp5.get(Button.class,"confirmSelection").setColorBackground(black);
  cp5.get(Button.class,"confirmSelection").setColorForeground(black);
  
  cp5.get(Button.class,"restartApplication").setVisible(true); // Restart button

} // End of clearWindow function
/* ========================================
 * connect2Arduinos
 *
 * The following function establishes a serial connection with multiple Arduinos loaded with the StandardFirmata script.
 * The routine assumes the COM port is always the same.
 *
 * Fluvio L. Lobo Fenoglietto 02/09/2016
 ======================================= */
 
public void connect2Arduinos(int Nardus) {
  
  for (int i = 0; i < Nardus; i ++) {
    
    // The "try-catch" statement works to identify a busy serial port
    try {
      
      // Establiching serial connection
      arduino[i] = new Arduino(this, Arduino.list()[i], 57600);
      
      // Validate connection
      int ledPin = 9;
      arduino[i].digitalWrite(ledPin, Arduino.HIGH);    
      
    } catch(RuntimeException e) {
       
      println("Serial Port Busy");
       
    } // End of try-catch statement
  
  } // End of for-loop "Arduinos"
        
} // End of connect2Arduino function
/* =====================================
 * Execution Log File
 *
 * This function was built with the purpose of creating and updating an execution log file
 * An execution log file consist of a text file containing the iteration and time the consys.pde program was executed
 *
 * Fluvio L. Lobo Fenoglietto 01/31/2016
 ==================================== */

public void exeLogFile(String exeLogFilePath) {
  
  //// First, the program generates the path for the execution file
  //// In the process, the program generates a directory using the CPU date
  //String timeStampFolder = timeStamp("dated-folder");
  //String logFile = "ExecutionLog.txt";
  //String exeLogFilePath = "data/output/" + timeStampFolder + "/" + logFile;
  
  // Here, the program reads such directory looking for the execution log
  // This, of course, may fail if the file has not been created
  String[] logFileLines = loadStrings(exeLogFilePath);
  
  // Conditional statement around the existence of the execution log
  if (logFileLines == null) {
    
    // In the case the file does not exist, the program creates one.
    createOutput(exeLogFilePath); // Generating execution log file
    
    // The initial strings are a combination of headers and the first execution time
    String[] outString = {"", ""};
    outString[0] = "Execution Log for consys.pde";
    String exeTimeStamp = timeStamp("clock");
    outString[1] = "1, " + exeTimeStamp;
    saveStrings(exeLogFilePath, outString);
    
  } else {
    
    // In the case the filke exists, the code must read he lines in order to find where to print the next stamp
    int Nlines = logFileLines.length;
    String[] outString = new String[Nlines+1];
    
    // If the file exists, the program must reprint the previous strings plus the new stamp. The following for loop ensures that.
    for (int i = 0; i <= Nlines; i++) {
      
      if (i < Nlines) {
        
        outString[i] = logFileLines[i];
        
      } else if (i == Nlines) {

        String exeTimeStamp = timeStamp("clock");
        outString[i] = Integer.toString(Nlines) + ", " + exeTimeStamp;
        saveStrings(exeLogFilePath, outString);
        
      } // End of if-statement

    } // End of for-loop
    
  } // End of if-statement
  
} // End of exeLogFile function
/* =====================================
 * readSensorData
 *
 * The following function reads the analog iput data from multiple arduino boards.
 * The number of arduino boards to be accessed is specified by (int) "Nardus".
 * The number of analog ports to be read is specified by (int) "Nports".
 *
 * Fluvio L. Lobo Fenoglietto 02/09/2016
 ==================================== */
    
public void readAnalogData(int dataIndex, int Nardus, int Nports) {
  
  for (int h = 0; h < Nardus; h ++) {
    
    // Variables
    int[] analogPin = new int[Nports];
    int[] analogVal = new int[Nports];
    
    // The following for-loop circles around all the analog ports of the micro-controller board
    for (int i = 0; i < Nports; i ++) {
      
      // Reading and storing analog data into local variables
      analogPin[i] = i; // Define analog pin in array 
      analogVal[i] = arduino[h].analogRead(analogPin[i]); // Read analog value of respective pin
      
    } // End of for-loop "Analog Ports Loop"
    
    // Writing analog data to file
    int arduIndex = h;
    writeAnalogData(dataIndex, arduIndex, analogVal);
    //printArray(analogVal);
  
  } // End of for-loop "Arduinos Loop"
    
} // End of readSensorData function
/* =====================================
 * Restart Application
 *
 * The following function, executed by the restart button, restores the visibility of the primary gui objects.
 * By doing this, the entire script is restarted.
 *
 * Fluvio L. Lobo Fenoglietto 02/19/2016
 ==================================== */

public void restartApplication() {
  
  // When pressed, the button recovers the hidden buttons and labels taken down by clearWindow()
  cp5.get(Button.class,"exitApplication").setVisible(true); // Exit Button
  cp5.get(Textlabel.class,"studentIDLabel").setVisible(true); // Student ID Label/Title
  
  cp5.get(Textfield.class,"userID").setVisible(true); // User ID input
  
  cp5.get(Textlabel.class,"currentInput").setText("Enter SP ID and press Enter/Return");
  cp5.get(Textlabel.class,"currentInput").setVisible(true); // Current user input
  
  cp5.get(Button.class,"confirmSelection").setVisible(false);
  cp5.get(Button.class,"confirmSelection").setColorCaptionLabel(black);
  cp5.get(Button.class,"confirmSelection").setColorBackground(gold);
  cp5.get(Button.class,"confirmSelection").setColorForeground(gray);
  
} // End of restartApplication function
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
/* =====================================
 * Single Digit Correction
 *
 * This function was built with the purpose of adding 0s to the left of single digits.
 * This process is important for the sake of comparing strings.
 *
 * Fluvio L. Lobo Fenoglietto 01/29/2016
 ==================================== */

public String singleDigitCorrection(String prefix, int counter) {
  
  String outString = ""; // Definng output string
  
  if (counter < 10) {
    
    outString = prefix + "0" + Integer.toString(counter);
    
  } else if (counter >= 10) {
    
    outString = prefix + Integer.toString(counter);
    
  } // End of if-statement "Single digit input detection"
  
  return outString;
  
} // End of singleDigitCorrection function
/* =====================================
 * Time Stamp
 *
 * The following function was designed to simplify the need for specifying the time-stamp throughout the code.
 * Additionally, the function corrects for single digit values.
 * 
 * The function takes the input "style" (String), which may be either:
 *     > "calendar" outputs date in the format "mm/dd/yyyy hh:mm:ss"
 *     > "clock" outputs time in the format "hh:mm:ss"
 *
 * Fluvio L. Lobo Fenoglietto 01/28/2016
 ==================================== */
 
public String timeStamp(String style) {
  
  // Variables
  // Input Variables --Processing functions
  int mm = month();
  int dd = day();
  int hh = hour();
  int mi = minute();
  int ss = second();
  
  // Internal Variables
  String month;
  String day;
  String year = Integer.toString(year()); // Does not require correction
  String hour;
  String minute;
  String second;
  
  // Output Variables --To be returned by the function
  String timeStamp = "";
 
  // Correct for single digits
  String prefix = "";
  month = singleDigitCorrection(prefix, mm);
  day = singleDigitCorrection(prefix, dd);
  hour = singleDigitCorrection(prefix, hh);
  minute = singleDigitCorrection(prefix, mi);
  second = singleDigitCorrection(prefix, ss);
  
  // Conditional statement for output type (calendar vs. clock)
  switch (style) {
    
    case "calendar":    
      timeStamp = month + "/" + day + "/" + year + " " + hour + ":" + minute + ":" + second;
      break;      
    case "clock":    
      timeStamp = hour + ":" + minute + ":" + second;
      break;      
    case "dated-folder":    
      timeStamp = month + day + year;
      break;      
    case "timed-filename":
      timeStamp = month + day + year + "-" + hour + minute + second;
      break;
      
  } // End of switch
    
  return timeStamp;
  
} // End of timeStamp function
/* =====================================
 * User Info Path
 *
 * This function creates the directory associated with the input user id
 * The program also saves text file with information regarding the scenario selected
 *
 * Fluvio L. Lobo Fenoglietto 02/09/2016
 ==================================== */
 
public void userInfoFile(int Nardus) {
  
  for (int h = 0; h < Nardus; h ++) {
    
    // First, the button generates the new path
    String userInfoFolder = "data/output/" + timeStampFolder + "/" + configInfo[1] + "/";
    String userInfoFilename = "Info.txt";
    String userInfoPath = userInfoFolder + userInfoFilename;
   
    // Path to data output file --Arduino and other sensor data
    String arduName = "ardu" + Integer.toString(h);
    String dataTimeStamp = timeStamp("timed-filename");
    String dataFilename = arduName + "-" + dataTimeStamp + ".txt";
    String dataFilePath = userInfoFolder + dataFilename;
  
    // The program creates the output file
    createOutput(userInfoPath);
    dataFile[h] = createWriter(dataFilePath);
   
    // The program writes information to the Info file
    String[] outString = new String[4];
    String timeStamp = timeStamp("clock");
    outString[0] = "User Input Summary (Info.txt)";
    outString[1] = "User ID = " + configInfo[1];
    outString[2] = "Scenario = " + configInfo[2];
    outString[3] = "Execution Time = " + timeStamp;
   
    // Write strings to file
    saveStrings(userInfoPath, outString);
   
  } // End of for-loop "Arduinos Loop"
   
} // End of userInfoFile function
/* =====================================
 * Wait Clock
 *
 * The following function creates/draw an analog clock on the current display.
 * The clock uses the CPU time (hour, minutes, seconds).
 *
 * This code has been adapted from a Processing example (https://processing.org/examples/clock.html)
 *
 * Fluvio L. Lobo Fenoglietto 02/19/2016
 ==================================== */

public void waitClock() {
  
  // Variable Definition
  int cx, cy;
  float secondsRadius;
  float minutesRadius;
  float hoursRadius;
  float clockDiameter;
  
  int radius = min(width, height) / 2;
  secondsRadius = radius * 0.72f;
  minutesRadius = radius * 0.60f;
  hoursRadius = radius * 0.50f;
  clockDiameter = radius * 1.8f;
  
  cx = width / 2;
  cy = height / 2;
  
  // Draw the clock background
  fill(0,0,0);
  noStroke();
  ellipse(cx, cy, clockDiameter, clockDiameter);
  
  // Angles for sin() and cos() start at 3 o'clock;
  // subtract HALF_PI to make them start at the top
  float s = map(second(), 0, 60, 0, TWO_PI) - HALF_PI;
  float m = map(minute() + norm(second(), 0, 60), 0, 60, 0, TWO_PI) - HALF_PI; 
  float h = map(hour() + norm(minute(), 0, 60), 0, 24, 0, TWO_PI * 2) - HALF_PI;
  
  // Draw the hands of the clock
  stroke(255);
  strokeWeight(1);
  line(cx, cy, cx + cos(s) * secondsRadius, cy + sin(s) * secondsRadius);
  strokeWeight(2);
  line(cx, cy, cx + cos(m) * minutesRadius, cy + sin(m) * minutesRadius);
  strokeWeight(4);
  line(cx, cy, cx + cos(h) * hoursRadius, cy + sin(h) * hoursRadius);
  
  // Draw the minute ticks
  strokeWeight(2);
  beginShape(POINTS);
  for (int a = 0; a < 360; a+=6) {
    float angle = radians(a);
    float x = cx + cos(angle) * secondsRadius;
    float y = cy + sin(angle) * secondsRadius;
    
    textSize(24);
    fill(255,255,255);
    if (a == 0) {  
      text("3", x+5, y-2.5f);
    } else if (a == 90) {
      text("6", x, y+5);
    } else if (a == 180) {
      text("9", x-5, y-2.5f);
    } else if (a == 270) {
      text("12", x, y-10);
    } else {
      vertex(x, y);
    }
    textAlign(CENTER, CENTER);
  }
  endShape();
  
} // End of waitClock function
/* =====================================
 * writeSensorData2File
 *
 * The following function writes the sensor data to a .txt file
 *
 * Fluvio L. Lobo Fenoglietto 02/09/2016
 ==================================== */
   
public void writeAnalogData(int dataIndex, int arduIndex, int[] analogVal) {

  if (dataIndex == 0) {
      
    // Initial iteration :: Headers for dataFile
    String timeStamp = timeStamp("calendar");
    String headerString1 = "Time Stamp = " + timeStamp;
    dataFile[arduIndex].println(headerString1);
    String headerString2 = "Device Name = " + deviceName;
    dataFile[arduIndex].println(headerString2);
    String headerString3 = "=======================================================";
    dataFile[arduIndex].println(headerString3);
      
    dataFile[arduIndex].flush();
      
  } else if (dataIndex > 0) {
    
    String analogValues = join(nf(analogVal, 0), ", ");
      
    String timeStamp = timeStamp("clock");
    String outString = dataIndex + ", " + timeStamp + ", " + analogValues;
    
    dataFile[arduIndex].println(outString);
    dataFile[arduIndex].flush();
    
  } // End of conditional statement
    
} // End of writeSensorData2File function
  public void settings() {  fullScreen(1); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "consys" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
