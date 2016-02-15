/* =====================================
 * readSensorDataMA
 *
 * The following function reads the analog iput data from multiple arduino boards.
 * The number of arduino boards to be accessed is specified by (int) "Nardus".
 * The number of analog ports to be read is specified by (int) "Nports".
 *
 * Fluvio L. Lobo Fenoglietto 02/09/2016
 ==================================== */
    
public void readAnalogData(int dataIndex, int Nardus, int Nports) {
  
  for (int h = 0; h < Nardus; h ++) {
    
    // Variables
    int[] analogPin = new int[Nports];
    int[] analogVal = new int[Nports];
    
    // The following for-loop circles around all the analog ports of the micro-controller board
    for (int i = 0; i < Nports; i ++) {
      
      // Reading and storing analog data into local variables
      analogPin[i] = i; // Define analog pin in array 
      analogVal[i] = arduino[h].analogRead(analogPin[i]); // Read analog value of respective pin
      
    } // End of for-loop "Analog Ports Loop"
    
    // Writing analog data to file
    int arduIndex = h;
    writeAnalogData(dataIndex, arduIndex, analogVal);
    printArray(analogVal);
  
  } // End of for-loop "Arduinos Loop"
    
} // End of readSensorData function