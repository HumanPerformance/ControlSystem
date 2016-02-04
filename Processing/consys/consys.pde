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
import processing.serial.*;
import cc.arduino.*;
import controlP5.*;

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

// Images
PImage hphlogo;

// GUI Layout Variables
// > GUI Dimensions
int lenX = width; // pixels
int lenY = height; // pixels
int midX = lenX/2; // pixels
int midY = lenY/2; // pixels
// > Margins
int topMargin = 50; // pixels
int rightMargin = 50; // pixels
int bottomMargin = 50; // pixels
int leftMargin = 100; // pixels
// > Colors
int black = color(0,0,0);
int gray = color(214,214,214);
int verydarkgray = color(5,5,5);
int gold = color(255,204,0);
int white = color(255,255,255);

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
Arduino arduino;
int arduPort = 8; // Serial Port Number for the Arduino --This will change depending on the device
String deviceName = "arduOTO";

// Data Acquisition/Record Index
int dataIndex = 0;

// Data File Path 
// Currently the same as userInfoFolder

// Data File Writer
PrintWriter dataFile;


/* ========================================
 * VOID SETUP LOOP
 ======================================= */ 
void setup() {
  
  // Execution Log File
  exeLogFile(exeLogFilePath);
  
  // GUI size
  size(800,800); // These are equivalent to lenX and lenY
  noStroke();
  cp5 = new ControlP5(this);
  
  // GUI Formatting :: Fonts
  PFont pfont_1 = createFont("Arial Rounded MT Bold",20,true);
  ControlFont titlefont = new ControlFont(pfont_1,28); // label font and size
  ControlFont labelfont = new ControlFont(pfont_1, 14); // label font and size
  ControlFont buttonfont = new ControlFont(pfont_1,14); // button font and size
  
  PFont pfont_2 = createFont("Consolas",20,true);
  ControlFont textfont = new ControlFont(pfont_2,14); // button font and size
  
  // GUI Elements :: Images :: Logos
  hphlogo = loadImage("media/hphlogo720res30pp.png");
  
  // GUI Element :: Label :: Student ID Label
  int titleLabelWidth = 250;
  int titleLabelHeight = 50;
  int titleLabelYPos = topMargin;
  cp5.addTextlabel("studentIDLabel") // title object
     .setBroadcast(false)
     .setSize(titleLabelWidth,titleLabelHeight)
     .setPosition(leftMargin - 5, titleLabelYPos) // set position of the title label
     .setText("Standardize Patient ID") // title text
     .setFont(titlefont) // set title font :: using lable font and size
     .setColor(gold)
     .setBroadcast(true)
     ; 
     
  // GUI Control :: Text Field
  int txtFieldWidth = 300;
  int txtFieldHeight = 25;
  int txtFieldYPos = titleLabelYPos + titleLabelHeight + 5;
  cp5.addTextfield("userID") // No text to be displayed below the field
     .setPosition(100,txtFieldYPos)
     .setSize(txtFieldWidth,txtFieldHeight)
     .setFont(textfont)
     .setColor(white)
     .setColorBackground(black)
     .setColorForeground(gray)
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
  int scenarioButtonHeight = 25;
  int scenarioButtonXPos = leftMargin;
  int scenarioButtonYPos0 = currentLabelYPos + currentLabelHeight + 25;
  int[] scenarioButtonYPos = new int[Nscenarios+1];
  int buttonSpacing = 10;
  
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
  int confirmSelectionButtonWidth = 200;
  int confirmSelectionButtonHeight = 25;
  int confirmSelectionButtonXPos = leftMargin;
  int confirmSelectionButtonYPos = scenarioButtonYPos[Nscenarios-1] + scenarioButtonHeight + 50;
  cp5.addButton("confirmSelection")
     .setBroadcast(false) // Avoids the immediate execution of the button
     .setVisible(false)
     .setValue(0)
     .setPosition(confirmSelectionButtonXPos,confirmSelectionButtonYPos)
     .setSize(confirmSelectionButtonWidth,confirmSelectionButtonHeight)
     .setLabel("Confirm Selection")
     .setColorCaptionLabel(black)
     .setColorBackground(gold)
     .setColorForeground(gray)
     .setBroadcast(true)
     ;
     
  cp5.getController("confirmSelection")
     .getCaptionLabel()
     .setFont(buttonfont)
     .toUpperCase(false)
     ;

  // GUI Element :: Label :: Current Input --Confirmation
  int confirmationLabelWidth = 200;
  int confirmationLabelHeight = 25;
  int confirmationLabelXPos = leftMargin + confirmSelectionButtonWidth + 25;
  int confirmationLabelYPos = confirmSelectionButtonYPos + 5;
  // int indent4ConfirmationLabel = 5;
  cp5.addTextlabel("confirmCurrentInput") // title object
     .setBroadcast(false)
     .setSize(confirmationLabelWidth, confirmationLabelHeight)
     .setPosition(confirmationLabelXPos, confirmationLabelYPos)
     .setFont(textfont) // set title font :: using lable font and size
     .setColor(white)
     .setBroadcast(true)
     ; 
  
     
} // End of void-setup loop

