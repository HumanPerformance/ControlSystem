from PyQt5 import QtCore, QtGui, QtWidgets
import paramiko as miko
import sys

'''
To the purveyor of this program:
Prepare yourself, poor soul. I cannot explain the suffering, the torment and the frustration that has been wrought here.
Surely, since you are here, there is more to come. If there is anything I can do to alleviate your burden, feel free to summon me.
The least I can do is help those who come after me, to navigate this endless, needlessly convoluted, and extravagantly hideous labyrinth.
Feel free to criticize and shame, for this is likely to be the worst thing you've ever seen.

To self:
You did this to yourself.
Welcome to Hell.
'''

# --------------------------
class TUNNEL(QtCore.QThread):
    '''
    Open an SSH terminal at the address specified and send the command specified.
    Within the context of a QThread

    INPUTS:
        - ADDR: The IP address of the SSH server to access. (String)
        - CMD: The single command, in the proper format, that is to be executed. (String)

    OUTPUT:
        - output: Reading from the socket's stdout, or else an error message.  (String)
    '''
    output = QtCore.pyqtSignal(str)

    # ----------------------
    def __init__(self):
        super(TUNNEL, self).__init__()
        self.usr  = "pi"
        self.pwrd = "raspberry"

        self.ssh = miko.SSHClient()
        self.ssh.set_missing_host_key_policy(miko.AutoAddPolicy())
        self.ssh_stdin  = None
        self.ssh_stdout = None
        self.ssh_stderr = None

    def direct(self, CMD, ADDR):
        self.cmd  = CMD
        self.addr = ADDR

    # ----------------------
    def run(self):

        try:
            self.ssh.connect(self.addr, username= self.usr, password= self.pwrd)
            self.ssh_stdin, self.ssh_stdout, self.ssh_stderr = self.ssh.exec_command(self.cmd)

        except Exception as e:
            sys.stderr.write("SSH connection error: {0}".format(e))
            self.output.emit("ERR: SSH")

        if self.ssh_stdout:
            output =  self.ssh_stdout.read()
            self.output.emit( str(output) )

        else:
            self.output.emit("ERR: NULL")

# --------------------------
class MONITOR(QtCore.QThread):
    '''
    Constantly review "PANEL_STATUS" array.
    Check the enumerated conditions and emit actionable signals when necessary.

    INPUTS:
        - PANEL_STATUS array of outputs. IT MUST BE DEFINED FIRST.

    OUTPUT:
        - connected[i]: When the control system (CONSYS) and the blood pressure cuff (BPC) in panel [i] both observe "AOK"

    '''
    connection1  = QtCore.pyqtSignal(bool)
    connection2  = QtCore.pyqtSignal(bool)
    connection3  = QtCore.pyqtSignal(bool)
    connection4  = QtCore.pyqtSignal(bool)
    connection5  = QtCore.pyqtSignal(bool)
    connection6  = QtCore.pyqtSignal(bool)
    connection7  = QtCore.pyqtSignal(bool)
    connection8  = QtCore.pyqtSignal(bool)
    connection9  = QtCore.pyqtSignal(bool)
    connection10 = QtCore.pyqtSignal(bool)

    # ----------------------
    def __init__(self, PANEL_STATUS):
        super(MONITOR, self).__init__()
        self.updatepanel = {"p1"  : False,
                            "p2"  : False,
                            "p3"  : False,
                            "p4"  : False,
                            "p5"  : False,
                            "p6"  : False,
                            "p7"  : False,
                            "p8"  : False,
                            "p9"  : False,
                            "p10" : False }

    # ----------------------
    def run(self):
        while(True):
            if self.updatepanel["p1"]:
                if (PANEL_STATUS[0][0] == "AOK" and PANEL_STATUS[0][1] == "AOK"):
                    self.connection1.emit( True )
                elif (PANEL_STATUS[0][0] == "ERR" and PANEL_STATUS[0][1] == "AOK"):
                    self.connection1.emit( False )
                elif (PANEL_STATUS[0][0] == "AOK" and PANEL_STATUS[0][1] == "ERR"):
                    self.connection1.emit( False )
                print("Panel Status 1: " + str(PANEL_STATUS[0]) )
                self.updatepanel["p1"] = False

            elif self.updatepanel["p2"]:
                if (PANEL_STATUS[1][0] == "AOK" and PANEL_STATUS[1][1] == "AOK"):
                    self.connection2.emit( True )
                elif (PANEL_STATUS[1][0] == "ERR" and PANEL_STATUS[1][1] == "AOK"):
                    self.connection2.emit( False )
                elif (PANEL_STATUS[1][0] == "AOK" and PANEL_STATUS[1][1] == "ERR"):
                    self.connection2.emit( False )
                print("Panel Status 2: " + str(PANEL_STATUS[1]) )
                self.updatepanel["p2"] = False

            elif self.updatepanel["p3"]:
                if (PANEL_STATUS[2][0] == "AOK" and PANEL_STATUS[2][1] == "AOK"):
                    self.connection3.emit( True )
                elif (PANEL_STATUS[2][0] == "ERR" and PANEL_STATUS[2][1] == "AOK"):
                    self.connection3.emit( False )
                elif (PANEL_STATUS[2][0] == "AOK" and PANEL_STATUS[2][1] == "ERR"):
                    self.connection3.emit( False )
                print("Panel Status 3: " + str(PANEL_STATUS[2]) )
                self.updatepanel["p3"] = False

            elif self.updatepanel["p4"]:
                if (PANEL_STATUS[3][0] == "AOK" and PANEL_STATUS[3][1] == "AOK"):
                    self.connection4.emit( True )
                elif (PANEL_STATUS[3][0] == "ERR" and PANEL_STATUS[3][1] == "AOK"):
                    self.connection4.emit( False )
                elif (PANEL_STATUS[3][0] == "AOK" and PANEL_STATUS[3][1] == "ERR"):
                    self.connection4.emit( False )
                print("Panel Status 4: " + str(PANEL_STATUS[3]) )
                self.updatepanel["p4"] = False

            elif self.updatepanel["p5"]:
                if (PANEL_STATUS[4][0] == "AOK" and PANEL_STATUS[4][1] == "AOK"):
                    self.connection5.emit( True )
                elif (PANEL_STATUS[4][0] == "ERR" and PANEL_STATUS[4][1] == "AOK"):
                    self.connection5.emit( False )
                elif (PANEL_STATUS[4][0] == "AOK" and PANEL_STATUS[4][1] == "ERR"):
                    self.connection5.emit( False )
                print("Panel Status 5: " + str(PANEL_STATUS[4]) )
                self.updatepanel["p5"] = False

            elif self.updatepanel["p6"]:
                if (PANEL_STATUS[5][0] == "AOK" and PANEL_STATUS[5][1] == "AOK"):
                    self.connection6.emit( True )
                elif (PANEL_STATUS[5][0] == "ERR" and PANEL_STATUS[5][1] == "AOK"):
                    self.connection6.emit( False )
                elif (PANEL_STATUS[5][0] == "AOK" and PANEL_STATUS[5][1] == "ERR"):
                    self.connection6.emit( False )
                print("Panel Status 6: " + str(PANEL_STATUS[5]) )
                self.updatepanel["p6"] = False

            elif self.updatepanel["p7"]:
                if (PANEL_STATUS[6][0] == "AOK" and PANEL_STATUS[6][1] == "AOK"):
                    self.connection7.emit( True )
                elif (PANEL_STATUS[6][0] == "ERR" and PANEL_STATUS[6][1] == "AOK"):
                    self.connection7.emit( False )
                elif (PANEL_STATUS[6][0] == "AOK" and PANEL_STATUS[6][1] == "ERR"):
                    self.connection7.emit( False )
                print("Panel Status 7: " + str(PANEL_STATUS[6]) )
                self.updatepanel["p7"] = False

            elif self.updatepanel["p8"]:
                if (PANEL_STATUS[7][0] == "AOK" and PANEL_STATUS[7][1] == "AOK"):
                    self.connection8.emit( True )
                elif (PANEL_STATUS[7][0] == "ERR" and PANEL_STATUS[7][1] == "AOK"):
                    self.connection8.emit( False )
                elif (PANEL_STATUS[7][0] == "AOK" and PANEL_STATUS[7][1] == "ERR"):
                    self.connection8.emit( False )
                print("Panel Status 8: " + str(PANEL_STATUS[7]) )
                self.updatepanel["p8"] = False

            elif self.updatepanel["p9"]:
                if (PANEL_STATUS[8][0] == "AOK" and PANEL_STATUS[8][1] == "AOK"):
                    self.connection9.emit( True )
                elif (PANEL_STATUS[8][0] == "ERR" and PANEL_STATUS[8][1] == "AOK"):
                    self.connection9.emit( False )
                elif (PANEL_STATUS[8][0] == "AOK" and PANEL_STATUS[8][1] == "ERR"):
                    self.connection9.emit( False )
                print("Panel Status 9: " + str(PANEL_STATUS[8]) )
                self.updatepanel["p9"] = False

            elif self.updatepanel["p10"]:
                if (PANEL_STATUS[9][0] == "AOK" and PANEL_STATUS[9][1] == "AOK"):
                    self.connection10.emit( True )
                elif (PANEL_STATUS[9][0] == "ERR" and PANEL_STATUS[9][1] == "AOK"):
                    self.connection10.emit( False )
                elif (PANEL_STATUS[9][0] == "AOK" and PANEL_STATUS[9][1] == "ERR"):
                    self.connection10.emit( False )
                print("Panel Status 10: " + str(PANEL_STATUS[9]) )
                self.updatepanel["p10"] = False

    # ----------------------
    def update(self, input):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        if (input == "p1"):
            self.updatepanel["p1"] = True
        if (input == "p2"):
            self.updatepanel["p2"] = True
        if (input == "p3"):
            self.updatepanel["p3"] = True
        if (input == "p4"):
            self.updatepanel["p4"] = True
        if (input == "p5"):
            self.updatepanel["p5"] = True
        if (input == "p6"):
            self.updatepanel["p6"] = True
        if (input == "p7"):
            self.updatepanel["p7"] = True
        if (input == "p8"):
            self.updatepanel["p8"] = True
        if (input == "p9"):
            self.updatepanel["p9"] = True
        if (input == "p10"):
            self.updatepanel["p10"] = True
        self.mutex.unlock()

