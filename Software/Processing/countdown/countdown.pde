/*
 * countdown
 * The following program has been created with the purpose of displaying a countdown clock for the clinical skills exam
 * Fluvio L. Lobo Fenoglietto 05/18/2016
 */
 
 
 // Importing Libraries
 
 
 // Variables
 // > Test Variables
int testTimeMinutes = 20; // 20 minutes

int startTime = 0;
int countDownMinutes = testTimeMinutes;
int countDownSeconds = 0;

 // > Colors
 int black = color(0,0,0);
 
 
 // Void Setup Loop
 void setup() {
   
   //fullscreen(1) // The GUI will cover the entire screen regardless the dimensions
   size(800,400); // The GUI will cover an area of 800x400 pixels - this line can be used for debugging
   background(black);
   
   // Start Time
   println(testTimeMinutes + ":00");
   
 } // End of void setup loop
 
 // Void Draw Loop
 void draw() {
  
   if (countDownSeconds == 0) {
     countDownMinutes = countDownMinutes - 1;
     startTime = millis();
   } // End of if statement - minutes check
   countDownSeconds = 59 - (millis() - startTime)/1000;
   String minString = singleDigitCorrection("",countDownMinutes);
   String secString = singleDigitCorrection(":",countDownSeconds);
   println(minString + secString);
   delay(1000);
   
 } // End of void draw loop
 
 