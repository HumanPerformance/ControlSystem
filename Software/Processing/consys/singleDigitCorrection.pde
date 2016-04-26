/* =====================================
 * Single Digit Correction
 *
 * This function was built with the purpose of adding 0s to the left of single digits.
 * This process is important for the sake of comparing strings.
 *
 * Fluvio L. Lobo Fenoglietto 01/29/2016
 ==================================== */

public String singleDigitCorrection(String prefix, int counter) {
  
  String outString = ""; // Definng output string
  
  if (counter < 10) {
    
    outString = prefix + "0" + Integer.toString(counter);
    
  } else if (counter >= 10) {
    
    outString = prefix + Integer.toString(counter);
    
  } // End of if-statement "Single digit input detection"
  
  return outString;
  
} // End of singleDigitCorrection function