import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class countdown extends PApplet {

/*
 * countdown
 * The following program has been created with the purpose of displaying a countdown clock for the clinical skills exam
 * Fluvio L. Lobo Fenoglietto 05/18/2016
 */
 
 // Variables
 // > Data Directory and Files
 String configFile = "countdownInit.txt";
 String[] configInfo;
 
 // > Test Variables
 int testTimeMinutes; // 20 minutes
 int testTimeWarning; // When 5 minutes are left on the clock, formatting changes to cue the tester
 int startTime = 0;
 int countDownMinutes;
 int countDownSeconds = 0;

 // Objects
 PFont numFont;
 PGraphics pg;

 // > Colors
 int black = color(0,0,0);
 int red = color(255, 0, 0);
 int green = color(0, 255, 0);
 
 
 // Void Setup Loop
 public void setup() {
   
    // The GUI will cover the entire screen regardless the dimensions
   //size(800,400); // The GUI will cover an area of 800x400 pixels - this line can be used for debugging
   //background(black);
   numFont = createFont("Consolas",100);
   pg = createGraphics(width,height,JAVA2D);
   
   // Read Data from Configuration File
   readConfigFile();
   
   // Start Time
   // println(testTimeMinutes + ":00");
   
 } // End of void setup loop
 
 // Void Draw Loop
 public void draw() {
   //background(black);
   if (countDownSeconds == 0) {
     countDownMinutes = countDownMinutes - 1;
     startTime = millis();
   } // End of if statement - minutes check
   if (countDownMinutes < 0) {
     pg.beginDraw();
     pg.smooth();
     pg.background(0);
     pg.fill(red);
     pg.textAlign(CENTER,CENTER);
     pg.textFont(numFont, 100);
     pg.text("GAME OVER!", width/2, height/2);
     pg.endDraw();
     image(pg,0,0);
     // delay(20000);
     // exit();
   } else {
     countDownSeconds = 59 - (millis() - startTime)/1000;
     String minString = singleDigitCorrection("",countDownMinutes);
     String secString = singleDigitCorrection(":",countDownSeconds);
     String timeString = minString + secString;
     // println(timeString);
     pg.beginDraw();
     pg.smooth();
     pg.background(0);
     if (countDownMinutes <= testTimeWarning) {
       pg.fill(red);
     } else {
       pg.fill(green);
     } // End of if statement - warning time check
     pg.textAlign(CENTER,CENTER);
     pg.textFont(numFont, 200);
     pg.text(timeString, width/2, height/2);
     pg.endDraw();
     image(pg,0,0);
     delay(1000); 
   } // End of if statement - test time limit check
 } // End of void draw loop
 
/*
 * References
 * 1- Loading Strings from Text File - https://processing.org/tutorials/data/
 * 2- Using Switch Statements - https://processing.org/reference/switch.html
 */
 
/*
 * readConfigFile.pde
 *
 * The following function was created to read data, in the form of strings, from a configuration or input file.
 * The configuration file is written and stored within the data folder by a separate program.
 *
 * Fluvio L. Lobo Fenoglietto 05/19/2016
 */
 
 public void readConfigFile() {
   
   // Read Configuration File Data
   configInfo = loadStrings(configFile);
   printArray(configInfo);
   
   int Nlines = configInfo.length;
   String[] splitString;
   for (int i = 0; i < Nlines; i ++) {
     
     splitString = split(configInfo[i],':');
     
     switch(splitString[0]) {
       
       case "StartTime":
       
         testTimeMinutes = PApplet.parseInt(splitString[splitString.length-1]);
         countDownMinutes = testTimeMinutes;
         println("Test Time : " + testTimeMinutes);
         println("Countdown Time : " + countDownMinutes);
     
      case "WarningTime":
      
        testTimeWarning = PApplet.parseInt(splitString[splitString.length-1]);
         println("Warning Time : " + testTimeWarning);
       
     } // End of switch statement - conditional around the content of the configuration file
   } // End of for loop - strings loaded from configuration file
 } // End of function - readConfigFile
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
  public void settings() {  fullScreen(1); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "countdown" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
