/*
 * smartHandle.ino
 *
 * The following script has been designed to control the arduino module and sensors embedded into our instrument handles
 *
 * Fluvio L. Lobo Fenoglietto 05/11/2016
 */
 
/*
 * Importing Libraries and Modules
 */
#include <Wire.h>
#include <SPI.h>
#include <SparkFunLSM9DS1.h>
#include <SparkFun_VL6180X.h>
/* Note that:
 * - The user may need to download and install this SparkFun library separately. This code will not install the library!
 * - The name of the library shown here has been modified by the user to match the name of the local library (as saved in /sketchbook/libraries/...)
 */

/*
 * Objects and/or Constructors
 */
LSM9DS1 imu;


/* 
 * Sensor Configuration Paramaters and/or Variables
 */

 // IMU
#define LSM9DS1_M	0x1E // Would be 0x1C if SDO_M is LOW
#define LSM9DS1_AG	0x6B // Would be 0x6A if SDO_AG is LOW
// Earth's magnetic field varies by location. Add or subtract 
// a declination to get a more accurate heading. Calculate 
// your's here:
// http://www.ngdc.noaa.gov/geomag-web/#declination
#define DECLINATION -8.58 // Declination (degrees) in Boulder, CO.

 // ToF Range Finder
#define VL6180X_ADDRESS 0x29
VL6180xIdentification identification;
VL6180x sensor(VL6180X_ADDRESS);
 
/*
 * Void Setup
 * - Serial Port Configuration
 * - I2C Configuration
 * - IMU Configuration
 * - ToF Range Finder Configuration
 */
void setup() {
  
  Serial.begin(115200); // Start Serial Library
  Wire.begin(); // Start I2C Library
  
  // Initializing IMU
  imu.settings.device.commInterface = IMU_MODE_I2C;
  imu.settings.device.mAddress = LSM9DS1_M;
  imu.settings.device.agAddress = LSM9DS1_AG;
  
  if (!imu.begin()) {
    Serial.println("Failed to communicate with LSM9DS1.");
    Serial.println("Double-check wiring.");
    Serial.println("Default settings in this sketch will " \
                  "work for an out of the box LSM9DS1 " \
                  "Breakout, but may need to be modified " \
                  "if the board jumpers are.");
    while (1);
  } // End of if statement - verification of connection with IMU
  
  // Initializing ToF Range Finder
  sensor.getIdentification(&identification); // Retrieve manufacture info from device memory
  //printIdentification(&identification); // Helper function to print all the Module information

  if(sensor.VL6180xInit() != 0) {
    Serial.println("FAILED TO INITALIZE"); //Initialize device and check for errors
  } 

  sensor.VL6180xDefautSettings(); //Load default settings to get started.
  
} // End of void setup loop

/*
 * Void Loop
 * - IMU Data
 *   - Gyroscope Data
 *   - Accelerometer Data
 *   - Magnetometer Data
 *   - Attitude: 
 */
void loop() {
  
  // IMU
  printGyro();                                                     // Print "GYR,gx,gy,gz,"
  printAccel();                                                    // Print "ACC,ax,ay,az,"
  printMag();                                                      // Print "MAG,mx,my,mz,"
  printAttitude(imu.ax, imu.ay, imu.az, -imu.my, -imu.mx, imu.mz); // Print "PIT,pitch,ROL,roll,HEA,heading,"
  // ToF Range Finder
  printAmbientLight();                                             // Print "LUX,ambientlight,"
  printProximity();                                                // Print "PRO,distance," 
  Serial.println();                                                // Print-line "\n"
  delay(250); // 1sec. delay
  
} // End of void loop

/*
 * Functions
 * - IMU
 *   - printGyro()
 *   - printAccel()
 *   - printMag()
 *   - printAttitude()
 * - ToF Range Finder
 *   - printIdentification()
 */


// IMU Functions
// The following version of printGyro() has been modified from the original SparkFun
// This version prints calculated gyroscope values automatically
void printGyro() {
  // Reading raw data from gyroscope
  imu.readGyro(); // (imu.gx, ...gy, ...gz) [deg/s] 
  // Now we can use the gx, gy, and gz variables as we please.
  // Either print them as raw ADC values, or calculated in DPS.
  Serial.print("GYR,");
  // Converting raw ADC values to DPS before printing
  Serial.print(imu.calcGyro(imu.gx), 2);
  Serial.print(",");
  Serial.print(imu.calcGyro(imu.gy), 2);
  Serial.print(",");
  Serial.print(imu.calcGyro(imu.gz), 2);
  Serial.print(",");
} // End of function - printGyro()


