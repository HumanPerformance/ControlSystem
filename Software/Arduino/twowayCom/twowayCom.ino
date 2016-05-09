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
 String inString;
 
 void setup() {
   
   Serial.begin(115200); // Default baudrate for the communication with the raspberry pi
   pinMode(8, OUTPUT);
   
 } // End of void setup
 
 void loop() {
   
   while (state.equals("idle")) {
     
     Serial.print(arduID);
     Serial.print("\n");
     delay(250);
     
     if (Serial.available() > 0) {
       
       inString = Serial.readString();
       
       if (inString.equals("GO")) {
         
         state = "active";
         digitalWrite(8, HIGH);
         
       } // End of if statement :: message check
       
     } // End of if statement :: serial port check
     
   } // End of while loop :: state check
   
 } // End of void loop
