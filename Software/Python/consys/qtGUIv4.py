from PyQt5 import QtCore, QtGui, QtWidgets
import paramiko as miko
import sys

class GUI(object):

    def setup(self, MainWindow):
        self.button = None

        # Create the main window and set the geometry.
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        MainWindow.setMinimumSize(QtCore.QSize(512, 768))
        MainWindow.setLayoutDirection(QtCore.Qt.RightToLeft)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background: rgb(255, 255, 255);")

        # Generate fancy Raspberry Pi icon for the window:
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Raspi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        # Setting the primary layout for the window:
        self.verticalLayout = QtWidgets.QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.primaryGrid = QtWidgets.QGridLayout()
        self.primaryGrid.setObjectName("primaryGrid")

        # Centering the logo widget in the window with a layout:
        self.logoLayout = QtWidgets.QHBoxLayout()
        self.logoLayout.setObjectName("logoLayout")
        self.logo = QtWidgets.QLabel(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)

        # PD3D logo, build and placement:
        self.logo.setMinimumSize(QtCore.QSize(350, 160))
        self.logo.setMaximumSize(QtCore.QSize(350, 160))
        self.logo.setPixmap(QtGui.QPixmap("pd3d.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setObjectName("logo")
        self.logoLayout.addWidget(self.logo)
        self.primaryGrid.addLayout(self.logoLayout, 0, 0, 1, 5)

        # Panel 1 button grid:
        self.gridP1 = QtWidgets.QGridLayout()
        self.gridP1.setSpacing(10)
        self.gridP1.setObjectName("gridP1")
        self.p1scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p1scene1.sizePolicy().hasHeightForWidth())
        self.p1scene1.setSizePolicy(sizePolicy)
        self.p1scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p1scene1.setObjectName("p1scene1")
        self.gridP1.addWidget(self.p1scene1, 3, 1, 1, 1)
        self.p1connect = QtWidgets.QPushButton(MainWindow)
        self.p1connect.setCheckable(True)
        self.p1connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p1connect.setObjectName("p1connect")
        self.gridP1.addWidget(self.p1connect, 2, 0, 1, 2)
        self.p1scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p1scene2.sizePolicy().hasHeightForWidth())
        self.p1scene2.setSizePolicy(sizePolicy)
        self.p1scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p1scene2.setObjectName("p1scene2")
        self.gridP1.addWidget(self.p1scene2, 3, 0, 1, 1)
        self.p1 = QtWidgets.QLabel(MainWindow)
        self.p1.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p1.setFont(font)
        self.p1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.p1.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p1.setAlignment(QtCore.Qt.AlignCenter)
        self.p1.setObjectName("p1")
        self.gridP1.addWidget(self.p1, 1, 0, 1, 2)
        self.primaryGrid.addLayout(self.gridP1, 2, 4, 1, 1)

        # Panel 2 button grid:
        self.gridP2 = QtWidgets.QGridLayout()
        self.gridP2.setSpacing(10)
        self.gridP2.setObjectName("gridP2")
        self.p2connect = QtWidgets.QPushButton(MainWindow)
        self.p2connect.setCheckable(True)
        self.p2connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p2connect.setObjectName("p2connect")
        self.gridP2.addWidget(self.p2connect, 2, 0, 1, 2)
        self.p2scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p2scene2.sizePolicy().hasHeightForWidth())
        self.p2scene2.setSizePolicy(sizePolicy)
        self.p2scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p2scene2.setObjectName("p2scene2")
        self.gridP2.addWidget(self.p2scene2, 3, 0, 1, 1)
        self.p2scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p2scene1.sizePolicy().hasHeightForWidth())
        self.p2scene1.setSizePolicy(sizePolicy)
        self.p2scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p2scene1.setObjectName("p2scene1")
        self.gridP2.addWidget(self.p2scene1, 3, 1, 1, 1)
        self.p2 = QtWidgets.QLabel(MainWindow)
        self.p2.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p2.setFont(font)
        self.p2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p2.setAlignment(QtCore.Qt.AlignCenter)
        self.p2.setObjectName("p2")
        self.gridP2.addWidget(self.p2, 1, 0, 1, 2)
        self.primaryGrid.addLayout(self.gridP2, 2, 3, 1, 1)

        # Panel 3 button grid:
        self.gridP3 = QtWidgets.QGridLayout()
        self.gridP3.setSpacing(10)
        self.gridP3.setObjectName("gridP3")
        self.p3connect = QtWidgets.QPushButton(MainWindow)
        self.p3connect.setCheckable(True)
        self.p3connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p3connect.setObjectName("p3connect")
        self.gridP3.addWidget(self.p3connect, 2, 0, 1, 2)
        self.p3 = QtWidgets.QLabel(MainWindow)
        self.p3.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p3.setFont(font)
        self.p3.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p3.setAlignment(QtCore.Qt.AlignCenter)
        self.p3.setObjectName("p3")
        self.gridP3.addWidget(self.p3, 1, 0, 1, 2)
        self.p3scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p3scene1.sizePolicy().hasHeightForWidth())
        self.p3scene1.setSizePolicy(sizePolicy)
        self.p3scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p3scene1.setObjectName("p3scene1")
        self.gridP3.addWidget(self.p3scene1, 3, 1, 1, 1)
        self.p3scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p3scene2.sizePolicy().hasHeightForWidth())
        self.p3scene2.setSizePolicy(sizePolicy)
        self.p3scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p3scene2.setObjectName("p3scene2")
        self.gridP3.addWidget(self.p3scene2, 3, 0, 1, 1)
        self.primaryGrid.addLayout(self.gridP3, 2, 2, 1, 1)

        # Panel 4 button grid:
        self.gridP4 = QtWidgets.QGridLayout()
        self.gridP4.setSpacing(10)
        self.gridP4.setObjectName("gridP4")
        self.p4 = QtWidgets.QLabel(MainWindow)
        self.p4.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p4.setFont(font)
        self.p4.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p4.setAlignment(QtCore.Qt.AlignCenter)
        self.p4.setObjectName("p4")
        self.gridP4.addWidget(self.p4, 1, 0, 1, 2)
        self.p4scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p4scene1.sizePolicy().hasHeightForWidth())
        self.p4scene1.setSizePolicy(sizePolicy)
        self.p4scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p4scene1.setObjectName("p4scene1")
        self.gridP4.addWidget(self.p4scene1, 4, 1, 1, 1)
        self.p4scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p4scene2.sizePolicy().hasHeightForWidth())
        self.p4scene2.setSizePolicy(sizePolicy)
        self.p4scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p4scene2.setObjectName("p4scene2")
        self.gridP4.addWidget(self.p4scene2, 4, 0, 1, 1)
        self.p4connect = QtWidgets.QPushButton(MainWindow)
        self.p4connect.setCheckable(True)
        self.p4connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p4connect.setObjectName("p4connect")
        self.gridP4.addWidget(self.p4connect, 3, 0, 1, 2)
        self.primaryGrid.addLayout(self.gridP4, 2, 1, 1, 1)

        # Panel 5 button grid:
        self.gridP5 = QtWidgets.QGridLayout()
        self.gridP5.setSpacing(10)
        self.gridP5.setObjectName("gridP5")
        self.p5connect = QtWidgets.QPushButton(MainWindow)
        self.p5connect.setCheckable(True)
        self.p5connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p5connect.setDefault(False)
        self.p5connect.setFlat(False)
        self.p5connect.setObjectName("p5connect")
        self.gridP5.addWidget(self.p5connect, 3, 0, 1, 2)
        self.p5scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p5scene1.sizePolicy().hasHeightForWidth())
        self.p5scene1.setSizePolicy(sizePolicy)
        self.p5scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p5scene1.setObjectName("p5scene1")
        self.gridP5.addWidget(self.p5scene1, 4, 1, 1, 1)
        self.p5 = QtWidgets.QLabel(MainWindow)
        self.p5.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p5.setFont(font)
        self.p5.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p5.setAlignment(QtCore.Qt.AlignCenter)
        self.p5.setObjectName("p5")
        self.gridP5.addWidget(self.p5, 2, 0, 1, 2)
        self.p5scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p5scene2.sizePolicy().hasHeightForWidth())
        self.p5scene2.setSizePolicy(sizePolicy)
        self.p5scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p5scene2.setObjectName("p5scene2")
        self.gridP5.addWidget(self.p5scene2, 4, 0, 1, 1)
        self.primaryGrid.addLayout(self.gridP5, 2, 0, 1, 1)

        # Line separation, for row 2 of the primaryGrid
        self.line = QtWidgets.QFrame(MainWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.primaryGrid.addWidget(self.line, 3, 0, 1, 5)
        self.verticalLayout.addLayout(self.primaryGrid)

        # Panel 6 button grid:
        self.gridP6 = QtWidgets.QGridLayout()
        self.gridP6.setSpacing(10)
        self.gridP6.setObjectName("gridP6")
        self.p6connect = QtWidgets.QPushButton(MainWindow)
        self.p6connect.setCheckable(True)
        self.p6connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p6connect.setObjectName("p6connect")
        self.gridP6.addWidget(self.p6connect, 2, 0, 1, 2)
        self.p6scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p6scene1.sizePolicy().hasHeightForWidth())
        self.p6scene1.setSizePolicy(sizePolicy)
        self.p6scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p6scene1.setObjectName("p6scene1")
        self.gridP6.addWidget(self.p6scene1, 3, 1, 1, 1)
        self.p6 = QtWidgets.QLabel(MainWindow)
        self.p6.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p6.setFont(font)
        self.p6.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p6.setAlignment(QtCore.Qt.AlignCenter)
        self.p6.setObjectName("p6")
        self.gridP6.addWidget(self.p6, 1, 0, 1, 2)
        self.p6scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p6scene2.sizePolicy().hasHeightForWidth())
        self.p6scene2.setSizePolicy(sizePolicy)
        self.p6scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p6scene2.setObjectName("p6scene2")
        self.gridP6.addWidget(self.p6scene2, 3, 0, 1, 1)
        self.primaryGrid.addLayout(self.gridP6, 4, 4, 1, 1)

        # Panel 7 button grid:
        self.gridP7 = QtWidgets.QGridLayout()
        self.gridP7.setSpacing(10)
        self.gridP7.setObjectName("gridP7")
        self.p7connect = QtWidgets.QPushButton(MainWindow)
        self.p7connect.setCheckable(True)
        self.p7connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p7connect.setObjectName("p7connect")
        self.gridP7.addWidget(self.p7connect, 2, 0, 1, 2)
        self.p7 = QtWidgets.QLabel(MainWindow)
        self.p7.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p7.setFont(font)
        self.p7.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p7.setAlignment(QtCore.Qt.AlignCenter)
        self.p7.setObjectName("p7")
        self.gridP7.addWidget(self.p7, 1, 0, 1, 2)
        self.p7scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p7scene1.sizePolicy().hasHeightForWidth())
        self.p7scene1.setSizePolicy(sizePolicy)
        self.p7scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p7scene1.setObjectName("p7scene1")
        self.gridP7.addWidget(self.p7scene1, 3, 1, 1, 1)
        self.p7scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p7scene2.sizePolicy().hasHeightForWidth())
        self.p7scene2.setSizePolicy(sizePolicy)
        self.p7scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p7scene2.setObjectName("p7scene2")
        self.gridP7.addWidget(self.p7scene2, 3, 0, 1, 1)
        self.primaryGrid.addLayout(self.gridP7, 4, 3, 1, 1)

        # Panel 8 button grid:
        self.gridP8 = QtWidgets.QGridLayout()
        self.gridP8.setSpacing(10)
        self.gridP8.setObjectName("gridP8")
        self.p8connect = QtWidgets.QPushButton(MainWindow)
        self.p8connect.setCheckable(True)
        self.p8connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p8connect.setObjectName("p8connect")
        self.gridP8.addWidget(self.p8connect, 2, 0, 1, 2)
        self.p8 = QtWidgets.QLabel(MainWindow)
        self.p8.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p8.setFont(font)
        self.p8.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p8.setAlignment(QtCore.Qt.AlignCenter)
        self.p8.setObjectName("p8")
        self.gridP8.addWidget(self.p8, 1, 0, 1, 2)
        self.p8scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p8scene1.sizePolicy().hasHeightForWidth())
        self.p8scene1.setSizePolicy(sizePolicy)
        self.p8scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p8scene1.setObjectName("p8scene1")
        self.gridP8.addWidget(self.p8scene1, 3, 1, 1, 1)
        self.p8scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p8scene2.sizePolicy().hasHeightForWidth())
        self.p8scene2.setSizePolicy(sizePolicy)
        self.p8scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p8scene2.setObjectName("p8scene2")
        self.gridP8.addWidget(self.p8scene2, 3, 0, 1, 1)
        self.primaryGrid.addLayout(self.gridP8, 4, 2, 1, 1)

        # Panel 9 button grid:
        self.gridP9 = QtWidgets.QGridLayout()
        self.gridP9.setSpacing(10)
        self.gridP9.setObjectName("gridP9")
        self.p9connect = QtWidgets.QPushButton(MainWindow)
        self.p9connect.setCheckable(True)
        self.p9connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p9connect.setObjectName("p9connect")
        self.gridP9.addWidget(self.p9connect, 2, 0, 1, 2)
        self.p9 = QtWidgets.QLabel(MainWindow)
        self.p9.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p9.setFont(font)
        self.p9.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p9.setAlignment(QtCore.Qt.AlignCenter)
        self.p9.setObjectName("p9")
        self.gridP9.addWidget(self.p9, 1, 0, 1, 2)
        self.p9scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p9scene1.sizePolicy().hasHeightForWidth())
        self.p9scene1.setSizePolicy(sizePolicy)
        self.p9scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p9scene1.setObjectName("p9scene1")
        self.gridP9.addWidget(self.p9scene1, 3, 1, 1, 1)
        self.p9scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p9scene2.sizePolicy().hasHeightForWidth())
        self.p9scene2.setSizePolicy(sizePolicy)
        self.p9scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p9scene2.setObjectName("p9scene2")
        self.gridP9.addWidget(self.p9scene2, 3, 0, 1, 1)
        self.primaryGrid.addLayout(self.gridP9, 4, 1, 1, 1)

        # Panel 10 button grid:
        self.gridP10 = QtWidgets.QGridLayout()
        self.gridP10.setSpacing(10)
        self.gridP10.setObjectName("gridP10")
        self.p10connect = QtWidgets.QPushButton(MainWindow)
        self.p10connect.setCheckable(True)
        self.p10connect.setMinimumSize(QtCore.QSize(50, 25))
        self.p10connect.setObjectName("p10connect")
        self.gridP10.addWidget(self.p10connect, 2, 0, 1, 2)
        self.p10 = QtWidgets.QLabel(MainWindow)
        self.p10.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.p10.setFont(font)
        self.p10.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p10.setAlignment(QtCore.Qt.AlignCenter)
        self.p10.setObjectName("p10")
        self.gridP10.addWidget(self.p10, 1, 0, 1, 2)
        self.p10scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p10scene1.sizePolicy().hasHeightForWidth())
        self.p10scene1.setSizePolicy(sizePolicy)
        self.p10scene1.setMinimumSize(QtCore.QSize(25, 25))
        self.p10scene1.setObjectName("p10scene1")
        self.gridP10.addWidget(self.p10scene1, 3, 1, 1, 1)
        self.p10scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p10scene2.sizePolicy().hasHeightForWidth())
        self.p10scene2.setSizePolicy(sizePolicy)
        self.p10scene2.setMinimumSize(QtCore.QSize(25, 25))
        self.p10scene2.setObjectName("p10scene2")
        self.gridP10.addWidget(self.p10scene2, 3, 0, 1, 1)
        self.primaryGrid.addLayout(self.gridP10, 4, 0, 1, 1)

        # "Quit the Program" button, build and placement:
        self.quitBtn = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHeightForWidth(self.quitBtn.sizePolicy().hasHeightForWidth())
        self.quitBtn.setSizePolicy(sizePolicy)
        self.quitBtn.setMinimumSize(QtCore.QSize(100, 100))
        self.quitBtn.setMaximumSize(QtCore.QSize(100, 100))
        self.quitBtn.setLayoutDirection(QtCore.Qt.RightToLeft)
        quit = QtGui.QIcon()
        quit.addPixmap(QtGui.QPixmap("powerbutton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quitBtn.setIcon(quit)
        self.quitBtn.setIconSize(QtCore.QSize(48, 48))
        self.quitBtn.setCheckable(False)
        self.quitBtn.setAutoDefault(False)
        self.quitBtn.setDefault(False)
        self.quitBtn.setFlat(False)
        self.quitBtn.setObjectName("quitBtn")
        self.verticalLayout.addWidget(self.quitBtn)

        # Route the setting of text in the window through automated translation:
        # (TO THE USER'S NATIVE LANGUAGE! :D)
        self.iniTranslate(MainWindow)

        # Defining what the buttons do:
        self.quitBtn.clicked.connect(MainWindow.close)
        self.p1connect.clicked.connect(self.p1set)
        self.p2connect.clicked.connect(self.p2set)
        self.p3connect.clicked.connect(self.p3set)
        self.p4connect.clicked.connect(self.tunnel, 4)
        self.p5connect.clicked.connect(self.tunnel, 5)
        self.p6connect.clicked.connect(self.tunnel, 6)
        self.p7connect.clicked.connect(self.tunnel, 7)
        self.p8connect.clicked.connect(self.tunnel, 8)
        self.p9connect.clicked.connect(self.tunnel, 9)
        self.p10connect.clicked.connect(self.tunnel, 10)

    def iniTranslate(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PD3D Control Panel"))

        self.p1scene1.setText(_translate("MainWindow", "S1"))
        self.p1connect.setText(_translate("MainWindow", "Connect"))
        self.p1scene2.setText(_translate("MainWindow", "S2"))
        self.p1.setText(_translate("MainWindow", "Panel 1"))

        self.p2connect.setText(_translate("MainWindow", "Connect"))
        self.p2scene2.setText(_translate("MainWindow", "S2"))
        self.p2scene1.setText(_translate("MainWindow", "S1"))
        self.p2.setText(_translate("MainWindow", "Panel 2"))

        self.p3connect.setText(_translate("MainWindow", "Connect"))
        self.p3.setText(_translate("MainWindow", "Panel 3"))
        self.p3scene1.setText(_translate("MainWindow", "S1"))
        self.p3scene2.setText(_translate("MainWindow", "S2"))

        self.p4.setText(_translate("MainWindow", "Panel 4"))
        self.p4scene1.setText(_translate("MainWindow", "S1"))
        self.p4scene2.setText(_translate("MainWindow", "S2"))
        self.p4connect.setText(_translate("MainWindow", "Connect"))

        self.p5connect.setText(_translate("MainWindow", "Connect"))
        self.p5scene1.setText(_translate("MainWindow", "S1"))
        self.p5.setText(_translate("MainWindow", "Panel 5"))
        self.p5scene2.setText(_translate("MainWindow", "S2"))

        self.p6connect.setText(_translate("MainWindow", "Connect"))
        self.p6scene1.setText(_translate("MainWindow", "S1"))
        self.p6.setText(_translate("MainWindow", "Panel 6"))
        self.p6scene2.setText(_translate("MainWindow", "S2"))

        self.p7connect.setText(_translate("MainWindow", "Connect"))
        self.p7.setText(_translate("MainWindow", "Panel 7"))
        self.p7scene1.setText(_translate("MainWindow", "S1"))
        self.p7scene2.setText(_translate("MainWindow", "S2"))

        self.p8connect.setText(_translate("MainWindow", "Connect"))
        self.p8.setText(_translate("MainWindow", "Panel 8"))
        self.p8scene1.setText(_translate("MainWindow", "S1"))
        self.p8scene2.setText(_translate("MainWindow", "S2"))

        self.p9connect.setText(_translate("MainWindow", "Connect"))
        self.p9.setText(_translate("MainWindow", "Panel 9"))
        self.p9scene1.setText(_translate("MainWindow", "S1"))
        self.p9scene2.setText(_translate("MainWindow", "S2"))

        self.p10connect.setText(_translate("MainWindow", "Connect"))
        self.p10.setText(_translate("MainWindow", "Panel 10"))
        self.p10scene1.setText(_translate("MainWindow", "S1"))
        self.p10scene2.setText(_translate("MainWindow", "S2"))

    def p1set(self, state):
        print(state)
        self.button = 1
        print("Test")
        self.tunnel()

    def p2set(self, state):
        self.button = 2
        self.tunnel()

    def p3set(self, state):
        self.button = 3
        self.tunnel()

    def tunnel(self):
        _translate = QtCore.QCoreApplication.translate
        print(self.button)

        if self.button == 1:
            SSH_ADDRESS = "10.171.190.201"
            SSH_USERNAME = "pi"
            SSH_PASSWORD = "raspberry"
            SSH_COMMAND = "sudo python pd3d/csec/repos/ControlSystem/Software/Python/consys/printme.py"

            ssh = miko.SSHClient()
            ssh.set_missing_host_key_policy(miko.AutoAddPolicy())

            ssh_stdin = ssh_stdout = ssh_stderr = None
            try:
                ssh.connect(SSH_ADDRESS, username=SSH_USERNAME, password=SSH_PASSWORD)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(SSH_COMMAND)

            except Exception as e:
                sys.stderr.write("SSH connection error: {0}".format(e))

            if ssh_stdout:
                output =  ssh_stdout.read()
                if (output == b'bruh\n'):
                    self.p1.setText(_translate("MainWindow", "FLUVIO"))
                    print("P1 Text Set")

        if self.button == 2:
            SSH_ADDRESS = "10.171.190.201"
            SSH_USERNAME = "pi"
            SSH_PASSWORD = "raspberry"
            SSH_COMMAND = "sudo python pd3d/csec/repos/ControlSystem/Software/Python/consys/printme.py"

            ssh = miko.SSHClient()
            ssh.set_missing_host_key_policy(miko.AutoAddPolicy())

            ssh_stdin = ssh_stdout = ssh_stderr = None
            try:
                ssh.connect(SSH_ADDRESS, username=SSH_USERNAME, password=SSH_PASSWORD)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(SSH_COMMAND)

            except Exception as e:
                sys.stderr.write("SSH connection error: {0}".format(e))

            if ssh_stdout:
                output =  ssh_stdout.read()
                if (output == b'bruh\n'):
                    self.p2.setText(_translate("MainWindow", "IS"))
                    print("P2 Text Set")

        if self.button == 3:
            SSH_ADDRESS = "10.171.190.201"
            SSH_USERNAME = "pi"
            SSH_PASSWORD = "raspberry"
            SSH_COMMAND = "sudo python pd3d/csec/repos/ControlSystem/Software/Python/consys/printme.py"

            ssh = miko.SSHClient()
            ssh.set_missing_host_key_policy(miko.AutoAddPolicy())

            ssh_stdin = ssh_stdout = ssh_stderr = None
            try:
                ssh.connect(SSH_ADDRESS, username=SSH_USERNAME, password=SSH_PASSWORD)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(SSH_COMMAND)

            except Exception as e:
                sys.stderr.write("SSH connection error: {0}".format(e))

            if ssh_stdout:
                output =  ssh_stdout.read()
                if (output == b'bruh\n'):
                    self.p3.setText(_translate("MainWindow", "LAME"))





def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = GUI()
    ui.setup(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

run()
