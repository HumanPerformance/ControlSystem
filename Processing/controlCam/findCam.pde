/* =====================================
 * Find Camera
 *
 * This function was designed to detect
 * a desired camera
 *
 * Fluvio L. Lobo Fenoglietto 02/11/2016
 ==================================== */
 
public void findCam(String[] cameras, String name, String res, String fps, int camId) {
  
  int Ncameras = cameras.length;
  // printArray(cameras);
  
  if (Ncameras == 0) {
    
    println("ERRORx001 :: No cameras found, please check connection");
    
  } else if (Ncameras > 0) {
    
    for (int i = 0; i < Ncameras; i ++) {
      
      // First, the program needs to process the string located in the capture-list
      // These strings are a composite of name, resolution, and frame rate
      // The information has been comma-delimited
      String[] connectedCamInfo = split(cameras[i], ',');
    
      // Second, the program uses the decomposed information of the detected cameras to find a match with the input information
      // Starting with matching the name...
      if (connectedCamInfo[0].equals(name)) {
        
        // println("Camera match");
        
        // Followed by matching the resolution...
        if (connectedCamInfo[1].equals(res)) {
          
          // println("Resolution match");
          
          // And finishing with a match on the frame rate...
          if (connectedCamInfo[2].equals(fps)) {
            
            println("Camera found");
            camId = i;
            break;
            
          } // End of if-statement "frame rate match"
          
        } // End of if-statement "resolution match"
        
      } // End of if-statement "name match"

    } // End of for-loop
    
  } // End of if-statement
   
} // End of function findCam