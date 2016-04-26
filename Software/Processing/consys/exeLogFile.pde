/* =====================================
 * Execution Log File
 *
 * This function was built with the purpose of creating and updating an execution log file
 * An execution log file consist of a text file containing the iteration and time the consys.pde program was executed
 *
 * Fluvio L. Lobo Fenoglietto 01/31/2016
 ==================================== */

public void exeLogFile(String exeLogFilePath) {
  
  //// First, the program generates the path for the execution file
  //// In the process, the program generates a directory using the CPU date
  //String timeStampFolder = timeStamp("dated-folder");
  //String logFile = "ExecutionLog.txt";
  //String exeLogFilePath = "data/output/" + timeStampFolder + "/" + logFile;
  
  // Here, the program reads such directory looking for the execution log
  // This, of course, may fail if the file has not been created
  String[] logFileLines = loadStrings(exeLogFilePath);
  
  // Conditional statement around the existence of the execution log
  if (logFileLines == null) {
    
    // In the case the file does not exist, the program creates one.
    createOutput(exeLogFilePath); // Generating execution log file
    
    // The initial strings are a combination of headers and the first execution time
    String[] outString = {"", ""};
    outString[0] = "Execution Log for consys.pde";
    String exeTimeStamp = timeStamp("clock");
    outString[1] = "1, " + exeTimeStamp;
    saveStrings(exeLogFilePath, outString);
    
  } else {
    
    // In the case the filke exists, the code must read he lines in order to find where to print the next stamp
    int Nlines = logFileLines.length;
    String[] outString = new String[Nlines+1];
    
    // If the file exists, the program must reprint the previous strings plus the new stamp. The following for loop ensures that.
    for (int i = 0; i <= Nlines; i++) {
      
      if (i < Nlines) {
        
        outString[i] = logFileLines[i];
        
      } else if (i == Nlines) {

        String exeTimeStamp = timeStamp("clock");
        outString[i] = Integer.toString(Nlines) + ", " + exeTimeStamp;
        saveStrings(exeLogFilePath, outString);
        
      } // End of if-statement

    } // End of for-loop
    
  } // End of if-statement
  
} // End of exeLogFile function