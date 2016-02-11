/* =====================================
 * Connect to Camera
 *
 * This function was designed to connect 
 * to a desired camera
 *
 * Fluvio L. Lobo Fenoglietto 02/11/2016
 ==================================== */
 
public void connect2Cam(String[] cameras, int camId) {
  
  cam = new Capture(this, cameras[camId]);
  cam.start();
   
} // End of connect2Cam function