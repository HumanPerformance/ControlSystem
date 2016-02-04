/* =====================================
 * readSensorData
 *
 * The following function reads the analog data measured by a specific sensor.
 *
 * Fluvio L. Lobo Fenoglietto 02/04/2016
 ==================================== */

/* The function readAnalogData() takes the following inputs
 *
 * > (int) dataIndex = counter for data indexing
 * > (int) Nports = number of analog ports to read from --more flexible than specifying the Arduino port
 * >
 *
*/
    
    
public void readAnalogData(int dataIndex, int Nports) {
  
  // Variables
  int[] analogPin = new int[Nports];
  int[] analogVal = new int[Nports];
  
  // The following for-loop circles around all the analog ports of the micro-controller board
  for (int i = 0; i < Nports; i ++) {
    
    // Reading and storing analog data into local variables
    analogPin[i] = i; // Define analog pin in array 
    analogVal[i] = arduino.analogRead(analogPin[i]); // Read analog value of respective pin
    
  } // End of for-loop
  
  // Writing analog data to file
  writeAnalogData(dataIndex, analogVal); 
  printArray(analogVal);
    
} // End of readSensorData function