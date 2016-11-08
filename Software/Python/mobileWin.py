"""
mobile.py
"""

# Import Libraries and/or Modules
from Tkinter import *                                   # GUI design libraries
import ttk                                              # ...
from mobileFunctionsWin import findStethoscope


gui = Tk()                                              # Initialization of the window under object name "root"
gui.title("mobile.py")                                  # Title of the window
gui.geometry('450x450+200+200')                         # Window dimensions in pixels + the distance from the top-left corner of your screen

# Information Label
infoLabel = Label(text="SMART STETHOSCOPE")
infoLabel.place(x=10,y=10)

# Action Buttons
searchDevicesButton = Button(text="Find Stethoscope", command=findStethoscope)
searchDevicesButton.place(x=10,y=50)


gui.mainloop()

