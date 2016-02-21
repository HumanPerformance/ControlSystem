/* =====================================
 * Wait Clock
 *
 * The following function creates/draw an analog clock on the current display.
 * The clock uses the CPU time (hour, minutes, seconds).
 *
 * This code has been adapted from a Processing example (https://processing.org/examples/clock.html)
 *
 * Fluvio L. Lobo Fenoglietto 02/19/2016
 ==================================== */

public void waitClock() {
  
  // Variable Definition
  int cx, cy;
  float secondsRadius;
  float minutesRadius;
  float hoursRadius;
  float clockDiameter;
  
  int radius = min(width, height) / 2;
  secondsRadius = radius * 0.72;
  minutesRadius = radius * 0.60;
  hoursRadius = radius * 0.50;
  clockDiameter = radius * 1.8;
  
  cx = width / 2;
  cy = height / 2;
  
  // Draw the clock background
  fill(0,0,0);
  noStroke();
  ellipse(cx, cy, clockDiameter, clockDiameter);
  
  // Angles for sin() and cos() start at 3 o'clock;
  // subtract HALF_PI to make them start at the top
  float s = map(second(), 0, 60, 0, TWO_PI) - HALF_PI;
  float m = map(minute() + norm(second(), 0, 60), 0, 60, 0, TWO_PI) - HALF_PI; 
  float h = map(hour() + norm(minute(), 0, 60), 0, 24, 0, TWO_PI * 2) - HALF_PI;
  
  // Draw the hands of the clock
  stroke(255);
  strokeWeight(1);
  line(cx, cy, cx + cos(s) * secondsRadius, cy + sin(s) * secondsRadius);
  strokeWeight(2);
  line(cx, cy, cx + cos(m) * minutesRadius, cy + sin(m) * minutesRadius);
  strokeWeight(4);
  line(cx, cy, cx + cos(h) * hoursRadius, cy + sin(h) * hoursRadius);
  
  // Draw the minute ticks
  strokeWeight(2);
  beginShape(POINTS);
  for (int a = 0; a < 360; a+=6) {
    float angle = radians(a);
    float x = cx + cos(angle) * secondsRadius;
    float y = cy + sin(angle) * secondsRadius;
    
    textSize(24);
    fill(255,255,255);
    if (a == 0) {  
      text("3", x+5, y-2.5);
    } else if (a == 90) {
      text("6", x, y+5);
    } else if (a == 180) {
      text("9", x-5, y-2.5);
    } else if (a == 270) {
      text("12", x, y-10);
    } else {
      vertex(x, y);
    }
    textAlign(CENTER, CENTER);
  }
  endShape();
  
} // End of waitClock function