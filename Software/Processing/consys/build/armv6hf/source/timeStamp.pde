/* =====================================
 * Time Stamp
 *
 * The following function was designed to simplify the need for specifying the time-stamp throughout the code.
 * Additionally, the function corrects for single digit values.
 * 
 * The function takes the input "style" (String), which may be either:
 *     > "calendar" outputs date in the format "mm/dd/yyyy hh:mm:ss"
 *     > "clock" outputs time in the format "hh:mm:ss"
 *
 * Fluvio L. Lobo Fenoglietto 01/28/2016
 ==================================== */
 
public String timeStamp(String style) {
  
  // Variables
  // Input Variables --Processing functions
  int mm = month();
  int dd = day();
  int hh = hour();
  int mi = minute();
  int ss = second();
  
  // Internal Variables
  String month;
  String day;
  String year = Integer.toString(year()); // Does not require correction
  String hour;
  String minute;
  String second;
  
  // Output Variables --To be returned by the function
  String timeStamp = "";
 
  // Correct for single digits
  String prefix = "";
  month = singleDigitCorrection(prefix, mm);
  day = singleDigitCorrection(prefix, dd);
  hour = singleDigitCorrection(prefix, hh);
  minute = singleDigitCorrection(prefix, mi);
  second = singleDigitCorrection(prefix, ss);
  
  // Conditional statement for output type (calendar vs. clock)
  switch (style) {
    
    case "calendar":    
      timeStamp = month + "/" + day + "/" + year + " " + hour + ":" + minute + ":" + second;
      break;      
    case "clock":    
      timeStamp = hour + ":" + minute + ":" + second;
      break;      
    case "dated-folder":    
      timeStamp = month + day + year;
      break;      
    case "timed-filename":
      timeStamp = month + day + year + "-" + hour + minute + second;
      break;
      
  } // End of switch
    
  return timeStamp;
  
} // End of timeStamp function