/*
 * readConfigFile.pde
 *
 * The following function was created to read data, in the form of strings, from a configuration or input file.
 * The configuration file is written and stored within the data folder by a separate program.
 *
 * Fluvio L. Lobo Fenoglietto 05/19/2016
 */
 
 public void readConfigFile() {
   
   // Read Configuration File Data
   configInfo = loadStrings(configFile);
   printArray(configInfo);
   
   int Nlines = configInfo.length;
   String[] splitString;
   for (int i = 0; i < Nlines; i ++) {
     
     splitString = split(configInfo[i],':');
     
     switch(splitString[0]) {
       
       case "StartTime":
       
         testTimeMinutes = int(splitString[splitString.length-1]);
         countDownMinutes = testTimeMinutes;
         println("Test Time : " + testTimeMinutes);
         println("Countdown Time : " + countDownMinutes);
     
      case "WarningTime":
      
        testTimeWarning = int(splitString[splitString.length-1]);
         println("Warning Time : " + testTimeWarning);
       
     } // End of switch statement - conditional around the content of the configuration file
   } // End of for loop - strings loaded from configuration file
 } // End of function - readConfigFile