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


// Camera Variables
String name = "name=/dev/video0";
String res = "size=640x480";
String fps = "fps=30";
int imageIndex = 1;


 
void setup() {
  
  size(640, 480);
  pg = createGraphics(640, 480);
  
  String[] cameras = Capture.list();
  //camId = 63;
  //printArray(cameras);
  int camId = findCam(cameras, name, res, fps);
  connect2Cam(cameras, camId);
  
   
} // End of void-setup loop

void draw() {
  
  grabFrame(pg, cam, imageIndex);
  imageIndex = imageIndex + 1;
  
} // End of void-draw loop