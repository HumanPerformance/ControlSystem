/* =====================================
 * Control Camera
 *
 * This function was designed to detect,
 * connect, and control a usb-web camera
 *
 * Fluvio L. Lobo Fenoglietto 02/11/2016
 ==================================== */
 
import processing.video.*;

PGraphics pg;
Capture cam;

int imageIndex = 1;

 
void setup() {
  
  size(640, 480);
  pg = createGraphics(640, 480);
  
  String[] cameras = Capture.list();
  int Ncameras = cameras.length;
  //printArray(cameras);
  
  cam = new Capture(this, cameras[58]);
  cam.start();
  
  
   
} // End of void-setup loop

void draw() {
  
  grabFrame(pg, cam, imageIndex);
  
  // Update indeces
  imageIndex = imageIndex + 1;
  
} // End of void-draw loop