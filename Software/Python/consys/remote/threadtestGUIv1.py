from PyQt5 import QtCore, QtGui, QtWidgets
import time

class increment(QtCore.QThread):

    value = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(increment, self).__init__(parent)

    def run(self):
        self.state = 0
        while( True ):
            self.value.emit(self.state)
            time.sleep(0.5)
            self.state = self.state + 1
            print(self.state)


class GUI():

    def __init__(self, MainWindow):
        super(GUI, self).__init__()

        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(500, 700))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Raspi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("Raspi.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(QtCore.Qt.RightToLeft)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background: rgb(255, 255, 255);")

        self.verticalLayout = QtWidgets.QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName("verticalLayout")

        self.logoLayout = QtWidgets.QHBoxLayout()
        self.logoLayout.setObjectName("logoLayout")
        self.logo = QtWidgets.QLabel(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMinimumSize(QtCore.QSize(350, 160))
        self.logo.setMaximumSize(QtCore.QSize(350, 160))
        self.logo.setPixmap(QtGui.QPixmap("pd3d.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.logo.setObjectName("logo")
        self.logoLayout.addWidget(self.logo)
        self.verticalLayout.addLayout(self.logoLayout)

        self.shellout = QtWidgets.QLabel(MainWindow)
        self.shellout.setAlignment(QtCore.Qt.AlignCenter)
        self.shellout.setObjectName("shellout")
        self.verticalLayout.addWidget(self.shellout)

        self.shellout2 = QtWidgets.QLabel(MainWindow)
        self.shellout2.setAlignment(QtCore.Qt.AlignCenter)
        self.shellout2.setObjectName("shellout2")
        self.verticalLayout.addWidget(self.shellout2)

        self.startbtn = QtWidgets.QPushButton(MainWindow)
        self.startbtn.setObjectName("startbtn")
        self.verticalLayout.addWidget(self.startbtn)

        self.stopbtn = QtWidgets.QPushButton(MainWindow)
        self.stopbtn.setObjectName("stopbtn")
        self.verticalLayout.addWidget(self.stopbtn)

        self.quitbtn = QtWidgets.QPushButton(MainWindow)
        self.quitbtn.setObjectName("quitbtn")
        self.verticalLayout.addWidget(self.quitbtn)

        self.iniTranslate(MainWindow)

        self.thread = increment()
        self.thread.value.connect(self.count)

        self.quitbtn.clicked.connect(MainWindow.close)
        self.startbtn.clicked.connect(self.begincounting)

    def iniTranslate(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "PD3D Control Panel"))
        self.shellout.setText(_translate("MainWindow", "THREAD OUTPUT 1"))
        self.shellout2.setText(_translate("MainWindow", "THREAD OUTPUT 2"))
        self.startbtn.setText(_translate("MainWindow", "Start"))
        self.stopbtn.setText(_translate("MainWindow", "Stop"))
        self.quitbtn.setText(_translate("MainWindow", "Quit"))

    def begincounting(self):
        _translate = QtCore.QCoreApplication.translate

        if not self.thread.isRunning():
            self.shellout2.setText(_translate("MainWindow", "Beginning Thread!"))
            print("Beginning Thread!")
            self.thread.start()

    def count(self, val):
        _translate = QtCore.QCoreApplication.translate
        self.shellout.setText(_translate("MainWindow",  str(val)))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = GUI(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
