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
 void setup() {
   
   //fullscreen(1) // The GUI will cover the entire screen regardless the dimensions
   size(800,400); // The GUI will cover an area of 800x400 pixels - this line can be used for debugging
   //background(black);
   numFont = createFont("Consolas",100);
   pg = createGraphics(width,height,JAVA2D);
   
   // Read Data from Configuration File
   readConfigFile();
   
   // Start Time
   // println(testTimeMinutes + ":00");
   
 } // End of void setup loop
 
 // Void Draw Loop
 void draw() {
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
 