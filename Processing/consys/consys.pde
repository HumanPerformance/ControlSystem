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
import controlP5.*;

// Variables
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

// Technical Variables
// Number of scenarios
int Nscenarios = 12;

/* ========================================
 * VOID SETUP LOOP
 ======================================= */ 
void setup() {
  
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
  int txtLabelWidth_1 = 250;
  int txtLabelHeight_1 = 50;
  int indentCorrection4Label_1 = 5;
  int textLabelYPos_1 = topMargin + 25;
  int elementSpacing_1 = 5;
  cp5.addTextlabel("studentIDLabel") // title object
     .setBroadcast(false)
     .setSize(txtLabelWidth_1,txtLabelHeight_1)
     .setPosition(100 - indentCorrection4Label_1, textLabelYPos_1) // set position of the title label
     .setText("Standardize Patient ID") // title text
     .setFont(titlefont) // set title font :: using lable font and size
     .setColor(gold)
     .setBroadcast(true)
     ; 
     
  // GUI Control :: Text Field
  int txtFieldWidth = 275;
  int txtFieldHeight = 25;
  int txtFieldYPos = textLabelYPos_1 + txtLabelHeight_1 + elementSpacing_1;
  int elementSpacing_2 = 10;
  cp5.addTextfield("") // No text to be displayed below the field
     .setPosition(100,txtFieldYPos)
     .setSize(txtFieldWidth,txtFieldHeight)
     .setFont(textfont)
     .setColor(gray)
     ;
     
  // GUI Element :: Label :: Current Input
  int txtLabelWidth_2 = 200;
  int txtLabelHeight_2 = 25;
  int txtLabelYPos_2 = txtFieldYPos + txtFieldHeight + elementSpacing_2;
  int indentCorrection4Label_2 = 5;
  cp5.addTextlabel("currentInput") // title object
     .setBroadcast(false)
     .setSize(txtLabelWidth_2,txtLabelHeight_2)
     .setPosition(100 - indentCorrection4Label_2, txtLabelYPos_2) // set position of the title label
     .setText("Enter SP ID and press Enter/Return") // title text
     .setFont(textfont) // set title font :: using lable font and size
     .setColor(white)
     .setBroadcast(true)
     ; 
     
  // GUI Control :: Button :: Select Scenario
  int selectButtonWidth = 200;
  int selectButtonHeight = txtFieldHeight;
  int selectButtonXPos = leftMargin + txtFieldWidth + 25;
  int selectButtonYPos = txtFieldYPos;
  cp5.addButton("selectScenario")
     .setBroadcast(false) // Avoids the immediate execution of the button
     .setVisible(false)
     .setValue(0)
     .setPosition(selectButtonXPos,selectButtonYPos)
     .setSize(selectButtonWidth,selectButtonHeight)
     .setLabel("Select Scenario")
     .setColorCaptionLabel(black)
     .setColorBackground(gold)
     .setColorForeground(gray)
     .setBroadcast(true)
     ;
     
  cp5.getController("selectScenario")
     .getCaptionLabel()
     .setFont(buttonfont)
     .toUpperCase(false)
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
  int buttonXPos_1 = leftMargin;
  int buttonYPos0 = txtLabelYPos_2 + txtLabelHeight_2 + 25;
  int[] buttonYPos = new int[Nscenarios+1];
  int buttonSpacing = 10;
  
  // Creator Loop
  for (int i = 0; i < Nscenarios; i++) {
    
    String buttonName = " ";
    String buttonLabelText = " ";
    
    if (i < 10) {
      
      buttonName = "sc0" + (i + 1); // Controller Name or ID
      buttonLabelText = "Scenario #0" + (i + 1); // Button Label
      
    } else if (i >= 10) {
      
      buttonName = "sc0" + (i + 1); // Controller Name or ID
      buttonLabelText = "Scenario #0" + (i + 1); // Button Label
      
    } // End of if-statement "Single Digit Correction"
    
    if (i == 0) {
      
      buttonYPos[i] = buttonYPos0;  

    } else if (i > 0) {
      
      buttonYPos[i] = buttonYPos[i-1] + scenarioButtonHeight + buttonSpacing;
        
    } // End of if-statement
    
    // GUI Controller :: Button :: Scenario #i
    cp5.addButton(buttonName)
        .setBroadcast(false) // Avoids the immediate execution of the button
        .setVisible(false)
        .setValue(0)
        .setPosition(buttonXPos_1,buttonYPos[i])
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
  int txtareaYPos = buttonYPos0;
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
     //.setText("hola me llamo jamon")
     ; 
     
} // End of void-setup loop

/* ========================================
 * VOID DRAW LOOP
 ======================================= */ 

void draw() {
  
  background(black);
  
  // Place Images
  image(hphlogo,width-180,height-90);
  
  
} // End of void-draw loop

/* ========================================
 * INTERFACE BUTTONS
 ======================================= */ 

public String controlEvent(ControlEvent theEvent) {
  
  // Variables
  String eventName = "";
  String textFieldInput = "";
  
  if(theEvent.isAssignableFrom(Textfield.class)) {
    
    eventName = theEvent.getName();
    textFieldInput = theEvent.getStringValue();
    println("controlEvent: accessing a string from controller '" + eventName+"': " + textFieldInput);
    cp5.get(Textlabel.class,"currentInput").setText("Current Input = " + textFieldInput);
    cp5.get(Button.class,"selectScenario").setVisible(true);
    
  } else if (theEvent.isAssignableFrom(Button.class)) {
    
     // First, the algorithm reads the name of the button.
     eventName = theEvent.getName();
     println(eventName + "button pressed");
     
     // Button recognition routine
     char c1 = eventName.charAt(0);
     char c2 = eventName.charAt(1);
     String buttonTypeID = str(c1) + str(c2);
         
     // Scenario Button Type Verification
     String expected = "sc";
     
     if (buttonTypeID.equals(expected)) {
       
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
       
     } // End of if-statement "Button Type Verification"
    
  } // End of if-statemnt "Controller Type Verification"
  
  return textFieldInput;
  
} // End of Control Event Routine

// GUI Element :: Button :: Begin Test
// Pressing this button will execute:
// > Writing of standard patient information to file
public void selectScenario(int theValue) {
 
  println("hola");
  scenarioButtonVisibilitySwitch(Nscenarios);
  
} // End of selectScenario button call

/* ========================================
 * FUNCTIONS
 ======================================= */
 
public void scenarioButtonVisibilitySwitch(int Nscenarios) {
   
  // Set scenario buttons visible for the user
  for (int i = 1; i <= Nscenarios; i++) {
    
    String controllerName = "sc" + i;
    cp5.get(Button.class,controllerName).setVisible(true);
    
  } // End of for-loop --Loop around scenario buttons
   
} // End of function scenarioButtonVisibilitySwitch