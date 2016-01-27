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
int lenX = 600; // pixels
int lenY = 600; // pixels
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
  size(600,600); // These are equivalent to lenX and lenY
  noStroke();
  cp5 = new ControlP5(this);
  
  // GUI Formatting :: Fonts
  PFont pfont_1 = createFont("Arial Rounded MT Bold",20,true);
  ControlFont titlefont = new ControlFont(pfont_1,28); // label font and size
  ControlFont labelfont = new ControlFont(pfont_1, 14); // label font and size
  ControlFont buttonfont = new ControlFont(pfont_1,12); // button font and size
  
  PFont pfont_2 = createFont("Consolas",20,true);
  ControlFont textfont = new ControlFont(pfont_2,14); // button font and size
  
  // GUI Elements :: Images :: Logos
  hphlogo = loadImage("hphlogo720res30pp.png");
  
  // GUI Element :: Label :: Student ID Label
  int txtLabelWidth_1 = 275;
  int txtLabelHeight_1 = 50;
  int indentCorrection4Label_1 = 5;
  cp5.addTextlabel("studentIDLabel") // title object
     .setBroadcast(false)
     .setSize(txtLabelWidth_1,txtLabelHeight_1)
     .setPosition(100 - indentCorrection4Label_1, 200) // set position of the title label
     .setText("Standard Patient ID") // title text
     .setFont(titlefont) // set title font :: using lable font and size
     .setColor(gold)
     .setBroadcast(true)
     ; 
     
  // GUI Control :: Text Field
  int txtFieldWidth = 275;
  int txtFieldHeight = 25;
  cp5.addTextfield("") // No text to be displayed below the field
     .setText("Enter SP Name or ID Number")
     .setPosition(100,250)
     .setSize(txtFieldWidth,txtFieldHeight)
     .setFont(textfont)
     .setColor(gray)
     ;
     
  // GUI Element :: Label :: Current Input
  int txtLabelWidth_2 = 200;
  int txtLabelHeight_2 = 50;
  int indentCorrection4Label_2 = 5;
  cp5.addTextlabel("currentInput") // title object
     .setBroadcast(false)
     .setSize(txtLabelWidth_2,txtLabelHeight_2)
     .setPosition(100 - indentCorrection4Label_2, 285) // set position of the title label
     .setText("Current Input = ") // title text
     .setFont(textfont) // set title font :: using lable font and size
     .setColor(white)
     .setBroadcast(true)
     ; 
     
  // GUI Control :: Button :: Begin Exercise
  cp5.addButton("beginTest")
     .setBroadcast(false) // Avoids the immediate execution of the button
     .setValue(0)
     .setPosition(100,325)
     .setSize(200,25)
     .setLabel("START")
     .setColorCaptionLabel(black)
     .setColorBackground(gold)
     .setColorForeground(gray)
     .setBroadcast(true)
     ;
     
  cp5.getController("beginTest")
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
  image(hphlogo,lenX-180,lenY-90);
  
  
} // End of void-draw loop

/* ========================================
 * INTERFACE BUTTONS
 ======================================= */ 

void controlEvent(ControlEvent theEvent) {
  if(theEvent.isAssignableFrom(Textfield.class)) {
    println("controlEvent: accessing a string from controller '" + theEvent.getName()+"': " + theEvent.getStringValue());
    cp5.get(Textlabel.class,"currentInput").setText("Current Input = " + theEvent.getStringValue());
  }
}

// function colorA will receive changes from 
// controller with name colorA
public void colorA(int theValue) {
  println("a button event from colorA: "+theValue);
}