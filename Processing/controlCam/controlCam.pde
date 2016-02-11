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
int camId = 0;
int imageIndex = 1;


 
void setup() {
  
  size(640, 480);
  pg = createGraphics(640, 480);
  
  String[] cameras = Capture.list();
  camId = 63;
  //printArray(cameras);
  //findCam(cameras, name, res, fps, camId);
  cam = new Capture(this, cameras[camId]);
  cam.start();
  
   
} // End of void-setup loop

void draw() {
  
  if (cam.available() == true) {
    
    // The program reads a frame from the camera
    cam.read();
    
   }
    
   // This function uses the defined PGraphics object to draw and save images without displaying on the main window/screen
   // Note that this method is significantly slower than using the main window --unknown reason
   pg.beginDraw(); // Begin creating the graphics
    
   pg.set(0, 0, cam); // Populate graphics with read camera frame
    
   String imagePath = "pics/screen" + imageIndex + ".png";
   pg.save(imagePath);
    
   pg.endDraw(); // End drawing on the graphics
    
  imageIndex = imageIndex + 1;
  
} // End of void-draw loop