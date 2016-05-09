/*
 * analogDataRelay.ino
 *
 * The following script has been designed to test an alternative approach at communicating with the Arduino modules, which does not involve any firmware that forces the Arduino to act as a slave.
 *
 * Fluvio L. Lobo Fenoglietto 05/09/2016
 *
 */
 
 // Variable Initialization
 int analogPin = 0;
 int analogVal = 0;
 
 void setup() {
   Serial.begin(115200);
 } // End of void setup
 
 void loop() {
   analogVal = analogRead(analogPin);
   Serial.print(analogVal);
   Serial.print("\n");
   delay(250);
 } // End of void loop
 
