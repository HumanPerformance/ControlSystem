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
import processing.video.*;

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
int Nardus = 2;
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
void setup() {
  
  // Execution Log File
  exeLogFile(exeLogFilePath);
  
  // GUI size
  //fullScreen(1);
  size(800,480); // These are the dimensions of the RasPi screen
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
     ; 
     
  // GUI Control :: Text Field
  int txtFieldWidth = 300;
  int txtFieldHeight = 25;
  int txtFieldXPos = leftMargin;
  int txtFieldYPos = titleLabelYPos + titleLabelHeight - 10;
  cp5.addTextfield("userID") // No text to be displayed below the field
     .setPosition(txtFieldXPos,txtFieldYPos)
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
    
      if (dataIndex == 0) {
        
        println("Program STATE :: Record");
        
        connect2Arduinos(Nardus);
        
        // Updating Indeces
        dataIndex = dataIndex + 1;
        
      } else {
        
        readAnalogData(dataIndex, Nardus, Nports);
        
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
      cp5.get(Textlabel.class,"confirmCurrentInput").setText("User " + configInfo[1] + ", selected scenario " + configInfo[2]);
    
      
    } // End if-statemnt "Scenario Buttons"
    
  } // End of if-statemnt "Controller Type Verification"
  
  // printArray(configInfo); // Use for debugging
  return configInfo;
  
} // End of Control Event Routine

void movieEvent(Movie ophvid) {
  
  if (scenario4VideoSwitch == 1) {
    ophvid.read();
  }
  
}

/* ----------------------------------------
 * BUTTONS
 ---------------------------------------- */

// Confirm selection
public void confirmSelection(int theValue) {
  
  // First, the button triggers the creation of user-input specific folders and files
  userInfoFile(Nardus);
  
  executionState = "record";
  
}

/* ========================================
 * FUNCTIONS
 ======================================= */
/*
 * All the functions used for this program have been added as "tabs" to this sketch.
 * When exported as an application, these functions will be embeded within the source folder.
 *
 */


 






     