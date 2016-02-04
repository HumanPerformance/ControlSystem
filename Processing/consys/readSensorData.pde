/* =====================================
 * readSensorData
 *
 * The following function reads the analog data measured by a specific sensor.
 *
 * Fluvio L. Lobo Fenoglietto 02/04/2016
 ==================================== */
    
public void readSensorData(int dataIndex) {
  
  // Sensor read
  int analogPin = 0;
  int val = arduino.analogRead(analogPin);
  println(val);

  writeSensorData2File(dataIndex, val);  
    
} // End of readSensorData function