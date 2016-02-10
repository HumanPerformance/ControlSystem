/* =====================================
 * User Info Path
 *
 * This function creates the directory associated with the input user id
 * The program also saves text file with information regarding the scenario selected
 *
 * Fluvio L. Lobo Fenoglietto 02/09/2016
 ==================================== */
 
public void userInfoFileMA(int Nardus) {
  
  for (int h = 0; h < Nardus; h ++) {
    
    // First, the button generates the new path
    String userInfoFolder = "data/output/" + timeStampFolder + "/" + configInfo[1] + "/";
    String userInfoFilename = "Info.txt";
    String userInfoPath = userInfoFolder + userInfoFilename;
   
    // Path to data output file --Arduino and other sensor data
    String arduName = "ardu" + Integer.toString(h);
    String dataTimeStamp = timeStamp("timed-filename");
    String dataFilename = arduName + "-" + dataTimeStamp + ".txt";
    String dataFilePath = userInfoFolder + dataFilename;
  
    // The program creates the output file
    createOutput(userInfoPath);
    dataFile[h] = createWriter(dataFilePath);
   
    // The program writes information to the Info file
    String[] outString = new String[4];
    String timeStamp = timeStamp("clock");
    outString[0] = "User Input Summary (Info.txt)";
    outString[1] = "User ID = " + configInfo[1];
    outString[2] = "Scenario = " + configInfo[2];
    outString[3] = "Execution Time = " + timeStamp;
   
    // Write strings to file
    saveStrings(userInfoPath, outString);
   
  } // End of for-loop "Arduinos Loop"
   
} // End of userInfoFile function