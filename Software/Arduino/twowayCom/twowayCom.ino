/*
 * twowayCom.ino
 *
 * Two way communication has been designed to establish an interation between the arduino modules and the control raspberry pi
 * 
 * Fluvio L. Lobo Fenoglietto 05/09/2016
 *
 */
 
 // Variable Definitions
 String state = "idle";
 String arduID = "oto";
 
 void setup() {
   
   Serial.begin(115200); // Default baudrate for the communication with the raspberry pi
   
 } // End of void setup
 
 void loop() {
   
   while (state.equals("idle")) {
     
     Serial.print(arduID);
     Serial.print("\n");
     delay(250);
     
     if (Serial.available() > 0) {
       
       inString = Serial.read();
       
       if (inString.equals("GO")) {
         
         state = "active";
         
       } // End of if statement :: message check
       
     } // End of if statement :: serial port check
     
   } // End of while loop :: state check
   
   
 } // End of void loop
