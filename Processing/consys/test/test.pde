

import processing.serial.*;
import cc.arduino.*;

Arduino arduino;

void setup() {
 
  printArray(Arduino.list());
  
  arduino = new Arduino(this, Arduino.list()[1], 57600);
  
  int ledPin = 9;
  arduino.digitalWrite(ledPin, Arduino.HIGH); 
  
  
}

void draw() {
  
}