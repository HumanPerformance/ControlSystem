/* =====================================
 * writeSensorData2File
 *
 * The following function writes the sensor data to a .txt file
 *
 * Fluvio L. Lobo Fenoglietto 02/04/2016
 ==================================== */
   
public void writeAnalogDataMA(int dataIndex, int Nardus, int[] analogVal) {
    
  if (dataIndex == 0) {
      
    // Initial iteration :: Headers for dataFile
    String timeStamp = timeStamp("calendar");
    String headerString1 = "Time Stamp = " + timeStamp;
    dataFile.println(headerString1);
    String headerString2 = "Device Name = " + deviceName;
    dataFile.println(headerString2);
    String headerString3 = "=======================================================";
    dataFile.println(headerString3);
      
    dataFile.flush();
      
  } else if (dataIndex > 0) {
    
    String analogValues = join(nf(analogVal, 0), ", ");
      
    String timeStamp = timeStamp("clock");
    String outString = dataIndex + ", " + timeStamp + ", " + analogValues;
    
    dataFile.println(outString);
    dataFile.flush();
    
  } // End of conditional statement
    
} // End of writeSensorData2File function