/* ========================================
 * VOID DRAW LOOP
 ======================================= */ 

void draw() {
  
  // Execution State Switch
  switch (executionState) {
    
    case "config":
    
      background(black);
  
      // Place Images
      image(hphlogo,width-180,height-90);
      
      if (configIndex == 0) {
        println("Program STATE :: Configuration");
        configIndex = 1;
      } // End of if-statement
      
      break;
      
    case "record":
    
      if (dataIndex == 0) {
        println("Program STATE :: Record");
        
        connect2Arduino();
        readSensorData(dataIndex);
  
        // Updating Indeces
        dataIndex = dataIndex + 1;
        
      } else {
        
        readSensorData(dataIndex);
        
        // Updating Indeces
        dataIndex = dataIndex + 1;
      
      } // End of if-statement

      break;
      
  } // End of switch
  
  
} // End of void-draw loop

/* ========================================
 * CONTROL EVENTS
 ======================================= */ 

public String[] controlEvent(ControlEvent theEvent) {
  
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
    
    // First, the algorithm reads the name of the button.
    String eventName = theEvent.getName();
    println(eventName + " button pressed");
     
    // Button recognition routine
    char c1 = eventName.charAt(0);
    char c2 = eventName.charAt(1);
    String buttonTypeID = str(c1) + str(c2);
     
    // Scenario Button Type Verification
    String expected = "sc";
     
    if (buttonTypeID.equals(expected)) {
      
      configInfo[2] = eventName;
       
      if (eventName.equals("sc03")) {
         
        // Will place an image here!
        println("An image will be embeded here!");
         
      } else if (eventName.equals("sc04")) {
         
        // Will palce a video here
        println("A video will be embeded here!");
         
      } else {
         
        /* ----------------------------------------
        * SCENARIO DETAILS
        *
        * This section creates a text area containing the details of the selected scenario.
        * The information referring to each scenario will be imported from a configuration file.
        *
        --------------------------------------- */
    
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
      cp5.get(Textlabel.class,"confirmCurrentInput").setText("User " + configInfo[1] + ", selected scenario " + configInfo[2]);
    
      
    } // End if-statemnt "Button Type Verification"
    
  } // End of if-statemnt "Controller Type Verification"
  
  // printArray(configInfo); // Use for debugging
  return configInfo;
  
} // End of Control Event Routine

/* ----------------------------------------
 * BUTTONS
 ---------------------------------------- */

// Confirm selection
public void confirmSelection(int theValue) {
  
  // First, the button triggers the creation of user-input specific folders and files
  userInfoFile();
  
  executionState = "record";
  

}

/* ========================================
 * FUNCTIONS
 ======================================= */
 
/* ---------------------------------------
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
 *
 -------------------------------------- */
 
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
 
/* ---------------------------------------
 * Scenario Button Visibility
 *
 * This function changes the visibility of the scenario buttons to "true".
 *
 * Fluvio L. Lobo Fenoglietto 01/28/2016
 --------------------------------------- */ 
 
