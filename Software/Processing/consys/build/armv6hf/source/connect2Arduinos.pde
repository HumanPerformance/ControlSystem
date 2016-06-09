/* ========================================
 * connect2Arduinos
 *
 * The following function establishes a serial connection with multiple Arduinos loaded with the StandardFirmata script.
 * The routine assumes the COM port is always the same.
 *
 * Fluvio L. Lobo Fenoglietto 02/09/2016
 ======================================= */
 
public void connect2Arduinos(int Nardus) {
  
  for (int i = 0; i < Nardus; i ++) {
    
    // The "try-catch" statement works to identify a busy serial port
    try {
      
      // Establiching serial connection
      arduino[i] = new Arduino(this, Arduino.list()[i], 57600);
      
      // Validate connection
      int ledPin = 9;
      arduino[i].digitalWrite(ledPin, Arduino.HIGH);    
      
    } catch(RuntimeException e) {
       
      println("Serial Port Busy");
       
    } // End of try-catch statement
  
  } // End of for-loop "Arduinos"
        
} // End of connect2Arduino function