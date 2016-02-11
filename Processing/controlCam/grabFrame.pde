/* =====================================
 * Grab Frame
 *
 * This function was designed to capture
 * and save a single frame obtained from
 * a connected device
 *
 * Fluvio L. Lobo Fenoglietto 02/11/2016
 ==================================== */
 
public void grabFrame(PGraphics pg, Capture cam, int imageIndex) {
  
  if (cam.available() == true) {
    
    // The program reads a frame from the camera
    cam.read();
    
    // This function uses the defined PGraphics object to draw and save images without displaying on the main window/screen
    // Note that this method is significantly slower than using the main window --unknown reason
    pg.beginDraw(); // Begin creating the graphics
    
    pg.set(0, 0, cam); // Populate graphics with read camera frame
    
    String imagePath = "pics/screen" + imageIndex + ".png";
    pg.save(imagePath);
    
    pg.endDraw(); // End drawing on the graphics
    
  } // End of if-statement "Camera Availability Check"
  
} // End of grabFrame function