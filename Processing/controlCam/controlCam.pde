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
  
  //if (cam.available() == true) {
  //  cam.read();
  //}
  ////image(cam, 0, 0);
  //// The following does the same, and is faster when just drawing the image
  //// without any additional resizing, transformations, or tint.
  //// set(0, 0, cam);
  //saveFrame();
  
} // End of void-draw loop

void captureEvent(Capture c) {
  
  c.read();
  set(0, 0, pg);
  saveFrame("pics/screen-#####.png");
  
} // End of captureEvent function 