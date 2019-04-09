from PyQt5 import QtCore, QtGui, QtWidgets
import sys, spur

class GUI(object):

    def setup(self, MainWindow):
        self.count = 0

        # Create the main window and set the geometry.
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 700)
        MainWindow.setMinimumSize(QtCore.QSize(500, 700))
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("background: rgb(255, 255, 255);")

        # Generate fancy Raspberry Pi icon for the window:
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Raspi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("Raspi.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)

        # Setting the primary layout for the window:
        self.verticalLayout = QtWidgets.QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName("verticalLayout")

        # Centering the logo widget in the window with a layout:
        self.logoLayout = QtWidgets.QHBoxLayout()
        self.logoLayout.setObjectName("logoLayout")

        # PD3D logo, build and placement:
        self.logo = QtWidgets.QLabel(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMinimumSize(QtCore.QSize(350, 160))
        self.logo.setMaximumSize(QtCore.QSize(350, 160))
        self.logo.setPixmap(QtGui.QPixmap("pd3d.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setObjectName("logo")
        self.logoLayout.addWidget(self.logo)
        self.verticalLayout.addLayout(self.logoLayout)

        # Generating the grid for the buttons and output labels:
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")

        # Separating the logo from the central grid:
        spacer1 = QtWidgets.QSpacerItem(692, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacer1, 0, 0, 1, 3)

        # "Connect to SSH" button, build and placement:
        self.connectBtn = QtWidgets.QPushButton(MainWindow)
        self.connectBtn.setCheckable(True)
        self.connectBtn.setMinimumSize(QtCore.QSize(100, 50))
        self.connectBtn.setObjectName("connectBtn")
        self.gridLayout.addWidget(self.connectBtn, 1, 0, 1, 1)

        # "Connection Status" label, build and placement:
        self.connectionOut = QtWidgets.QLabel(MainWindow)
        self.connectionOut.setMinimumSize(QtCore.QSize(0, 100))
        self.connectionOut.setAlignment(QtCore.Qt.AlignCenter)
        self.connectionOut.setIndent(0)
        self.connectionOut.setObjectName("connectionOut")
        self.gridLayout.addWidget(self.connectionOut, 1, 1, 1, 2)

        # Separating the first row of widgets from the rest:
        spacer2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacer2, 2, 0, 1, 3)

        # "Send Command" button, build and placement:
        self.sendBtn = QtWidgets.QPushButton(MainWindow)
        self.sendBtn.setMinimumSize(QtCore.QSize(100, 50))
        self.sendBtn.setObjectName("sendBtn")
        self.gridLayout.addWidget(self.sendBtn, 4, 0, 2, 1)

        # Output from SSH Unix Bash, build and placement:
        self.bashOut = QtWidgets.QLabel(MainWindow)
        self.bashOut.setMinimumSize(QtCore.QSize(0, 100))
        self.bashOut.setText("")
        self.bashOut.setAlignment(QtCore.Qt.AlignCenter)
        self.bashOut.setIndent(0)
        self.bashOut.setObjectName("bashOut")
        self.gridLayout.addWidget(self.bashOut, 4, 1, 2, 2)

        # Separating the second row of widgets from the rest:
        spacer3 = QtWidgets.QSpacerItem(379, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacer3, 6, 0, 1, 3)

        # "Quit the Program" button, build and placement:
        self.quitBtn = QtWidgets.QPushButton(MainWindow)
        self.quitBtn.setMinimumSize(QtCore.QSize(100, 100))
        self.quitBtn.setMaximumSize(QtCore.QSize(100, 100))
        power = QtGui.QIcon()
        power.addPixmap(QtGui.QPixmap("powerbutton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quitBtn.setIcon(power)
        self.quitBtn.setIconSize(QtCore.QSize(48, 48))
        self.quitBtn.setObjectName("quitBtn")
        self.gridLayout.addWidget(self.quitBtn, 9, 2, 1, 1)

        # "Hard Reboot of Pi" button, build and placement:
        self.rebootBtn = QtWidgets.QPushButton(MainWindow)
        self.rebootBtn.setMinimumSize(QtCore.QSize(100, 100))
        self.rebootBtn.setMaximumSize(QtCore.QSize(100, 100))
        self.rebootBtn.setIconSize(QtCore.QSize(32, 32))
        self.rebootBtn.setObjectName("rebootBtn")
        self.gridLayout.addWidget(self.rebootBtn, 9, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        # Route the setting of text in the window through automated translation:
        # (TO THE USER'S NATIVE LANGUAGE! :D)
        self.initTranslate(MainWindow)

        # Setup the signal and slot connections for buttons and output:
        self.quitBtn.clicked.connect(MainWindow.close)
        self.connectBtn.toggled['bool'].connect(self.tunnel)
        self.sendBtn.clicked.connect(self.send)

        self.rebootBtn.clicked.connect(self.reboot)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def initTranslate(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PD3D Control Panel"))
        self.sendBtn.setText(_translate("MainWindow", "Send Command"))
        self.connectionOut.setText(_translate("MainWindow", "Awaiting Connection (via SSH) ..."))
        self.connectBtn.setText(_translate("MainWindow", "Connect"))
        self.rebootBtn.setText(_translate("MainWindow", "Force Reboot"))

    def tunnel(self, on):
        _translate = QtCore.QCoreApplication.translate
        if (on):
            self.connectionOut.setText(_translate("MainWindow", "Connected!"))
        else:
            self.connectionOut.setText(_translate("MainWindow", "Disconnected!"))

    def send(self):
        _translate = QtCore.QCoreApplication.translate
        if (self.connectBtn.isChecked()):
            self.bashOut.setText(_translate("MainWindow", "Sending Command: 'ls'"))
        else:
            self.bashOut.setText(_translate("MainWindow", "Error: Not Connected!"))
    def reboot(self):
        _translate = QtCore.QCoreApplication.translate

        if (self.connectBtn.isChecked()):
            self.bashOut.setText(_translate("MainWindow", "Sending Command: 'sudo reboot'"))
            self.connectBtn.toggle()
        else:
            self.bashOut.setText(_translate("MainWindow", "Error: Not Connected!"))


def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = GUI()
    ui.setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

run()
