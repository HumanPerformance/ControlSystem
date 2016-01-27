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


// Colors
int black = color(0,0,0);
int gray = color(214,214,214);
int gold = color(255,204,0);
int white = color(255,255,255);

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
  hphlogo = loadImage("hphlogo720res30pp.png");
  
  // GUI Element :: Label :: Student ID Label
  int txtLabelWidth_1 = 275;
  int txtLabelHeight_1 = 50;
  int indentCorrection4Label_1 = 5;
  int textLabelYPos_1 = 50 + topMargin;
  int elementSpacing_1 = 5;
  cp5.addTextlabel("studentIDLabel") // title object
     .setBroadcast(false)
     .setSize(txtLabelWidth_1,txtLabelHeight_1)
     .setPosition(100 - indentCorrection4Label_1, textLabelYPos_1) // set position of the title label
     .setText("Standard Patient ID") // title text
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
  int txtLabelHeight_2 = 50;
  int txtLabelYPos_2 = txtFieldYPos + txtFieldHeight + elementSpacing_2;
  int indentCorrection4Label_2 = 5;
  cp5.addTextlabel("currentInput") // title object
     .setBroadcast(false)
     .setSize(txtLabelWidth_2,txtLabelHeight_2)
     .setPosition(100 - indentCorrection4Label_2, txtLabelYPos_2) // set position of the title label
     .setText("Enter SP ID and hit Enter/Return on your keyboard") // title text
     .setFont(textfont) // set title font :: using lable font and size
     .setColor(white)
     .setBroadcast(true)
     ; 
     
  // GUI Control :: Button :: Begin Exercise
  cp5.addButton("selectScenario")
     .setBroadcast(false) // Avoids the immediate execution of the button
     .setVisible(false)
     .setValue(0)
     .setPosition(100,325)
     .setSize(200,25)
     .setLabel("START")
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
     
  // GUI Control :: Button :: Scenario #1
  int buttonWidth = 125;
  int buttonHeight = 25;
  int buttonXPos_1 = leftMargin;
  int buttonYPos_1 = 300;
  int buttonSpacing = 10;
  
  cp5.addButton("sc1")
     .setBroadcast(false) // Avoids the immediate execution of the button
     //.setVisible(false)
     .setValue(0)
     .setPosition(buttonXPos_1,buttonYPos_1)
     .setSize(buttonWidth,buttonHeight)
     .setLabel("Scenario #1")
     .setColorCaptionLabel(black)
     .setColorBackground(gold)
     .setColorForeground(gray)
     .setBroadcast(true)
     ;
     
  cp5.getController("sc1")
     .getCaptionLabel()
     .setFont(buttonfont)
     .toUpperCase(false)
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
  }
  return textFieldInput;
}

// GUI Element :: Button :: Begin Test
// Pressing this button will execute:
// > Writing of standard patient information to file
public void selectScenario(int theValue) {
  
}