// The following version of printAccel() has been modified from the original SparkFun
// This version prints calculated accelerometer values automatically
void printAccel() {
  // Reading raw data from accelerometer
  imu.readAccel(); // (imu.ax, ...ay, ...az) [g]
  Serial.print("ACC,");
  // Converting ADC values to Gs before printing
  Serial.print(imu.calcAccel(imu.ax), 2);
  Serial.print(",");
  Serial.print(imu.calcAccel(imu.ay), 2);
  Serial.print(",");
  Serial.print(imu.calcAccel(imu.az), 2);
  Serial.print(",");
} // End of function - printAccel()

// The following version of printMag() has been modified from the original SparkFun
// This version prints calculated magnetometer values automatically
void printMag() {
  // Reading raw data from magnetometer
  imu.readMag(); // (imu.mx, ...my, ...mz) [gauss]
  Serial.print("MAG,");
  // Converting ADC values to Bs before printing
  Serial.print(imu.calcMag(imu.mx), 2);
  Serial.print(",");
  Serial.print(imu.calcMag(imu.my), 2);
  Serial.print(",");
  Serial.print(imu.calcMag(imu.mz), 2);
  Serial.print(",");
} // End of function - printMag()

// Calculate pitch, roll, and heading.
// Pitch/roll calculations take from this app note:
// http://cache.freescale.com/files/sensors/doc/app_note/AN3461.pdf?fpsp=1
// Heading calculations taken from this app note:
// http://www51.honeywell.com/aero/common/documents/myaerospacecatalog-documents/Defense_Brochures-documents/Magnetic__Literature_Application_notes-documents/AN203_Compass_Heading_Using_Magnetometers.pdf
void printAttitude(float ax, float ay, float az, float mx, float my, float mz) {
  float roll = atan2(ay, az);
  float pitch = atan2(-ax, sqrt(ay * ay + az * az));
  
  float heading;
  if (my == 0)
    heading = (mx < 0) ? 180.0 : 0;
  else
    heading = atan2(mx, my);
    
  heading -= DECLINATION * PI / 180;
  
  if (heading > PI) heading -= (2 * PI);
  else if (heading < -PI) heading += (2 * PI);
  else if (heading < 0) heading += 2 * PI;
  
  // Convert everything from radians to degrees:
  heading *= 180.0 / PI;
  pitch *= 180.0 / PI;
  roll  *= 180.0 / PI;
  
  Serial.print("PIT,");
  Serial.print(pitch, 2);
  Serial.print(",");
  Serial.print("ROL,");
  Serial.print(roll, 2);
  Serial.print(",");
  Serial.print("HEA,");
  Serial.print(heading, 2);
  Serial.print(",");
  
} // End of function - printAttitude()


// ToF Range Finder Functions
// All functions beow were developed by our group to follow the same protocol used by SparkFun on their IMU function library.
// These functions simplify the void loop process and make the development/editing process more efficient.
void printAmbientLight() {
  
  // Read raw ambient light level and report in LUX
  Serial.print("LUX,");
  //Input GAIN for light levels, 
  // GAIN_20     // Actual ALS Gain of 20
  // GAIN_10     // Actual ALS Gain of 10.32
  // GAIN_5      // Actual ALS Gain of 5.21
  // GAIN_2_5    // Actual ALS Gain of 2.60
  // GAIN_1_67   // Actual ALS Gain of 1.72
  // GAIN_1_25   // Actual ALS Gain of 1.28
  // GAIN_1      // Actual ALS Gain of 1.01
  // GAIN_40     // Actual ALS Gain of 40
  Serial.print(sensor.getAmbientLight(GAIN_1));
  Serial.print(",");

} // End of function - printAmbientLight()

void printProximity() {
  
  // Read raw proximity data and report in millimeters (mm)
  Serial.print("PRO,");
  Serial.print(sensor.getDistance());
  Serial.print(",");
  
} // End of function - printProximity()

void printIdentification(struct VL6180xIdentification *temp){
  Serial.print("Model ID = ");
  Serial.println(temp->idModel);

  Serial.print("Model Rev = ");
  Serial.print(temp->idModelRevMajor);
  Serial.print(".");
  Serial.println(temp->idModelRevMinor);

  Serial.print("Module Rev = ");
  Serial.print(temp->idModuleRevMajor);
  Serial.print(".");
  Serial.println(temp->idModuleRevMinor);  

  Serial.print("Manufacture Date = ");
  Serial.print((temp->idDate >> 3) & 0x001F);
  Serial.print("/");
  Serial.print((temp->idDate >> 8) & 0x000F);
  Serial.print("/1");
  Serial.print((temp->idDate >> 12) & 0x000F);
  Serial.print(" Phase: ");
  Serial.println(temp->idDate & 0x0007);

  Serial.print("Manufacture Time (s)= ");
  Serial.println(temp->idTime * 2);
  Serial.println();
  Serial.println();
}