public void scenarioButtonVisibilitySwitch(int Nscenarios) {
   
  // Set scenario buttons visible for the user
  for (int i = 1; i <= Nscenarios; i++) {
    
    String prefix = "sc";
    String controllerName = singleDigitCorrection(prefix, i);
    // println(controllerName);
    cp5.get(Button.class,controllerName).setVisible(true);
    
  } // End of for-loop --Loop around scenario buttons
   
} // End of function scenarioButtonVisibilitySwitch


/* ---------------------------------------
 * Single Digit Correction
 *
 * This function was built with the purpose of adding 0s to the left of single digits.
 * This process is important for the sake of comparing strings.
 *
 * Fluvio L. Lobo Fenoglietto 01/29/2016
 --------------------------------------- */

public String singleDigitCorrection(String prefix, int counter) {
  
  String outString = ""; // Definng output string
  
  if (counter < 10) {
    
    outString = prefix + "0" + Integer.toString(counter);
    
  } else if (counter >= 10) {
    
    outString = prefix + Integer.toString(counter);
    
  } // End of if-statement "Single digit input detection"
  
  return outString;
  
} // End of singleDigitCorrection function

/* ---------------------------------------
 * Execution Log File
 *
 * This function was built with the purpose of creating and updating an execution log file
 * An execution log file consist of a text file containing the iteration and time the consys.pde program was executed
 *
 * Fluvio L. Lobo Fenoglietto 01/31/2016
 --------------------------------------- */

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

/* ---------------------------------------
 * User Info Path
 *
 * This function creates the directory associated with the input user id
 * The program also saves text file with information regarding the scenario selected
 *
 * Fluvio L. Lobo Fenoglietto 02/01/2016
 --------------------------------------- */
 
 public void userInfoFile() {
   
   // First, the button generates the new path
   String userInfoFolder = "data/output/" + timeStampFolder + "/" + configInfo[1] + "/";
   String userInfoFilename = "Info.txt";
   String userInfoPath = userInfoFolder + userInfoFilename;
   
   // Path to data output file --Arduino and other sensor data
   String dataTimeStamp = timeStamp("timed-filename");
   String dataFilename = "dataFile-" + dataTimeStamp + ".txt";
   String dataFilePath = userInfoFolder + dataFilename;
  
   // The program creates the output file
   createOutput(userInfoPath);
   dataFile = createWriter(dataFilePath);
   
   // The program writes information to the Info file
   String[] outString = new String[4];
   String timeStamp = timeStamp("clock");
   outString[0] = "User Input Summary (Info.txt)";
   outString[1] = "User ID = " + configInfo[1];
   outString[2] = "Scenario = " + configInfo[2];
   outString[3] = "Execution Time = " + timeStamp;
   
   // Write strings to file
   saveStrings(userInfoPath, outString);
   
 }
 

   
   
 /* readSensorData
  *
  * The following function reads the analog data measured by a specific sensor.
  *
  */
    
public void readSensorData(int dataIndex) {
  
  // Sensor read
  int analogPin = 0;
  int val = arduino.analogRead(analogPin);
  println(val);

  writeSensorData2File(dataIndex, val);  
    
} // End of readSensorData function
  
  
/* writeSensorData2File
 *
 * The following function writes the sensor data to a .txt file
 *
 */
   
public void writeSensorData2File(int dataIndex, int val) {
    
  if (dataIndex == 0) {
      
    // Initial iteration :: Headers for dataFile
    String timeStamp = timeStamp("calendar");
    String headerString1 = "Time Stamp = " + timeStamp;
    dataFile.println(headerString1);
    String headerString2 = "Device Name = " + deviceName;
    dataFile.println(headerString2);
    String headerString3 = "Sensor (Analog/Digital Pin) = Proximity (A0)";
    dataFile.println(headerString3);
    String headerString4 = "=======================================================";
    dataFile.println(headerString4);
      
    dataFile.flush();
      
  } else if (dataIndex > 0) {
      
    String timeStamp = timeStamp("clock");
    String dataString = dataIndex + ", " + timeStamp + ", " + val;
    dataFile.println(dataString);
    dataFile.flush();
    
  } // End of conditional statement
    
} // End of writeSensorData2File function