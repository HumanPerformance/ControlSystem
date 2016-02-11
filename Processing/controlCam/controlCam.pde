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
  
  if (cam.available() == true) {
   cam.read();
  }
  pg.beginDraw();
  //pg.image(cam, 0, 0);
  pg.set(0, 0, cam);
  String imagePath = "pics/screen" + imageIndex + ".png";
  pg.save(imagePath);
  imageIndex = imageIndex + 1;
  pg.endDraw();
  // The following does the same, and is faster when just drawing the image
  // without any additional resizing, transformations, or tint.
  //pg.set(0, 0, cam);
  //saveFrame("pics/screen-#####.png");
  
} // End of void-draw loop

//void captureEvent(Capture c) {
  
//  c.read();
//  pg.beginDraw();
//  pg.image(cam, 0, 0);
//  pg.endDraw();
//  saveFrame("pics/screen-#####.png");
  
//} // End of captureEvent function 