# --------------------------
class GUI(object):

    # --------------------------
    def __init__(self, MainWindow):
        # --------------------------
        # Create the main window and set the geometry.
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        MainWindow.setMinimumSize(QtCore.QSize(800, 800))
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

        font = QtGui.QFont()
        #font.setFamily("Sitka Banner")
        font.setFamily("Yu Gothic")
        font.setBold(True)
        font.setPointSize(24)

        initBtnfont = QtGui.QFont()
        initBtnfont.setFamily("Yu Gothic")
        initBtnfont.setPointSize(13)
        initBtnfont.setBold(True)

        # Centering the logo widget in the window with a layout:
        self.logoLayout = QtWidgets.QHBoxLayout()
        self.logoLayout.setObjectName("logoLayout")

        # --------------------------
        # "Control All" buttons, build and placement:
        self.gridAll = QtWidgets.QVBoxLayout()
        self.gridAll.setContentsMargins(50, 0, 0, 0)
        self.gridAll.setSpacing(5)
        self.gridAll.setObjectName("gridAll")

        self.connectAll = QtWidgets.QPushButton(MainWindow)
        self.connectAll.setMaximumSize(QtCore.QSize(16777215, 50))
        self.connectAll.setFont(initBtnfont)
        self.connectAll.setObjectName("connectAll")
        self.gridAll.addWidget(self.connectAll)

        self.scene1All = QtWidgets.QPushButton(MainWindow)
        self.scene1All.setMaximumSize(QtCore.QSize(16777215, 50))
        self.scene1All.setSizeIncrement(QtCore.QSize(0, 0))
        self.scene1All.setFont(initBtnfont)
        self.scene1All.setObjectName("scene1All")
        self.gridAll.addWidget(self.scene1All)

        self.scene2All = QtWidgets.QPushButton(MainWindow)
        self.scene2All.setMaximumSize(QtCore.QSize(16777215, 50))
        self.scene2All.setFont(initBtnfont)
        self.scene2All.setObjectName("scene2All")
        self.gridAll.addWidget(self.scene2All)

        self.fetchAll = QtWidgets.QPushButton(MainWindow)
        self.fetchAll.setMaximumSize(QtCore.QSize(16777215, 50))
        self.fetchAll.setFont(initBtnfont)
        self.fetchAll.setObjectName("fetchAll")
        self.gridAll.addWidget(self.fetchAll)
        self.logoLayout.addLayout(self.gridAll)

        # --------------------------
        # PD3D Logo, build and placement:
        self.logoLabel = QtWidgets.QLabel(MainWindow)
        self.logoLabel.setMinimumSize(QtCore.QSize(350, 160))
        self.logoLabel.setMaximumSize(QtCore.QSize(350, 160))
        self.logoLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.logoLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap("pd3d.png"))
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.logoLabel.setObjectName("logoLabel")
        self.logoLayout.addWidget(self.logoLabel)
        self.primaryGrid.addLayout(self.logoLayout, 0, 0, 1, 5)
        self.verticalLayout.addLayout(self.primaryGrid)

        # --------------------------
        # Panel 1 button grid:
        self.gridP1 = QtWidgets.QGridLayout()
        self.gridP1.setSpacing(10)
        self.gridP1.setObjectName("gridP1")

        self.p1 = QtWidgets.QLabel(MainWindow)
        self.p1.setMinimumSize(QtCore.QSize(50, 50))
        self.p1.setFont(font)
        self.p1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.p1.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p1.setAlignment(QtCore.Qt.AlignCenter)
        self.p1.setObjectName("p1")
        self.gridP1.addWidget(self.p1, 1, 0, 1, 2)

        self.p1connect = QtWidgets.QPushButton(MainWindow)
        self.p1connect.setCheckable(True)
        self.p1connect.setFont(initBtnfont)
        self.p1connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p1connect.setObjectName("p1connect")
        self.gridP1.addWidget(self.p1connect, 2, 0, 1, 2)

        self.p1scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p1scene1.sizePolicy().hasHeightForWidth())
        self.p1scene1.setSizePolicy(sizePolicy)
        self.p1scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p1scene1.setObjectName("p1scene1")
        self.p1scene1.setFont(initBtnfont)
        self.p1scene1.setEnabled(False)
        self.gridP1.addWidget(self.p1scene1, 3, 1, 1, 1)

        self.p1scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p1scene2.sizePolicy().hasHeightForWidth())
        self.p1scene2.setSizePolicy(sizePolicy)
        self.p1scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p1scene2.setObjectName("p1scene2")
        self.p1scene2.setFont(initBtnfont)
        self.p1scene2.setEnabled(False)
        self.gridP1.addWidget(self.p1scene2, 3, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP1, 2, 4, 1, 1)

        # --------------------------
        # Panel 2 button grid:
        self.gridP2 = QtWidgets.QGridLayout()
        self.gridP2.setSpacing(10)
        self.gridP2.setObjectName("gridP2")

        self.p2 = QtWidgets.QLabel(MainWindow)
        self.p2.setMinimumSize(QtCore.QSize(50, 50))
        self.p2.setFont(font)
        self.p2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p2.setAlignment(QtCore.Qt.AlignCenter)
        self.p2.setObjectName("p2")
        self.gridP2.addWidget(self.p2, 1, 0, 1, 2)

        self.p2connect = QtWidgets.QPushButton(MainWindow)
        self.p2connect.setCheckable(True)
        self.p2connect.setFont(initBtnfont)
        self.p2connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p2connect.setObjectName("p2connect")
        self.gridP2.addWidget(self.p2connect, 2, 0, 1, 2)

        self.p2scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p2scene1.sizePolicy().hasHeightForWidth())
        self.p2scene1.setSizePolicy(sizePolicy)
        self.p2scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p2scene1.setObjectName("p2scene1")
        self.p2scene1.setFont(initBtnfont)
        self.p2scene1.setEnabled(False)
        self.gridP2.addWidget(self.p2scene1, 3, 1, 1, 1)

        self.p2scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p2scene2.sizePolicy().hasHeightForWidth())
        self.p2scene2.setSizePolicy(sizePolicy)
        self.p2scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p2scene2.setObjectName("p2scene2")
        self.p2scene2.setFont(initBtnfont)
        self.p2scene2.setEnabled(False)
        self.gridP2.addWidget(self.p2scene2, 3, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP2, 2, 3, 1, 1)

        # --------------------------
        # Panel 3 button grid:
        self.gridP3 = QtWidgets.QGridLayout()
        self.gridP3.setSpacing(10)
        self.gridP3.setObjectName("gridP3")

        self.p3 = QtWidgets.QLabel(MainWindow)
        self.p3.setMinimumSize(QtCore.QSize(50, 50))
        self.p3.setFont(font)
        self.p3.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p3.setAlignment(QtCore.Qt.AlignCenter)
        self.p3.setObjectName("p3")
        self.gridP3.addWidget(self.p3, 1, 0, 1, 2)

        self.p3connect = QtWidgets.QPushButton(MainWindow)
        self.p3connect.setCheckable(True)
        self.p3connect.setFont(initBtnfont)
        self.p3connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p3connect.setObjectName("p3connect")
        self.gridP3.addWidget(self.p3connect, 2, 0, 1, 2)

        self.p3scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p3scene1.sizePolicy().hasHeightForWidth())
        self.p3scene1.setSizePolicy(sizePolicy)
        self.p3scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p3scene1.setObjectName("p3scene1")
        self.p3scene1.setFont(initBtnfont)
        self.p3scene1.setEnabled(False)
        self.gridP3.addWidget(self.p3scene1, 3, 1, 1, 1)

        self.p3scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p3scene2.sizePolicy().hasHeightForWidth())
        self.p3scene2.setSizePolicy(sizePolicy)
        self.p3scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p3scene2.setObjectName("p3scene2")
        self.p3scene2.setFont(initBtnfont)
        self.p3scene2.setEnabled(False)
        self.gridP3.addWidget(self.p3scene2, 3, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP3, 2, 2, 1, 1)

        # --------------------------
        # Panel 4 button grid:
        self.gridP4 = QtWidgets.QGridLayout()
        self.gridP4.setSpacing(10)
        self.gridP4.setObjectName("gridP4")

        self.p4 = QtWidgets.QLabel(MainWindow)
        self.p4.setMinimumSize(QtCore.QSize(50, 50))
        self.p4.setFont(font)
        self.p4.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p4.setAlignment(QtCore.Qt.AlignCenter)
        self.p4.setObjectName("p4")
        self.gridP4.addWidget(self.p4, 1, 0, 1, 2)

        self.p4connect = QtWidgets.QPushButton(MainWindow)
        self.p4connect.setCheckable(True)
        self.p4connect.setFont(initBtnfont)
        self.p4connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p4connect.setObjectName("p4connect")
        self.gridP4.addWidget(self.p4connect, 3, 0, 1, 2)

        self.p4scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p4scene1.sizePolicy().hasHeightForWidth())
        self.p4scene1.setSizePolicy(sizePolicy)
        self.p4scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p4scene1.setObjectName("p4scene1")
        self.p4scene1.setFont(initBtnfont)
        self.p4scene1.setEnabled(False)
        self.gridP4.addWidget(self.p4scene1, 4, 1, 1, 1)

        self.p4scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p4scene2.sizePolicy().hasHeightForWidth())
        self.p4scene2.setSizePolicy(sizePolicy)
        self.p4scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p4scene2.setObjectName("p4scene2")
        self.p4scene2.setFont(initBtnfont)
        self.p4scene2.setEnabled(False)
        self.gridP4.addWidget(self.p4scene2, 4, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP4, 2, 1, 1, 1)

        # --------------------------
        # Panel 5 button grid:
        self.gridP5 = QtWidgets.QGridLayout()
        self.gridP5.setSpacing(10)
        self.gridP5.setObjectName("gridP5")

        self.p5 = QtWidgets.QLabel(MainWindow)
        self.p5.setMinimumSize(QtCore.QSize(50, 50))
        self.p5.setFont(font)
        self.p5.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p5.setAlignment(QtCore.Qt.AlignCenter)
        self.p5.setObjectName("p5")
        self.gridP5.addWidget(self.p5, 2, 0, 1, 2)

        self.p5connect = QtWidgets.QPushButton(MainWindow)
        self.p5connect.setCheckable(True)
        self.p5connect.setFont(initBtnfont)
        self.p5connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p5connect.setDefault(False)
        self.p5connect.setFlat(False)
        self.p5connect.setObjectName("p5connect")
        self.gridP5.addWidget(self.p5connect, 3, 0, 1, 2)

        self.p5scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p5scene1.sizePolicy().hasHeightForWidth())
        self.p5scene1.setSizePolicy(sizePolicy)
        self.p5scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p5scene1.setObjectName("p5scene1")
        self.p5scene1.setFont(initBtnfont)
        self.p5scene1.setEnabled(False)
        self.gridP5.addWidget(self.p5scene1, 4, 1, 1, 1)

        self.p5scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p5scene2.sizePolicy().hasHeightForWidth())
        self.p5scene2.setSizePolicy(sizePolicy)
        self.p5scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p5scene2.setObjectName("p5scene2")
        self.p5scene2.setFont(initBtnfont)
        self.p5scene2.setEnabled(False)
        self.gridP5.addWidget(self.p5scene2, 4, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP5, 2, 0, 1, 1)

        # # --------------------------
        # # Line separation, for row 2 of the primaryGrid
        # self.line = QtWidgets.QFrame(MainWindow)
        # self.line.setFrameShape(QtWidgets.QFrame.HLine)
        # self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.line.setObjectName("line")
        # self.primaryGrid.addWidget(self.line, 3, 0, 1, 5)
        # self.verticalLayout.addLayout(self.primaryGrid)

        # --------------------------
        # Panel 6 button grid:
        self.gridP6 = QtWidgets.QGridLayout()
        self.gridP6.setSpacing(10)
        self.gridP6.setObjectName("gridP6")

        self.p6 = QtWidgets.QLabel(MainWindow)
        self.p6.setMinimumSize(QtCore.QSize(50, 50))
        self.p6.setFont(font)
        self.p6.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p6.setAlignment(QtCore.Qt.AlignCenter)
        self.p6.setObjectName("p6")
        self.gridP6.addWidget(self.p6, 1, 0, 1, 2)

        self.p6connect = QtWidgets.QPushButton(MainWindow)
        self.p6connect.setCheckable(True)
        self.p6connect.setFont(initBtnfont)
        self.p6connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p6connect.setObjectName("p6connect")
        self.gridP6.addWidget(self.p6connect, 2, 0, 1, 2)

        self.p6scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p6scene1.sizePolicy().hasHeightForWidth())
        self.p6scene1.setSizePolicy(sizePolicy)
        self.p6scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p6scene1.setObjectName("p6scene1")
        self.p6scene1.setFont(initBtnfont)
        self.p6scene1.setEnabled(False)
        self.gridP6.addWidget(self.p6scene1, 3, 1, 1, 1)

        self.p6scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p6scene2.sizePolicy().hasHeightForWidth())
        self.p6scene2.setSizePolicy(sizePolicy)
        self.p6scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p6scene2.setObjectName("p6scene2")
        self.p6scene2.setFont(initBtnfont)
        self.p6scene2.setEnabled(False)
        self.gridP6.addWidget(self.p6scene2, 3, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP6, 4, 4, 1, 1)

        # --------------------------
        # Panel 7 button grid:
        self.gridP7 = QtWidgets.QGridLayout()
        self.gridP7.setSpacing(10)
        self.gridP7.setObjectName("gridP7")

        self.p7 = QtWidgets.QLabel(MainWindow)
        self.p7.setMinimumSize(QtCore.QSize(50, 50))
        self.p7.setFont(font)
        self.p7.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p7.setAlignment(QtCore.Qt.AlignCenter)
        self.p7.setObjectName("p7")
        self.gridP7.addWidget(self.p7, 1, 0, 1, 2)

        self.p7connect = QtWidgets.QPushButton(MainWindow)
        self.p7connect.setCheckable(True)
        self.p7connect.setFont(initBtnfont)
        self.p7connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p7connect.setObjectName("p7connect")
        self.gridP7.addWidget(self.p7connect, 2, 0, 1, 2)

        self.p7scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p7scene1.sizePolicy().hasHeightForWidth())
        self.p7scene1.setSizePolicy(sizePolicy)
        self.p7scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p7scene1.setObjectName("p7scene1")
        self.p7scene1.setFont(initBtnfont)
        self.p7scene1.setEnabled(False)
        self.gridP7.addWidget(self.p7scene1, 3, 1, 1, 1)

        self.p7scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p7scene2.sizePolicy().hasHeightForWidth())
        self.p7scene2.setSizePolicy(sizePolicy)
        self.p7scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p7scene2.setObjectName("p7scene2")
        self.p7scene2.setFont(initBtnfont)
        self.p7scene2.setEnabled(False)
        self.gridP7.addWidget(self.p7scene2, 3, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP7, 4, 3, 1, 1)

        # --------------------------
        # Panel 8 button grid:
        self.gridP8 = QtWidgets.QGridLayout()
        self.gridP8.setSpacing(10)
        self.gridP8.setObjectName("gridP8")

        self.p8 = QtWidgets.QLabel(MainWindow)
        self.p8.setMinimumSize(QtCore.QSize(50, 50))
        self.p8.setFont(font)
        self.p8.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p8.setAlignment(QtCore.Qt.AlignCenter)
        self.p8.setObjectName("p8")
        self.gridP8.addWidget(self.p8, 1, 0, 1, 2)

        self.p8connect = QtWidgets.QPushButton(MainWindow)
        self.p8connect.setCheckable(True)
        self.p8connect.setFont(initBtnfont)
        self.p8connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p8connect.setObjectName("p8connect")
        self.gridP8.addWidget(self.p8connect, 2, 0, 1, 2)

        self.p8scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p8scene1.sizePolicy().hasHeightForWidth())
        self.p8scene1.setSizePolicy(sizePolicy)
        self.p8scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p8scene1.setObjectName("p8scene1")
        self.p8scene1.setFont(initBtnfont)
        self.p8scene1.setEnabled(False)
        self.gridP8.addWidget(self.p8scene1, 3, 1, 1, 1)

        self.p8scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p8scene2.sizePolicy().hasHeightForWidth())
        self.p8scene2.setSizePolicy(sizePolicy)
        self.p8scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p8scene2.setObjectName("p8scene2")
        self.p8scene2.setFont(initBtnfont)
        self.p8scene2.setEnabled(False)
        self.gridP8.addWidget(self.p8scene2, 3, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP8, 4, 2, 1, 1)

        # --------------------------
        # Panel 9 button grid:
        self.gridP9 = QtWidgets.QGridLayout()
        self.gridP9.setSpacing(10)
        self.gridP9.setObjectName("gridP9")

        self.p9 = QtWidgets.QLabel(MainWindow)
        self.p9.setMinimumSize(QtCore.QSize(50, 50))
        self.p9.setFont(font)
        self.p9.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p9.setAlignment(QtCore.Qt.AlignCenter)
        self.p9.setObjectName("p9")
        self.gridP9.addWidget(self.p9, 1, 0, 1, 2)

        self.p9connect = QtWidgets.QPushButton(MainWindow)
        self.p9connect.setCheckable(True)
        self.p9connect.setFont(initBtnfont)
        self.p9connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p9connect.setObjectName("p9connect")
        self.gridP9.addWidget(self.p9connect, 2, 0, 1, 2)

        self.p9scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p9scene1.sizePolicy().hasHeightForWidth())
        self.p9scene1.setSizePolicy(sizePolicy)
        self.p9scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p9scene1.setObjectName("p9scene1")
        self.p9scene1.setFont(initBtnfont)
        self.p9scene1.setEnabled(False)
        self.gridP9.addWidget(self.p9scene1, 3, 1, 1, 1)

        self.p9scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p9scene2.sizePolicy().hasHeightForWidth())
        self.p9scene2.setSizePolicy(sizePolicy)
        self.p9scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p9scene2.setObjectName("p9scene2")
        self.p9scene2.setFont(initBtnfont)
        self.p9scene2.setEnabled(False)
        self.gridP9.addWidget(self.p9scene2, 3, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP9, 4, 1, 1, 1)

        # --------------------------
        # Panel 10 button grid:
        self.gridP10 = QtWidgets.QGridLayout()
        self.gridP10.setSpacing(10)
        self.gridP10.setObjectName("gridP10")

        self.p10 = QtWidgets.QLabel(MainWindow)
        self.p10.setMinimumSize(QtCore.QSize(50, 50))
        self.p10.setFont(font)
        self.p10.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.p10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.p10.setAlignment(QtCore.Qt.AlignCenter)
        self.p10.setObjectName("p10")
        self.gridP10.addWidget(self.p10, 1, 0, 1, 2)

        self.p10connect = QtWidgets.QPushButton(MainWindow)
        self.p10connect.setCheckable(True)
        self.p10connect.setFont(initBtnfont)
        self.p10connect.setMinimumSize(QtCore.QSize(50, 50))
        self.p10connect.setObjectName("p10connect")
        self.gridP10.addWidget(self.p10connect, 2, 0, 1, 2)

        self.p10scene1 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p10scene1.sizePolicy().hasHeightForWidth())
        self.p10scene1.setSizePolicy(sizePolicy)
        self.p10scene1.setMinimumSize(QtCore.QSize(25, 50))
        self.p10scene1.setObjectName("p10scene1")
        self.p10scene1.setFont(initBtnfont)
        self.p10scene1.setEnabled(False)
        self.gridP10.addWidget(self.p10scene1, 3, 1, 1, 1)

        self.p10scene2 = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.p10scene2.sizePolicy().hasHeightForWidth())
        self.p10scene2.setSizePolicy(sizePolicy)
        self.p10scene2.setMinimumSize(QtCore.QSize(25, 50))
        self.p10scene2.setObjectName("p10scene2")
        self.p10scene2.setFont(initBtnfont)
        self.p10scene2.setEnabled(False)
        self.gridP10.addWidget(self.p10scene2, 3, 0, 1, 1)

        self.primaryGrid.addLayout(self.gridP10, 4, 0, 1, 1)

        # --------------------------
        # Initiate and connect the Status Monitor:
        self.monitor = MONITOR(PANEL_STATUS)
        self.monitor.connection1.connect(self.connected1)
        self.monitor.connection2.connect(self.connected2)
        self.monitor.connection3.connect(self.connected3)
        self.monitor.connection4.connect(self.connected4)
        self.monitor.connection5.connect(self.connected5)
        self.monitor.connection6.connect(self.connected6)
        self.monitor.connection7.connect(self.connected7)
        self.monitor.connection8.connect(self.connected8)
        self.monitor.connection9.connect(self.connected9)
        self.monitor.connection10.connect(self.connected10)
        self.monitor.start()

        # --------------------------
        # "Quit the Program" button, build and placement:
        self.quitBtn = QtWidgets.QPushButton(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHeightForWidth(self.quitBtn.sizePolicy().hasHeightForWidth())
        self.quitBtn.setSizePolicy(sizePolicy)
        self.quitBtn.setMinimumSize(QtCore.QSize(100, 75))
        self.quitBtn.setMaximumSize(QtCore.QSize(16777215, 75))
        self.quitBtn.setLayoutDirection(QtCore.Qt.RightToLeft)
        quit = QtGui.QIcon()
        quit.addPixmap(QtGui.QPixmap("powerbutton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quitBtn.setIcon(quit)
        self.quitBtn.setIconSize(QtCore.QSize(48, 48))
        self.quitBtn.setAutoDefault(False)
        self.quitBtn.setDefault(False)
        self.quitBtn.setFlat(False)
        self.quitBtn.setObjectName("quitBtn")
        self.verticalLayout.addWidget(self.quitBtn)

        # --------------------------
        # "Additional Options" button, build and placement:
        self.toolButton = QtWidgets.QToolButton(MainWindow)
        self.toolButton.setSizePolicy(sizePolicy)
        self.toolButton.setMinimumSize(QtCore.QSize(100, 0))
        self.toolButton.setMaximumSize(QtCore.QSize(16777215, 25))
        self.toolButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButton.setFont(initBtnfont)
        self.toolButton.setAutoRaise(False)
        self.toolButton.setObjectName("toolButton")
        self.verticalLayout.addWidget(self.toolButton)

        self.menu = QtWidgets.QMenu("Options")
        self.menu.addAction("(Empty)")
        self.menu.addAction("(Empty)")
        self.menu.addSeparator()
        self.menu.addAction("(Empty)")
        self.menu.addAction("(Empty)")
        self.menu.addAction("(Empty)")
        self.menu.addAction("(Empty)")
        self.menu.addAction("(Empty)")
        self.toolButton.setMenu(self.menu)

        # Route the setting of text in the window through automated translation:
        # (TO THE USER'S NATIVE LANGUAGE! :D)
        self.iniTranslate(MainWindow)

        # --------------------------
        # Defining what the buttons do:
        self.quitBtn.clicked.connect(MainWindow.close)
        self.p1connect.clicked.connect(self.statuscheck_1)
        self.p2connect.clicked.connect(self.statuscheck_2)
        self.p3connect.clicked.connect(self.statuscheck_3)
        self.p4connect.clicked.connect(self.statuscheck_4)
        self.p5connect.clicked.connect(self.statuscheck_5)
        self.p6connect.clicked.connect(self.statuscheck_6)
        self.p7connect.clicked.connect(self.statuscheck_7)
        self.p8connect.clicked.connect(self.statuscheck_8)
        self.p9connect.clicked.connect(self.statuscheck_9)
        self.p10connect.clicked.connect(self.statuscheck_10)

        self.p1scene1.clicked.connect(lambda: self.p1scene(1))
        self.p1scene2.clicked.connect(lambda: self.p1scene(2))
        self.p2scene1.clicked.connect(lambda: self.p2scene(1))
        self.p2scene2.clicked.connect(lambda: self.p2scene(2))
        self.p3scene1.clicked.connect(lambda: self.p3scene(1))
        self.p3scene2.clicked.connect(lambda: self.p3scene(2))
        self.p4scene1.clicked.connect(lambda: self.p4scene(1))
        self.p4scene2.clicked.connect(lambda: self.p4scene(2))
        self.p5scene1.clicked.connect(lambda: self.p5scene(1))
        self.p5scene2.clicked.connect(lambda: self.p5scene(2))
        self.p6scene1.clicked.connect(lambda: self.p6scene(1))
        self.p6scene2.clicked.connect(lambda: self.p6scene(2))
        self.p7scene1.clicked.connect(lambda: self.p7scene(1))
        self.p7scene2.clicked.connect(lambda: self.p7scene(2))
        self.p8scene1.clicked.connect(lambda: self.p8scene(1))
        self.p8scene2.clicked.connect(lambda: self.p8scene(2))
        self.p9scene1.clicked.connect(lambda: self.p9scene(1))
        self.p9scene2.clicked.connect(lambda: self.p9scene(2))
        self.p10scene1.clicked.connect(lambda: self.p10scene(1))
        self.p10scene2.clicked.connect(lambda: self.p10scene(2))

    # --------------------------
    def iniTranslate(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PD3D Control Panel"))

        self.p1.setText(_translate("MainWindow", "Panel 1"))
        self.p1connect.setText(_translate("MainWindow", "Connect"))
        self.p1scene1.setText(_translate("MainWindow", "S1"))
        self.p1scene2.setText(_translate("MainWindow", "S2"))

        self.p2.setText(_translate("MainWindow", "Panel 2"))
        self.p2connect.setText(_translate("MainWindow", "Connect"))
        self.p2scene1.setText(_translate("MainWindow", "S1"))
        self.p2scene2.setText(_translate("MainWindow", "S2"))

        self.p3.setText(_translate("MainWindow", "Panel 3"))
        self.p3connect.setText(_translate("MainWindow", "Connect"))
        self.p3scene1.setText(_translate("MainWindow", "S1"))
        self.p3scene2.setText(_translate("MainWindow", "S2"))

        self.p4.setText(_translate("MainWindow", "Panel 4"))
        self.p4scene1.setText(_translate("MainWindow", "S1"))
        self.p4scene2.setText(_translate("MainWindow", "S2"))
        self.p4connect.setText(_translate("MainWindow", "Connect"))

        self.p5.setText(_translate("MainWindow", "Panel 5"))
        self.p5connect.setText(_translate("MainWindow", "Connect"))
        self.p5scene1.setText(_translate("MainWindow", "S1"))
        self.p5scene2.setText(_translate("MainWindow", "S2"))

        self.p6.setText(_translate("MainWindow", "Panel 6"))
        self.p6connect.setText(_translate("MainWindow", "Connect"))
        self.p6scene1.setText(_translate("MainWindow", "S1"))
        self.p6scene2.setText(_translate("MainWindow", "S2"))

        self.p7.setText(_translate("MainWindow", "Panel 7"))
        self.p7connect.setText(_translate("MainWindow", "Connect"))
        self.p7scene1.setText(_translate("MainWindow", "S1"))
        self.p7scene2.setText(_translate("MainWindow", "S2"))

        self.p8.setText(_translate("MainWindow", "Panel 8"))
        self.p8connect.setText(_translate("MainWindow", "Connect"))
        self.p8scene1.setText(_translate("MainWindow", "S1"))
        self.p8scene2.setText(_translate("MainWindow", "S2"))

        self.p9.setText(_translate("MainWindow", "Panel 9"))
        self.p9connect.setText(_translate("MainWindow", "Connect"))
        self.p9scene1.setText(_translate("MainWindow", "S1"))
        self.p9scene2.setText(_translate("MainWindow", "S2"))

        self.p10.setText(_translate("MainWindow", "Panel 10"))
        self.p10connect.setText(_translate("MainWindow", "Connect"))
        self.p10scene1.setText(_translate("MainWindow", "S1"))
        self.p10scene2.setText(_translate("MainWindow", "S2"))

        self.connectAll.setText(_translate("MainWindow", "Connect All"))
        self.scene1All.setText(_translate("MainWindow", "Scene 1"))
        self.scene2All.setText(_translate("MainWindow", "Scene 2"))
        self.fetchAll.setText(_translate("MainWindow", "Fetch All"))
        self.toolButton.setText(_translate("MainWindow", "Options"))

    # --------------------------
    def statuscheck_1(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS1 = TUNNEL()
            self.checkCONSYS1.direct(PANEL_COMMAND["status"], PANEL_IP["pi1"])
            #self.checkCONSYS1.direct(PANEL_COMMAND["test"], PANEL_IP["pi1"])
            self.checkCONSYS1.output.connect(self.updatestatus_consys1)
            self.checkCONSYS1.start()
            self.checkBPC1 = TUNNEL()
            self.checkBPC1.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi2"])
            #self.checkBPC1.direct(PANEL_COMMAND["test"], PANEL_IP["pi2"])
            self.checkBPC1.output.connect(self.updatestatus_bpc1)
            self.checkBPC1.start()
            self.p1connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p1connect.setText(_translate("MainWindow", "Connect"))
            self.p1connect.setStyleSheet("")
            self.p1.setStyleSheet("")
            self.p1scene1.setEnabled(False)
            self.p1scene2.setEnabled(False)

    def updatestatus_consys1(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[0][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[0][0] = "AOK"
            else:
                print("CONSYS1: ")
                for i in range(0, len(self.fullstatus) ):
                     print(self.fullstatus[i])
                PANEL_STATUS[0][0] = "ERR"
        self.monitor.update("p1")
        self.mutex.unlock()

    def updatestatus_bpc1(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[0][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[0][1] = "AOK"
            else:
                print("BPC1: ")
                for i in range(0, len(self.fullstatus) ):
                     print(self.fullstatus[i])
                PANEL_STATUS[0][1] = "ERR"
        self.monitor.update("p1")
        self.mutex.unlock()

    def connected1(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p1connect.setText(_translate("MainWindow", "Connected"))
            self.p1connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p1scene1.setEnabled(True)
            self.p1scene2.setEnabled(True)
        else:
            self.p1connect.setText(_translate("MainWindow", "Error"))
            self.p1connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p1scene(self, whichBtn):
        if(whichBtn == 1):
            print("P1SCENE")
        else:
            print("P1SCENE")

    # --------------------------
    def statuscheck_2(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS2 = TUNNEL()
            self.checkCONSYS2.direct(PANEL_COMMAND["status"], PANEL_IP["pi3"])
            #self.checkCONSYS2.direct(PANEL_COMMAND["test"], PANEL_IP["pi3"])
            self.checkCONSYS2.output.connect(self.updatestatus_consys2)
            self.checkCONSYS2.start()
            self.checkBPC2 = TUNNEL()
            self.checkBPC2.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi4"])
            #self.checkBPC2.direct(PANEL_COMMAND["test"], PANEL_IP["pi4"])
            self.checkBPC2.output.connect(self.updatestatus_bpc2)
            self.checkBPC2.start()
            self.p2connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p2connect.setText(_translate("MainWindow", "Connect"))
            self.p2connect.setStyleSheet("")
            self.p2.setStyleSheet("")
            self.p2scene1.setEnabled(False)
            self.p2scene2.setEnabled(False)

    def updatestatus_consys2(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[1][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[1][0] = "AOK"
            else:
                # Populate with more sophisticated error messages.
                # self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                print("CONSYS2: ")
                for i in range(0, len(self.fullstatus) ):
                     print(self.fullstatus[i])
                PANEL_STATUS[1][0] = "ERR"

        self.monitor.update("p2")
        self.mutex.unlock()

    def updatestatus_bpc2(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[1][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[1][1] = "AOK"
            else:
                # Populate with more sophisticated error messages.
                # self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                print("BPC2: ")
                for i in range(0, len(self.fullstatus) ):
                     print(self.fullstatus[i])
                PANEL_STATUS[1][1] = "ERR"

        self.monitor.update("p2")
        self.mutex.unlock()

    def connected2(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p2connect.setText(_translate("MainWindow", "Connected"))
            self.p2connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p2scene1.setEnabled(True)
            self.p2scene2.setEnabled(True)
        else:
            self.p2connect.setText(_translate("MainWindow", "Error"))
            self.p2connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p2scene(self, whichBtn):
        if(whichBtn == 1):
            print("P2SCENE")
        else:
            print("P2SCENE")

    # --------------------------
    def statuscheck_3(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS3 = TUNNEL()
            self.checkCONSYS3.direct(PANEL_COMMAND["status"], PANEL_IP["pi5"])
            #self.checkCONSYS3.direct(PANEL_COMMAND["test"], PANEL_IP["pi5"])
            self.checkCONSYS3.output.connect(self.updatestatus_consys3)
            self.checkCONSYS3.start()
            self.checkBPC3 = TUNNEL()
            self.checkBPC3.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi6"])
            #self.checkBPC3.direct(PANEL_COMMAND["test"], PANEL_IP["pi6"])
            self.checkBPC3.output.connect(self.updatestatus_bpc3)
            self.checkBPC3.start()
            self.p3connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p3connect.setText(_translate("MainWindow", "Connect"))
            self.p3connect.setStyleSheet("")
            self.p3.setStyleSheet("")
            self.p3scene1.setEnabled(False)
            self.p3scene2.setEnabled(False)

    def updatestatus_consys3(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[2][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[2][0] = "AOK"
            elif any("ERR" in s for s in self.fullstatus):
                # Will want to print out the error message later.
                self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                PANEL_STATUS[2][0] = "ERR"
            else:
                PANEL_STATUS[2][0] = "ERR"
        self.monitor.update("p3")
        self.mutex.unlock()

    def updatestatus_bpc3(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[2][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[2][1] = "AOK"
            else:
                PANEL_STATUS[2][1] = "ERR"
        self.monitor.update("p3")
        self.mutex.unlock()

    def connected3(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p3connect.setText(_translate("MainWindow", "Connected"))
            self.p3connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p3scene1.setEnabled(True)
            self.p3scene2.setEnabled(True)
        else:
            self.p3connect.setText(_translate("MainWindow", "Error"))
            self.p3connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p3scene(self, whichBtn):
        if(whichBtn == 1):
            print("P3SCENE")
        else:
            print("P3SCENE")

    # --------------------------
    def statuscheck_4(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS4 = TUNNEL()
            self.checkCONSYS4.direct(PANEL_COMMAND["status"], PANEL_IP["pi7"])
            #self.checkCONSYS4.direct(PANEL_COMMAND["test"], PANEL_IP["pi1"])
            self.checkCONSYS4.output.connect(self.updatestatus_consys4)
            self.checkCONSYS4.start()
            self.checkBPC4 = TUNNEL()
            self.checkBPC4.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi8"])
            #self.checkBPC4.direct(PANEL_COMMAND["test"], PANEL_IP["pi2"])
            self.checkBPC4.output.connect(self.updatestatus_bpc4)
            self.checkBPC4.start()
            self.p4connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p4connect.setText(_translate("MainWindow", "Connect"))
            self.p4connect.setStyleSheet("")
            self.p4.setStyleSheet("")
            self.p4scene1.setEnabled(False)
            self.p4scene2.setEnabled(False)

    def updatestatus_consys4(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[3][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[3][0] = "AOK"
            elif any("ERR" in s for s in self.fullstatus):
                # Will want to print out the error message later.
                self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                PANEL_STATUS[3][0] = "ERR"
            else:
                PANEL_STATUS[3][0] = "ERR"
        self.monitor.update("p4")
        self.mutex.unlock()

    def updatestatus_bpc4(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[3][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[3][1] = "AOK"
            else:
                PANEL_STATUS[3][1] = "ERR"
        self.monitor.update("p4")
        self.mutex.unlock()

    def connected4(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p4connect.setText(_translate("MainWindow", "Connected"))
            self.p4connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p4scene1.setEnabled(True)
            self.p4scene2.setEnabled(True)
        else:
            self.p4connect.setText(_translate("MainWindow", "Error"))
            self.p4connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p4scene(self, whichBtn):
        if(whichBtn == 1):
            print("P4SCENE")
        else:
            print("P4SCENE")

    # --------------------------
    def statuscheck_5(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS5 = TUNNEL()
            self.checkCONSYS5.direct(PANEL_COMMAND["status"], PANEL_IP["pi9"])
            #self.checkCONSYS5.direct(PANEL_COMMAND["test"], PANEL_IP["pi9"])
            self.checkCONSYS5.output.connect(self.updatestatus_consys5)
            self.checkCONSYS5.start()
            self.checkBPC5 = TUNNEL()
            self.checkBPC5.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi10"])
            #self.checkBPC5.direct(PANEL_COMMAND["test"], PANEL_IP["pi10"])
            self.checkBPC5.output.connect(self.updatestatus_bpc5)
            self.checkBPC5.start()
            self.p5connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p5connect.setText(_translate("MainWindow", "Connect"))
            self.p5connect.setStyleSheet("")
            self.p5.setStyleSheet("")
            self.p5scene1.setEnabled(False)
            self.p5scene2.setEnabled(False)

    def updatestatus_consys5(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[4][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[4][0] = "AOK"
            elif any("ERR" in s for s in self.fullstatus):
                # Will want to print out the error message later.
                self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                PANEL_STATUS[4][0] = "ERR"
            else:
                PANEL_STATUS[4][0] = "ERR"
        self.monitor.update("p5")
        self.mutex.unlock()

    def updatestatus_bpc5(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[4][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[4][1] = "AOK"
            else:
                PANEL_STATUS[4][1] = "ERR"
        self.monitor.update("p5")
        self.mutex.unlock()

    def connected5(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p5connect.setText(_translate("MainWindow", "Connected"))
            self.p5connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p5scene1.setEnabled(True)
            self.p5scene2.setEnabled(True)
        else:
            self.p5connect.setText(_translate("MainWindow", "Error"))
            self.p5connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p5scene(self, whichBtn):
        if(whichBtn == 1):
            print("P5SCENE")
        else:
            print("P5SCENE")

    # --------------------------
    def statuscheck_6(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS6 = TUNNEL()
            self.checkCONSYS6.direct(PANEL_COMMAND["status"], PANEL_IP["pi11"])
            #self.checkCONSYS6.direct(PANEL_COMMAND["test"], PANEL_IP["pi11"])
            self.checkCONSYS6.output.connect(self.updatestatus_consys6)
            self.checkCONSYS6.start()
            self.checkBPC6 = TUNNEL()
            self.checkBPC6.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi12"])
            #self.checkBPC6.direct(PANEL_COMMAND["test"], PANEL_IP["pi12"])
            self.checkBPC6.output.connect(self.updatestatus_bpc6)
            self.checkBPC6.start()
            self.p6connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p6connect.setText(_translate("MainWindow", "Connect"))
            self.p6connect.setStyleSheet("")
            self.p6.setStyleSheet("")
            self.p6scene1.setEnabled(False)
            self.p6scene2.setEnabled(False)

    def updatestatus_consys6(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[5][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[5][0] = "AOK"
            elif any("ERR" in s for s in self.fullstatus):
                # Will want to print out the error message later.
                self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                PANEL_STATUS[5][0] = "ERR"
            else:
                PANEL_STATUS[5][0] = "ERR"
        self.monitor.update("p6")
        self.mutex.unlock()

    def updatestatus_bpc6(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[5][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[5][1] = "AOK"
            else:
                PANEL_STATUS[5][1] = "ERR"
        self.monitor.update("p6")
        self.mutex.unlock()

    def connected6(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p6connect.setText(_translate("MainWindow", "Connected"))
            self.p6connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p6scene1.setEnabled(True)
            self.p6scene2.setEnabled(True)
        else:
            self.p6connect.setText(_translate("MainWindow", "Error"))
            self.p6connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p6scene(self, whichBtn):
        if(whichBtn == 1):
            print("P6SCENE")
        else:
            print("P6SCENE")

    # --------------------------
    def statuscheck_7(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS7 = TUNNEL()
            self.checkCONSYS7.direct(PANEL_COMMAND["status"], PANEL_IP["pi13"])
            #self.checkCONSYS7.direct(PANEL_COMMAND["test"], PANEL_IP["pi7"])
            self.checkCONSYS7.output.connect(self.updatestatus_consys7)
            self.checkCONSYS7.start()
            self.checkBPC7 = TUNNEL()
            self.checkBPC7.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi14"])
            #self.checkBPC7.direct(PANEL_COMMAND["test"], PANEL_IP["pi7"])
            self.checkBPC7.output.connect(self.updatestatus_bpc7)
            self.checkBPC7.start()
            self.p7connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p7connect.setText(_translate("MainWindow", "Connect"))
            self.p7connect.setStyleSheet("")
            self.p7.setStyleSheet("")
            self.p7scene1.setEnabled(False)
            self.p7scene2.setEnabled(False)

    def updatestatus_consys7(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[6][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[6][0] = "AOK"
            elif any("ERR" in s for s in self.fullstatus):
                # Will want to print out the error message later.
                self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                PANEL_STATUS[6][0] = "ERR"
            else:
                PANEL_STATUS[6][0] = "ERR"
        self.monitor.update("p7")
        self.mutex.unlock()

    def updatestatus_bpc7(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[6][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[6][1] = "AOK"
            else:
                PANEL_STATUS[6][1] = "ERR"
        self.monitor.update("p7")
        self.mutex.unlock()

    def connected7(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p7connect.setText(_translate("MainWindow", "Connected"))
            self.p7connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p7scene1.setEnabled(True)
            self.p7scene2.setEnabled(True)
        else:
            self.p7connect.setText(_translate("MainWindow", "Error"))
            self.p7connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p7scene(self, whichBtn):
        if(whichBtn == 1):
            print("P7SCENE")
        else:
            print("P7SCENE")

    # --------------------------
    def statuscheck_8(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS8 = TUNNEL()
            self.checkCONSYS8.direct(PANEL_COMMAND["status"], PANEL_IP["pi15"])
            #self.checkCONSYS8.direct(PANEL_COMMAND["test"], PANEL_IP["pi15"])
            self.checkCONSYS8.output.connect(self.updatestatus_consys8)
            self.checkCONSYS8.start()
            self.checkBPC8 = TUNNEL()
            self.checkBPC8.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi16"])
            #self.checkBPC8.direct(PANEL_COMMAND["test"], PANEL_IP["pi16"])
            self.checkBPC8.output.connect(self.updatestatus_bpc8)
            self.checkBPC8.start()
            self.p8connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p8connect.setText(_translate("MainWindow", "Connect"))
            self.p8connect.setStyleSheet("")
            self.p8.setStyleSheet("")
            self.p8scene1.setEnabled(False)
            self.p8scene2.setEnabled(False)

    def updatestatus_consys8(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[7][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[7][0] = "AOK"
            elif any("ERR" in s for s in self.fullstatus):
                # Will want to print out the error message later.
                self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                PANEL_STATUS[7][0] = "ERR"
            else:
                PANEL_STATUS[7][0] = "ERR"
        self.monitor.update("p8")
        self.mutex.unlock()

    def updatestatus_bpc8(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[7][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[7][1] = "AOK"
            else:
                PANEL_STATUS[7][1] = "ERR"
        self.monitor.update("p8")
        self.mutex.unlock()

    def connected8(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p8connect.setText(_translate("MainWindow", "Connected"))
            self.p8connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p8scene1.setEnabled(True)
            self.p8scene2.setEnabled(True)
        else:
            self.p8connect.setText(_translate("MainWindow", "Error"))
            self.p8connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p8scene(self, whichBtn):
        if(whichBtn == 1):
            print("P8SCENE")
        else:
            print("P8SCENE")

    # --------------------------
    def statuscheck_9(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS9 = TUNNEL()
            self.checkCONSYS9.direct(PANEL_COMMAND["status"], PANEL_IP["pi17"])
            #self.checkCONSYS9.direct(PANEL_COMMAND["test"], PANEL_IP["pi9"])
            self.checkCONSYS9.output.connect(self.updatestatus_consys9)
            self.checkCONSYS9.start()
            self.checkBPC9 = TUNNEL()
            self.checkBPC9.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi18"])
            #self.checkBPC9.direct(PANEL_COMMAND["test"], PANEL_IP["pi9"])
            self.checkBPC9.output.connect(self.updatestatus_bpc9)
            self.checkBPC9.start()
            self.p9connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p9connect.setText(_translate("MainWindow", "Connect"))
            self.p9connect.setStyleSheet("")
            self.p9.setStyleSheet("")
            self.p9scene1.setEnabled(False)
            self.p9scene2.setEnabled(False)

    def updatestatus_consys9(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[8][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[8][0] = "AOK"
            elif any("ERR" in s for s in self.fullstatus):
                # Will want to print out the error message later.
                self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                PANEL_STATUS[8][0] = "ERR"
            else:
                PANEL_STATUS[8][0] = "ERR"
        self.monitor.update("p9")
        self.mutex.unlock()

    def updatestatus_bpc9(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[8][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[8][1] = "AOK"
            else:
                PANEL_STATUS[8][1] = "ERR"
        self.monitor.update("p9")
        self.mutex.unlock()

    def connected9(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p9connect.setText(_translate("MainWindow", "Connected"))
            self.p9connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p9scene1.setEnabled(True)
            self.p9scene2.setEnabled(True)
        else:
            self.p9connect.setText(_translate("MainWindow", "Error"))
            self.p9connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p9scene(self, whichBtn):
        if(whichBtn == 1):
            print("P9SCENE")
        else:
            print("P9SCENE")

    # --------------------------
    def statuscheck_10(self, state):
        _translate = QtCore.QCoreApplication.translate
        if state:
            self.checkCONSYS10 = TUNNEL()
            self.checkCONSYS10.direct(PANEL_COMMAND["status"], PANEL_IP["pi19"])
            #self.checkCONSYS10.direct(PANEL_COMMAND["test"], PANEL_IP["pi19"])
            self.checkCONSYS10.output.connect(self.updatestatus_consys10)
            self.checkCONSYS10.start()
            self.checkBPC10 = TUNNEL()
            self.checkBPC10.direct(PANEL_COMMAND["statusbpc"], PANEL_IP["pi20"])
            #self.checkBPC10.direct(PANEL_COMMAND["test"], PANEL_IP["pi20"])
            self.checkBPC10.output.connect(self.updatestatus_bpc10)
            self.checkBPC10.start()
            self.p10connect.setText(_translate("MainWindow", "Connecting..."))
        else:
            self.p10connect.setText(_translate("MainWindow", "Connect"))
            self.p10connect.setStyleSheet("")
            self.p10.setStyleSheet("")
            self.p10scene1.setEnabled(False)
            self.p10scene2.setEnabled(False)

    def updatestatus_consys10(self, output ):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'CONSYS\\n'" ):
            PANEL_STATUS[9][0] = "CONSYS"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[9][0] = "AOK"
            elif any("ERR" in s for s in self.fullstatus):
                # Will want to print out the error message later.
                self.index = [i for i, s in enumerate(self.fullstatus) if 'ERR' in s]
                PANEL_STATUS[9][0] = "ERR"
            else:
                PANEL_STATUS[9][0] = "ERR"
        self.monitor.update("p10")
        self.mutex.unlock()

    def updatestatus_bpc10(self, output):
        self.mutex = QtCore.QMutex()
        self.mutex.lock()
        output = str(output)
        if( output == "b'BPC\\n'" ):
            PANEL_STATUS[9][1] = "BPC"
        else:
            self.archive = output.strip("b'")
            self.fullstatus = self.archive.split("\\n")
            if any("AOK" in s for s in self.fullstatus):
                PANEL_STATUS[9][1] = "AOK"
            else:
                PANEL_STATUS[9][1] = "ERR"
        self.monitor.update("p10")
        self.mutex.unlock()

    def connected10(self, bool):
        _translate = QtCore.QCoreApplication.translate
        if bool:
            self.p1connect.setText(_translate("MainWindow", "Connected"))
            self.p1connect.setStyleSheet("background: rgb(0, 255, 0);")
            self.p1scene1.setEnabled(True)
            self.p1scene2.setEnabled(True)
        else:
            self.p1connect.setText(_translate("MainWindow", "Error"))
            self.p1connect.setStyleSheet("background: rgb(255, 0, 0);")

    def p10scene(self, whichBtn):
        if(whichBtn == 1):
            print("P10SCENE")
        else:
            print("P10SCENE")

# --------------------------
def getIPs(file):
    '''
    Retrieve the IP addresses of the panels listed from a separate file.
    The file can (for sure) be .txt or .csv

    INPUTS:
        - file : The name of the file to access (string)

    OUTPUT:
        - IPs : A dict structure with the addresses in panel{i} format.
    '''
    IPs = dict()
    i=1
    with open( file, 'r' ) as f:                # Open file
        for ip in f:                            # Iterate over the contents
            name = "pi{}".format(i)             # Construct panel name
            IPs[ name ] = ip.strip('\n')        # Store into dictionary
            i=i+1                               # Increment counter
    return IPs

# --------------------------
# BEGIN THE PROGRAM:
def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = GUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

file = "ip_addrs.csv"

panels=10
global PANEL_IP, PANEL_COMMAND, PANEL_STATUS

PANEL_STATUS = []
for i in range(panels):
    PANEL_STATUS.append(["NULL", "NULL"])

PANEL_IP = getIPs(file)
PANEL_COMMAND = {
"reset"     : "sudo reboot",
"status"    : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
"statusbpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
"consys"    : "DISPLAY=:0 python pd3d/csec/repos/ControlSystem/Software/Python/consys/consys4.3.py",
"consysbpc" : "DISPLAY=:0 python pd3d/csec/repos/ControlSystem/Software/Python/consys/consys4.3bpc.py",
"test"      : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status.py"
}

run()
