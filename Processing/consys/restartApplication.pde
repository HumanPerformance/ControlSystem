


public void restartApplication() {
  
  // When pressed, the button recovers the hidden buttons and labels taken down by clearWindow()
  
  
  cp5.get(Button.class,"exitApplication").setVisible(true); // Exit Button
  cp5.get(Textlabel.class,"studentIDLabel").setVisible(true); // Student ID Label/Title
  
  cp5.get(Textfield.class,"userID").setVisible(true); // User ID input
  
  cp5.get(Textlabel.class,"currentInput").setText("Enter SP ID and press Enter/Return");
  cp5.get(Textlabel.class,"currentInput").setVisible(true); // Current user input
  
  cp5.get(Button.class,"confirmSelection").setVisible(false);
  cp5.get(Button.class,"confirmSelection").setColorCaptionLabel(black);
  cp5.get(Button.class,"confirmSelection").setColorBackground(gold);
  cp5.get(Button.class,"confirmSelection").setColorForeground(gray);
  
} // End of restartApplication function