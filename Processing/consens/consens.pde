/**
 * 
 * HPH Knowledgebase
 * Processing Development
 * Fluvio L Lobo Fenoglietto
 *
 */
 
// Import Libraries
import processing.serial.*;
import cc.arduino.*;
import controlP5.*;

// Variables

Serial comPort;
Arduino arduino;

// Device Identifiers
String deviceName = "arduOTO";

int arduPort = 8;

// >> Indeces
int dataIndex = 0; // Index used to index or enumerate data reads

// >> Output Variables
PrintWriter dataFile;

/* ===================================================================
 * VOID SETUP LOOP
 * =================================================================*/

void setup() {

  size(400,400);
  
  // Connecting to Arduino
  connect2Arduino();
  
  // Output
  // > Data file
  dataFile = createWriter("otoDataFile.txt"); // Path can be changed to specify a directory
  

} // End of void-setup loop

/* ===================================================================
 * VOID DRAW LOOP
 * =================================================================*/

void draw() {
  
  // Draw Backgorund
  int bgColor = color(0,0,0);
  background(bgColor);
  
  readSensorData(dataIndex);
  
  // Updating Indeces
  dataIndex = dataIndex + 1;


} // End of void-draw loop

/* ===================================================================
 * FUNCTIONS
 * =================================================================*/
 
 /* connect2Arduino
  *
  * The following function establishes a serial connection with an Arduino loaded with the StandardFirmata script.
  * The routine assumes the COM port is always the same.
  *
  */
 
 public void connect2Arduino() {
   
   // The "try-catch" statement works to identify a busy serial port
   try {
     
    // Establiching serial connection
    arduino = new Arduino(this, Arduino.list()[arduPort], 57600);
    
    // Validate connection
    int ledPin = 9;
    arduino.digitalWrite(ledPin, Arduino.HIGH);    
    
   } catch(RuntimeException e) {
     
     println("Serial Port Busy");
     
   } // End of try-catch statement
   
 } // End of connect2Arduino function
 
 
 /* readSensorData
  *
  * The following function reads the analog data measured by a specific sensor.
  *
  */
  
public void readSensorData(int dataIndex) {
  
    // Sensor read
  int analogPin = 0;
  int val = arduino.analogRead(analogPin);
  println(val);
  
  // Writing data to file
  //dataFile.println(val);
  //dataFile.flush();
  //dataFile.close();
  writeSensorData2File(dataIndex, val);
  
  
} // End of readSensorData function


/* writeSensorData2File
 *
 * The following function writes the sensor data to a .txt file
 *
 */
 
public void writeSensorData2File(int dataIndex, int val) {
  
  if (dataIndex == 0) {
    
    // Initial iteration :: Headers for dataFile
    String timeStamp = timeStamp("calendar");
    String headerString1 = "Time Stamp = " + timeStamp;
    dataFile.println(headerString1);
    String headerString2 = "Device Name = " + deviceName;
    dataFile.println(headerString2);
    String headerString3 = "Sensor (Analog/Digital Pin) = Proximity (A0)";
    dataFile.println(headerString3);
    String headerString4 = "=======================================================";
    dataFile.println(headerString4);
    
    dataFile.flush();
    
  } else if (dataIndex > 0) {
    
    String timeStamp = timeStamp("clock");
    String dataString = dataIndex + ", " + timeStamp + ", " + val;
    dataFile.println(dataString);
    dataFile.flush();
  
  } // End of conditional statement
  
} // End of writeSensorData2File function

/* timeStamp
 *
 * The following function was designed to simplify the need for specifying the time-stamp throughout the code.
 * Additionally, the function corrects for single digit values.
 * 
 * The function takes the input "style" (String), which may be either:
 *     > "calendar" outputs date in the format "mm/dd/yyyy hh:mm:ss"
 *     > "clock" outputs time in the format "hh:mm:ss"
 *
 */
 
public String timeStamp(String style) {
  
  // Variables
  String month;
  String day;
  String year;
  String hour;
  String minute;
  String second;
  String timeStamp = " ";
 
  // Define month
  int mm = month();
  
  // Correct for single digits
  if (mm < 10) {
    
    month = "0" + mm;
    
  } else {
    
    month = Integer.toString(mm);
    
  } // End of conditional statement
  
  // Define day
  int dd = day();
  
  // Correct for single digits
  if (dd < 10) {
    
    day = "0" + dd;
    
  } else {
    
    day = Integer.toString(dd);
    
  } // End of conditional statement
  
  // Define year
  year = Integer.toString(year());
  
  // Define hour
  int hh = hour();
  
  if (hh < 10) {
    
    hour = "0" + hh;
    
  } else {
    
    hour = Integer.toString(hh);
    
  } // End of conditional Statement
  
  // Define minute
  int mi = minute();
  
  if (mi < 10) {
    
    minute = "0" + mi;
    
  } else {
    
    minute = Integer.toString(mi);
    
  } // End of conditional Statement
  
  // Define second
  int ss = second();
  
  if (ss < 10) {
    
    second = "0" + ss;
    
  } else {
    
    second = Integer.toString(ss);
    
  } // End of conditional Statement
  
  
  if (style.equals("calendar")) {
    
    timeStamp = month + "/" + day + "/" + year + " " + hour + ":" + minute + ":" + second;
    
  } else if (style.equals("clock")) {
    
    timeStamp = hour + ":" + minute + ":" + second;
    
  } // End of conditional statement
    
  return timeStamp;
  
} // End of timeStamp function

public String digitCorrect(int inVal) {
  
 String outVal;
  
 if (inVal < 10) {
    
   outVal = "0" + inVal;
    
 } else {
    
   outVal = Integer.toString(inVal);
    
 } // End
 
 return outVal;
  
} // End of digitCorrect function
 