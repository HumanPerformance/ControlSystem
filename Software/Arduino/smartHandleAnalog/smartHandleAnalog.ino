
/*
 * smartHandleAnalog.ino
 * 
 * Smart Handle Analog was developed for the initial prototype of the smart instrument handles, which used analog sensors.
 * 
 * Fluvio L. Lobo Fenoglietto 06/08/2016
 */

void setup() {
  
  Serial.begin(9600);
  
} // End of void setup

void loop() {

  // Read IR and Accelerometer data
  int AX = analogRead(0);
  int AY = analogRead(1);
  int AZ = analogRead(2);
  int IR = analogRead(3);

  // Print IR and Accelerometer data
  Serial.print("AX,");
  Serial.print(AX);
  Serial.print(",AY,");
  Serial.print(AY);
  Serial.print(",AZ,");
  Serial.print(AZ);
  Serial.print(",IR,");
  Serial.println(IR);

  // Delay
  delay(250);

} // End of void loop
