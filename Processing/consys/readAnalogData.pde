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
    
    // Writing analog data to file
    
    printArray(analogVal);
    
  } // End of for-loop

  writeSensorData2File(dataIndex, val);  
    
} // End of readSensorData function