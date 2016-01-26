/**
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
int lenX = 600; // pixels
int lenY = 600; // pixels
int midX = lenX/2; // pixels
int midY = lenY/2; // pixels

// Labels
Textlabel studentIDLabel;

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
  PFont pfont = createFont("Arial Rounded MT Bold",20,true);
  ControlFont titlefont = new ControlFont(pfont,48); // label font and size
  ControlFont labelfont = new ControlFont(pfont,28); // label font and size
  ControlFont textfont = new ControlFont(pfont,12); // button font and size
  ControlFont buttonfont = new ControlFont(pfont,12); // button font and size
  
  // GUI Elements :: Images :: Logos
  hphlogo = loadImage("hphlogo720res30pp.png");
  
  // GUI Element :: Label :: Student ID Label
  cp5.addTextlabel("studentIDLabel") // title object
     .setBroadcast(false)
     .setSize(200,100)
     .setPosition(width/4,50) // set position of the title label
     .setText("Student ID") // title text
     .setFont(labelfont) // set title font :: using lable font and size
     .setColor(gold)
     .setBroadcast(true)
     .getCaptionLabel().align(CENTER,CENTER)
     ;
     
  // GUI Control :: Text Field
  
  // GUI Control :: Button :: Begin Exercise
  cp5.addButton("beginTest")
     .setBroadcast(false) // Avoids the immediate execution of the button
     .setValue(0)
     .setPosition(100,100)
     .setSize(200,19)
     ;

  PImage[] imgs = {loadImage("button_a.png"),loadImage("button_b.png"),loadImage("button_c.png")};
  cp5.addButton("play")
     .setValue(128)
     .setPosition(140,300)
     .setImages(imgs)
     .updateSize()
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

public void controlEvent(ControlEvent theEvent) {
  println(theEvent.getController().getName());
}

// function colorA will receive changes from 
// controller with name colorA
public void colorA(int theValue) {
  println("a button event from colorA: "+theValue);
}