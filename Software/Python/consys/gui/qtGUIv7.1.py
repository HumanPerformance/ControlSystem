'''
Author  : Edward Daniel Nichols
Date    : May 8th, 2018 AD

Proprietor:
PD3D, Institute for Simulation and Training
University of Central Florida
'''
from PyQt5 import QtCore, QtGui, QtWidgets
import paramiko as miko
import sys

# ---------------------------------------------------- #
class TUNNEL(QtCore.QThread):
    '''
    Open an SSH terminal at the address specified and send the command specified.
    Within the context of a QThread
    INPUTS:
        - outputChannel: Indicator where to place the output, within a GLOBAL array. (Int)
        - ADDR: The IP address of the SSH server to access. (String)
        - CMD: The single command, in the proper format, that is to be executed. (String)
    OUTPUT:
        - output: Reading from the socket's stdout, or else an error message.  (String)
    '''
    outputrdy = QtCore.pyqtSignal()
    # ----------------------
    def __init__(self, channel):
        super(TUNNEL, self).__init__()
        self.chnl = channel
        self.usr  = "pi"
        self.pwrd = "raspberry"
        self.ssh = miko.SSHClient()
        self.ssh.set_missing_host_key_policy(miko.AutoAddPolicy())
        self.ssh_stdin  = None
        self.ssh_stdout = None
        self.ssh_stderr = None
    # ----------------------
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
            outputChannel[self.chnl] = "ERROR: SSH Connection Failed"
            self.outputrdy.emit()

        if self.ssh_stdout:
            output =  self.ssh_stdout.read()
            outputChannel[self.chnl] = output
            self.outputrdy.emit()
        else:
            outputChannel[self.chnl] = "ERROR: NULL"
            self.outputrdy.emit()


# ---------------------------------------------------- #
class ROOM(QtCore.QObject):
    retrieve = QtCore.pyqtSignal(int, int)
    statbtntoggled = QtCore.pyqtSignal(int, int)
    int1btntoggled = QtCore.pyqtSignal(int, int)
    int2btntoggled = QtCore.pyqtSignal(int, int)
    AOKstatus = QtCore.pyqtSignal(int, int)
    ERRstatus = QtCore.pyqtSignal(int, int)

    def setup(self, roomNumber):
        self.identity = roomNumber

    def associatePanel(self, panel):
        self.operatingPanel = panel
        self.retrieve.emit(self.identity, self.operatingPanel-1)

    def statuscheck_btn(self):
        self.statbtntoggled.emit(self.identity, self.operatingPanel)

    def int1_btn(self):
        self.int1btntoggled.emit(self.identity, self.operatingPanel)

    def int2_btn(self):
        self.int2btntoggled.emit(self.identity, self.operatingPanel)

    def reviewStats(self, oppanel=["NULL", "NULL"]):
        # print(self.identity, self.operatingPanel, oppanel)
        self.status = oppanel

        if  (self.status[0]=="AOK" and self.status[1]=="AOK" ):
            self.AOKstatus.emit(self.identity, self.operatingPanel)
        elif(self.status[0]=="ERR" and self.status[1]=="AOK" ):
            self.ERRstatus.emit(self.identity, self.operatingPanel)
        elif(self.status[0]=="AOK" and self.status[1]=="ERR" ):
            self.ERRstatus.emit(self.identity, self.operatingPanel)
        elif(self.status[0]=="ERR" and self.status[1]=="ERR" ):
            self.ERRstatus.emit(self.identity, self.operatingPanel)
        # elif(self.status[0]=="DONE" and self.status[1]=="DONE" ):
        #     self.AOKstatus.emit(self.identity, self.operatingPanel)
        else:
            pass

# ---------------------------------------------------- #
class PANEL(QtCore.QObject):
    rawOutput = QtCore.pyqtSignal(int, str, str)

    def __init__(self, panelIdentity, CONSYSaddr, BPCaddr, commands):
        super(PANEL, self).__init__()
        self.panel = panelIdentity
        self.CONSYSaddr = CONSYSaddr
        self.CONSYSchnl = 2*(panelIdentity)-2
        self.BPCaddr = BPCaddr
        self.BPCchnl = 2*(panelIdentity)-1
        self.commands = dict()
        self.commands = commands

    def setRoomkey(self, roomKey ):
        self.roomKey = dict()
        self.roomKey = roomKey

    def pulloutput(self, subSys):
        if(subSys == "CON"):
            self.rawOutput.emit( self.panel, subSys, str( outputChannel[self.CONSYSchnl] ) )
        if(subSys == "BPC"):
            self.rawOutput.emit( self.panel, subSys, str( outputChannel[self.BPCchnl] ) )

    def checkstatus(self):
        self.CONSYSthread = TUNNEL(self.CONSYSchnl)
        self.CONSYSthread.direct(self.commands["statuscon"], self.CONSYSaddr)
        self.CONSYSthread.outputrdy.connect(lambda: self.pulloutput("CON"))
        self.CONSYSthread.start()

        self.BPCthread = TUNNEL(self.BPCchnl)
        self.BPCthread.direct(self.commands["statusbpc"], self.BPCaddr)
        self.BPCthread.outputrdy.connect(lambda: self.pulloutput("BPC"))
        self.BPCthread.start()

    def interaction1(self):
        self.CONSYSthread = TUNNEL(self.CONSYSchnl)
        self.CONSYSthread.direct(self.roomKey["int1con"], self.CONSYSaddr)
        self.CONSYSthread.outputrdy.connect(lambda: self.pulloutput("CON"))
        self.CONSYSthread.start()

        self.BPCthread = TUNNEL(self.BPCchnl)
        self.BPCthread.direct(self.roomKey["int1bpc"], self.BPCaddr)
        self.BPCthread.outputrdy.connect(lambda: self.pulloutput("BPC"))
        self.BPCthread.start()

    def interaction2(self):
        self.CONSYSthread = TUNNEL(self.CONSYSchnl)
        self.CONSYSthread.direct(self.roomKey["int2con"], self.CONSYSaddr)
        self.CONSYSthread.outputrdy.connect(lambda: self.pulloutput("CON"))
        self.CONSYSthread.start()

        self.BPCthread = TUNNEL(self.BPCchnl)
        self.BPCthread.direct(self.roomKey["int2bpc"], self.BPCaddr)
        self.BPCthread.outputrdy.connect(lambda: self.pulloutput("BPC"))
        self.BPCthread.start()

# ---------------------------------------------------- #
class GUI(object):

    def __init__(self, systems, file, commands):
        '''
        The Control System Graphical User Interface built for the sponsors of
        PD3D, at the University of Central Florida
        @RestrictedLicense
        '''
        self.systems = systems

        self.commands = dict()
        self.commands = commands

        self.ipADDRS = dict()
        self.ipADDRS = self.getADDRs(file)

        self.panels=[]
        for index in range(self.systems):
            CONSYSkey = "pi" + str(2*index+1)
            BPCkey="pi" + str(2*index+2)
            self.panels.append( PANEL( index+1,
                                       self.ipADDRS[CONSYSkey],
                                       self.ipADDRS[BPCkey],
                                       self.commands) )
        self.panel_status=[]
        # print("Initializing... " + str(self.systems) + " systems.")
        for index in range(systems):
            # Format: CONSYS_STATE, BPC_STATE, ROOM_ASSOC
            self.panel_status.append(["NULL", "NULL", "NULL", ""])

    def setup(self, ControlSystem):
        # ---------------------------------------------------- #
        # Predefine some basic parameters:

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ControlSystem.sizePolicy().hasHeightForWidth())

        self.greybg = "background: rgba(240, 240, 240, 220);"
        self.redbg = "background: rgba(255, 20, 0, 230);"
        self.greenbg = "background: rgba(0, 255, 0, 230);"
        self.bluebg = "background: rgba(0, 160, 255, 100);"
        self.purpbg = "background: rgba(200, 0, 255, 100);"
        self.yellowbg = "background: rgba(255, 180, 0, 230);"

        panelfont = QtGui.QFont()
        panelfont.setFamily("Yu Gothic UI")
        panelfont.setPointSize(10)

        btnfont = QtGui.QFont()
        btnfont.setFamily("Yu Gothic UI")
        btnfont.setPointSize(12)
        btnfont.setBold(False)
        btnfont.setWeight(50)

        consysfont = QtGui.QFont()
        consysfont.setFamily("Yu Gothic UI")
        consysfont.setPointSize(16)
        consysfont.setBold(False)
        consysfont.setWeight(50)

        titleFont = QtGui.QFont()
        titleFont.setFamily("Yu Gothic UI")
        titleFont.setPointSize(26)
        titleFont.setBold(True)
        titleFont.setWeight(75)

        # ---------------------------------------------------- #
        # Create the main window and set the geometry:
        ControlSystem.setObjectName("ControlSystem")
        ControlSystem.resize(1000, 850)

        ControlSystem.setSizePolicy(sizePolicy)
        ControlSystem.setMinimumSize(QtCore.QSize(1000, 850))
        ControlSystem.setLayoutDirection(QtCore.Qt.LeftToRight)
        ControlSystem.setAutoFillBackground(False)
        ControlSystem.setStyleSheet("background: rgb(255, 255, 255);")
        self.windowLayout = QtWidgets.QVBoxLayout(ControlSystem)
        self.windowLayout.setObjectName("windowLayout")

        # ---------------------------------------------------- #
        # Create the primary grid within the main window:
        self.primaryGrid = QtWidgets.QGridLayout()
        self.primaryGrid.setSpacing(10)
        self.primaryGrid.setObjectName("primaryGrid")

        # ---------------------------------------------------- #
        # Grid layout and interface for each room:

        self.gridR=[]
        self.room=[]
        self.selectPanelR=[]
        self.statusR=[]
        self.int1R=[]
        self.int2R=[]
        self.roomMonitor=[]

        for i in range(0,3):
            for j in range(0,3):

                index = 3*i + j

                # -------------------------- Grid:
                name = "R" + str(index + 1)
                self.gridR.append(QtWidgets.QGridLayout())
                self.gridR[index].setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
                self.gridR[index].setContentsMargins(10, 10, 10, 10)
                self.gridR[index].setSpacing(10)
                self.gridR[index].setObjectName("grid" + name)

                # -------------------------- Room Label:
                self.room.append(QtWidgets.QLabel(ControlSystem))
                self.room[index].setMinimumSize(QtCore.QSize(150, 150))
                self.room[index].setMaximumSize(QtCore.QSize(16777215, 200))
                self.room[index].setFont(titleFont)
                self.room[index].setStyleSheet(self.greybg)
                self.room[index].setScaledContents(False)
                self.room[index].setAlignment(QtCore.Qt.AlignCenter)
                self.room[index].setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                self.room[index].setObjectName("room" + name)
                self.gridR[index].addWidget(self.room[index], 0, 0, 1, 2)

                # -------------------------- Panel Selection Drop Menu:
                self.selectPanelR.append(QtWidgets.QComboBox(ControlSystem))
                self.selectPanelR[index].setMinimumSize(QtCore.QSize(150, 25))
                self.selectPanelR[index].setFont(btnfont)
                self.selectPanelR[index].setStyleSheet(self.greybg)
                self.selectPanelR[index].setObjectName("selectPanel" + name)
                for k in range(0, self.systems+1):
                    self.selectPanelR[index].addItem("")
                self.gridR[index].addWidget(self.selectPanelR[index], 1, 0, 1, 2)

                # -------------------------- Status Button:
                self.statusR.append(QtWidgets.QPushButton(ControlSystem))
                self.statusR[index].setMinimumSize(QtCore.QSize(150, 25))
                self.statusR[index].setFont(btnfont)
                self.statusR[index].setStyleSheet(self.greybg)
                self.statusR[index].setEnabled(False)
                self.statusR[index].setCheckable(True)
                self.statusR[index].setObjectName("status" + name)
                self.gridR[index].addWidget(self.statusR[index], 2, 0, 1, 2)

                # -------------------------- Interaction 1 Button:
                self.int1R.append(QtWidgets.QPushButton(ControlSystem))
                self.int1R[index].setMinimumSize(QtCore.QSize(50, 25))
                self.int1R[index].setFont(btnfont)
                self.int1R[index].setStyleSheet(self.greybg)
                self.int1R[index].setObjectName("int1" + name)
                self.int1R[index].setEnabled(False)
                self.gridR[index].addWidget(self.int1R[index], 3, 0, 1, 1)

                # -------------------------- Interaction 2 Button:
                self.int2R.append(QtWidgets.QPushButton(ControlSystem))
                self.int2R[index].setMinimumSize(QtCore.QSize(50, 25))
                self.int2R[index].setFont(btnfont)
                self.int2R[index].setStyleSheet(self.greybg)
                self.int2R[index].setObjectName("int2" + name)
                self.int2R[index].setEnabled(False)
                self.gridR[index].addWidget(self.int2R[index], 3, 1, 1, 1)

                # -------------------------- Populate primary Layout:
                self.primaryGrid.addLayout(self.gridR[index], i, j+1, 1, 1)

                # -------------------------- Room Monitor Threads:
                self.roomMonitor.append(ROOM())
                self.roomMonitor[index].setup(index)
                self.roomMonitor[index].retrieve.connect(self.retrievePanel)
                self.roomMonitor[index].statbtntoggled.connect(self.statbtnCondition)
                self.roomMonitor[index].int1btntoggled.connect(self.RUN1statusCondition)
                self.roomMonitor[index].int2btntoggled.connect(self.RUN2statusCondition)
                self.roomMonitor[index].AOKstatus.connect(self.AOKstatusCondition)
                self.roomMonitor[index].ERRstatus.connect(self.ERRstatusCondition)
                self.selectPanelR[index].currentIndexChanged.connect(self.roomMonitor[index].associatePanel)

        # ---------------------------------------------------- #
        # Layout and interface for consolidated control sidebar:

        self.controlLayout = QtWidgets.QVBoxLayout()
        self.controlLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.controlLayout.setSpacing(10)
        self.controlLayout.setObjectName("controlLayout")

        # -------------------------- Logo:
        self.logo = QtWidgets.QLabel(ControlSystem)
        self.logo.setMinimumSize(QtCore.QSize(400, 180))
        self.logo.setMaximumSize(QtCore.QSize(400, 180))
        self.logo.setPixmap(QtGui.QPixmap("pd3d.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.logo.setObjectName("logo")
        self.controlLayout.addWidget(self.logo)

        # -------------------------- Connect All Button:
        self.connectAll = QtWidgets.QPushButton(ControlSystem)
        self.connectAll.setMinimumSize(QtCore.QSize(0, 50))
        self.connectAll.setMaximumSize(QtCore.QSize(400, 50))
        self.connectAll.setFont(consysfont)
        self.connectAll.setStyleSheet(self.greybg)
        self.connectAll.setObjectName("connectAll")
        self.controlLayout.addWidget(self.connectAll)

        # -------------------------- Interaction 1 Button:
        self.int1All = QtWidgets.QPushButton(ControlSystem)
        self.int1All.setMinimumSize(QtCore.QSize(0, 50))
        self.int1All.setMaximumSize(QtCore.QSize(400, 50))
        self.int1All.setFont(consysfont)
        self.int1All.setStyleSheet(self.greybg)
        self.int1All.setObjectName("int1All")
        self.controlLayout.addWidget(self.int1All)

        # -------------------------- Interaction 2 Button:
        self.int2All = QtWidgets.QPushButton(ControlSystem)
        self.int2All.setMinimumSize(QtCore.QSize(0, 50))
        self.int2All.setMaximumSize(QtCore.QSize(400, 50))
        self.int2All.setFont(consysfont)
        self.int2All.setStyleSheet(self.greybg)
        self.int2All.setObjectName("int2All")
        self.controlLayout.addWidget(self.int2All)

        # -------------------------- System Panel Tabs:
        self.panelTabs = QtWidgets.QTabWidget(ControlSystem)
        self.panelTabs.setEnabled(True)
        self.panelTabs.setMinimumSize(QtCore.QSize(0, 200))
        self.panelTabs.setMaximumSize(QtCore.QSize(400, 16777215))
        self.panelTabs.setFont(panelfont)
        self.panelTabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.panelTabs.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.panelTabs.setUsesScrollButtons(True)
        self.panelTabs.setObjectName("panelTabs")

        self.ptab=[]
        self.ptabLayout=[]
        self.paddr=[]
        self.pscrollArea=[]
        self.pscrollContents=[]
        self.tabinteriorLayout=[]
        self.poutput=[]

        for index in range (0, self.systems):
            self.ptab.append(QtWidgets.QWidget())
            self.ptab[index].setObjectName("tab" + str(index))
            self.ptabLayout.append(QtWidgets.QGridLayout(self.ptab[index]))
            self.ptabLayout[index].setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
            self.ptabLayout[index].setContentsMargins(5, 5, 5, 5)
            self.ptabLayout[index].setSpacing(10)
            self.ptabLayout[index].setObjectName("ptabLayout" + str(index))
            self.paddr.append(QtWidgets.QLabel(self.ptab[index]))
            self.paddr[index].setMinimumSize(QtCore.QSize(0, 0))
            self.paddr[index].setFont(panelfont)
            self.paddr[index].setStyleSheet(self.greybg)
            self.paddr[index].setObjectName("paddr" + str(index))
            self.ptabLayout[index].addWidget(self.paddr[index], 0, 0, 1, 1)
            self.pscrollArea.append(QtWidgets.QScrollArea(self.ptab[index]))
            self.pscrollArea[index].setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.pscrollArea[index].setWidgetResizable(True)
            self.pscrollArea[index].setObjectName("pscrollArea" + str(index))
            self.pscrollContents.append(QtWidgets.QWidget())
            self.pscrollContents[index].setMinimumSize(QtCore.QSize(0, 150))
            self.pscrollContents[index].setSizePolicy(sizePolicy)
            self.pscrollContents[index].setObjectName("pscrollContents" + str(index))
            self.tabinteriorLayout.append(QtWidgets.QGridLayout(self.pscrollContents[index]))
            self.tabinteriorLayout[index].setObjectName("tabinteriorLayout" + str(index))
            self.tabinteriorLayout[index].setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
            self.tabinteriorLayout[index].setContentsMargins(0, 0, 0, 0)
            self.tabinteriorLayout[index].setSpacing(0)
            self.poutput.append(QtWidgets.QLabel(self.pscrollContents[index]))
            self.poutput[index].setSizePolicy(sizePolicy)
            self.poutput[index].setStyleSheet(self.greybg)
            self.poutput[index].setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
            self.poutput[index].setObjectName("poutput" + str(index))
            self.tabinteriorLayout[index].addWidget(self.poutput[index], 0, 0, 1, 1)
            self.pscrollArea[index].setWidget(self.pscrollContents[index])
            self.ptabLayout[index].addWidget(self.pscrollArea[index], 1, 0, 1, 1)
            self.panelTabs.addTab(self.ptab[index], "")
        self.controlLayout.addWidget(self.panelTabs)

        # -------------------------- Options Layout:
        self.optionsLayout = QtWidgets.QHBoxLayout()
        self.optionsLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.optionsLayout.setSpacing(10)
        self.optionsLayout.setObjectName("optionsLayout")

        # -------------------------- Options Button:
        self.advancedOpt = QtWidgets.QToolButton(ControlSystem)
        self.advancedOpt.setMinimumSize(QtCore.QSize(75, 75))
        self.advancedOpt.setMaximumSize(QtCore.QSize(75, 75))
        self.advancedOpt.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.advancedOpt.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.advancedOpt.setFont(panelfont)
        self.advancedOpt.setStyleSheet(self.greybg)
        self.advancedOpt.setObjectName("advancedOpt")
        self.optionsLayout.addWidget(self.advancedOpt)

        # -------------------------- Options Menu in Button:
        menu = QtWidgets.QMenu("Options")
        menu.addAction("Show Full Screen", ControlSystem.showFullScreen)
        menu.addAction("Show Window", ControlSystem.showNormal)
        menu.addSeparator()
        menu.addAction("Fetch Data from All", ControlSystem.close)
        for index in range(0,9):
            actionItem = "Fetch from Room " + str(index+1)
            menu.addAction(actionItem, ControlSystem.close)
        menu.addSeparator()
        for index in range(0, self.systems):
            actionItem = "Test Panel " + str(index+1)
            menu.addAction(actionItem)
        menu.addSeparator()
        menu.addAction("Reboot All Panels")
        self.advancedOpt.setMenu(menu)

        # -------------------------- "Quit Program" Button:
        self.quitProg = QtWidgets.QPushButton(ControlSystem)
        self.quitProg.setMinimumSize(QtCore.QSize(75, 75))
        self.quitProg.setMaximumSize(QtCore.QSize(350, 75))
        self.quitProg.setStyleSheet(self.greybg)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("powerbutton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quitProg.setIcon(icon)
        self.quitProg.setIconSize(QtCore.QSize(50, 50))
        self.quitProg.setObjectName("quitProg")
        self.optionsLayout.addWidget(self.quitProg)

        # -------------------------- Populate ControlSystem Window:
        self.controlLayout.addLayout(self.optionsLayout)
        self.primaryGrid.addLayout(self.controlLayout, 0, 0, 3, 1)
        self.windowLayout.addLayout(self.primaryGrid)

        # -------------------------- Translate Text to Locality Language:
        self.initTranslateGUI(ControlSystem)

        # -------------------------- Arrange Connections:
        for index in range(self.systems):
            self.panels[index].rawOutput.connect(self.panelEndJob)

        for index in range(0, 9):
            self.connectAll.clicked.connect(self.statusR[index].click)
            self.int1All.clicked.connect(self.int1R[index].click)
            self.int2All.clicked.connect(self.int2R[index].click)

        self.quitProg.clicked.connect(ControlSystem.close)
        self.panelTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ControlSystem)

    # ---------------------------------------------------- #
    def initTranslateGUI(self, ControlSystem):
        _translate = QtCore.QCoreApplication.translate
        ControlSystem.setWindowTitle(_translate("ControlSystem", "Panel Control System"))

        for index in range(0,9):
            rname = "Room " + str(index + 1)
            self.room[index].setText(_translate("ControlSystem", rname))
            self.selectPanelR[index].setItemText(0, _translate("ControlSystem", "No Panel"))
            for k in range (1, self.systems+1):
                pnames = str(k)
                self.selectPanelR[index].setItemText(k, _translate("ControlSystem", "Panel " + pnames))
            self.statusR[index].setText(_translate("ControlSystem", "Connect"))
            self.int1R[index].setText(_translate("ControlSystem", "Int: 1"))
            self.int2R[index].setText(_translate("ControlSystem", "Int: 2"))

        self.connectAll.setText(_translate("ControlSystem", "Connect All"))
        self.int1All.setText(_translate("ControlSystem", "Interaction 1"))
        self.int2All.setText(_translate("ControlSystem", "Interaction 2"))

        for index in range(0,self.systems):
            pnames = "P" + str(index+1)
            consys = "CONSYS IP:\t\t\t\t\t" + self.ipADDRS["pi"+str(2*index+1)]
            bpc    = "BPC IP:\t\t\t\t\t\t" + self.ipADDRS["pi"+str(2*index+2)]
            ipshow = consys + "\n" + bpc
            self.paddr[index].setText(_translate("ControlSystem", ipshow))
            self.poutput[index].setText(_translate("ControlSystem", self.panel_status[index][3]))
            self.panelTabs.setTabText(self.panelTabs.indexOf(self.ptab[index]), _translate("ControlSystem", pnames))

        self.advancedOpt.setText(_translate("ControlSystem", "Adv.\nOptions"))
        self.quitProg.setShortcut(_translate("ControlSystem", "Ctrl+C"))

    # ---------------------------------------------------- #
    def getADDRs(self, file):
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

    # ---------------------------------------------------- #
    def retrievePanel(self, roomID, panelID):
        if panelID == -1:
            _translate = QtCore.QCoreApplication.translate
            if self.statusR[roomID].isChecked():
                self.statusR[roomID].click()
            self.statusR[roomID].setText(_translate("ControlSystem", "Connect"))
            self.statusR[roomID].setStyleSheet(self.greybg)
            self.statusR[roomID].setEnabled(False)

            self.room[roomID].setStyleSheet(self.greybg)
        else:
            self.statusR[roomID].setEnabled(True)
            # self.int1R[roomID].setEnabled(True)
            # self.int2R[roomID].setEnabled(True)
            if  (self.panel_status[panelID][2] == "NULL"):
                self.statusR[roomID].clicked.connect(lambda: self.roomMonitor[roomID].statuscheck_btn() )
                self.int1R[roomID].clicked.connect(lambda: self.roomMonitor[roomID].int1_btn())
                self.int2R[roomID].clicked.connect(lambda: self.roomMonitor[roomID].int2_btn())
                self.panels[panelID].setRoomkey(keyChain[roomID])
                self.panel_status[panelID][2] = "R" + str(roomID)
            else:
                prevAssoc = int( self.panel_status[panelID][2].strip('R') )
                self.selectPanelR[prevAssoc].setCurrentIndex(0)
                self.statusR[prevAssoc].clicked.disconnect()
                self.int1R[prevAssoc].clicked.disconnect()
                self.int2R[prevAssoc].clicked.disconnect()
                self.statusR[roomID].clicked.connect(lambda: self.roomMonitor[roomID].statuscheck_btn() )
                self.int1R[roomID].clicked.connect(lambda: self.roomMonitor[roomID].int1_btn())
                self.int2R[roomID].clicked.connect(lambda: self.roomMonitor[roomID].int2_btn())
                self.panels[panelID].setRoomkey(keyChain[roomID])
                self.panel_status[panelID][2] = "R" + str(roomID)

    # ---------------------------------------------------- #
    def statbtnCondition(self, roomID, panelID):
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate
        if self.statusR[roomID].isChecked():
            self.statusR[roomID].setEnabled(False)
            self.statusR[roomID].setText(_translate("ControlSystem", "Connecting..."))

            self.panel_status[panelIdx][0] = "NULL"
            self.panel_status[panelIdx][1] = "NULL"
            oppanel = [ self.panel_status[panelIdx][0], self.panel_status[panelIdx][1] ]
            self.roomMonitor[roomID].reviewStats(oppanel)

            self.panel_status[panelIdx][3] = "Connecting...\n"
            self.poutput[panelIdx].setText(_translate("ControlSystem", self.panel_status[panelIdx][3]))
            self.panels[panelIdx].checkstatus()
        else:
            self.statusR[roomID].setText(_translate("ControlSystem", "Connect"))
            self.statusR[roomID].setStyleSheet(self.greybg)
            self.room[roomID].setStyleSheet(self.greybg)
            self.int1R[roomID].setEnabled(False)
            self.int2R[roomID].setEnabled(False)

    # ---------------------------------------------------- #
    def AOKstatusCondition(self, roomID, panelID):
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate

        if self.statusR[roomID].isChecked():
            self.statusR[roomID].setText(_translate("ControlSystem", "Connected"))
            self.statusR[roomID].setStyleSheet(self.greenbg)
            self.room[roomID].setStyleSheet(self.greenbg)

            self.statusR[roomID].setEnabled(True)
            self.int1R[roomID].setEnabled(True)
            self.int2R[roomID].setEnabled(True)
        else:
            pass

    # ---------------------------------------------------- #
    def ERRstatusCondition(self, roomID, panelID):
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate

        if self.statusR[roomID].isChecked():
            self.statusR[roomID].setText(_translate("ControlSystem", "Error"))
            self.statusR[roomID].setStyleSheet(self.redbg)
            self.room[roomID].setStyleSheet(self.redbg)

            self.statusR[roomID].setEnabled(True)
            self.int1R[roomID].setEnabled(False)
            self.int2R[roomID].setEnabled(False)
        else:
            pass

    # ---------------------------------------------------- #
    def RUN1statusCondition(self, roomID, panelID):
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate

        if self.statusR[roomID].isChecked():
            self.room[roomID].setStyleSheet(self.bluebg)

            self.statusR[roomID].setEnabled(False)
            self.statusR[roomID].setStyleSheet(self.bluebg)
            self.statusR[roomID].setText(_translate("ControlSystem", "Running Int: 1"))

            self.int1R[roomID].setEnabled(False)
            self.int2R[roomID].setEnabled(False)

            self.panel_status[panelIdx][0] = "RN1"
            self.panel_status[panelIdx][1] = "RN1"
            oppanel = [ self.panel_status[panelIdx][0], self.panel_status[panelIdx][1] ]
            self.roomMonitor[roomID].reviewStats(oppanel)

            self.panel_status[panelIdx][3] = "Interaction 1...\n"
            self.poutput[panelIdx].setText(_translate("ControlSystem", self.panel_status[panelIdx][3]))
            self.panels[panelIdx].interaction1()

        else:
            pass

    # ---------------------------------------------------- #
    def RUN2statusCondition(self, roomID, panelID):
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate

        if self.statusR[roomID].isChecked():
            self.room[roomID].setStyleSheet(self.purpbg)

            self.statusR[roomID].setEnabled(False)
            self.statusR[roomID].setStyleSheet(self.purpbg)
            self.statusR[roomID].setText(_translate("ControlSystem", "Running Int: 2"))

            self.int1R[roomID].setEnabled(False)
            self.int2R[roomID].setEnabled(False)

            self.panel_status[panelIdx][0] = "RN2"
            self.panel_status[panelIdx][1] = "RN2"
            oppanel = [ self.panel_status[panelIdx][0], self.panel_status[panelIdx][1] ]
            self.roomMonitor[roomID].reviewStats(oppanel)

            self.panel_status[panelIdx][3] = "Interaction 2...\n"
            self.poutput[panelIdx].setText(_translate("ControlSystem", self.panel_status[panelIdx][3]))
            self.panels[panelIdx].interaction2()

        else:
            pass

    # ---------------------------------------------------- #
    def panelEndJob(self, panelID, subSys, rawMessage):
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate
        edits = rawMessage.strip("b'")
        review = edits.split("\\n")
        message = edits.replace("\\n", "\n")
        if(subSys == "CON"):
            if( rawMessage == "b'CONSYS\\n'" ):
                self.panel_status[panelIdx][0] = "CONSYS"
            else:
                if any("AOK" in s for s in review):
                    self.panel_status[panelIdx][0] = "AOK"
                elif any("DONE" in s for s in review):
                    self.panel_status[panelIdx][0] = "DONE"
                else:
                    self.panel_status[panelIdx][0] = "ERR"
        if(subSys == "BPC"):
            if( rawMessage == "b'BPC\\n'" ):
                self.panel_status[panelIdx][1] = "BPC"
            else:
                if any("AOK" in s for s in review):
                    self.panel_status[panelIdx][1] = "AOK"
                elif any("DONE" in s for s in review):
                    self.panel_status[panelIdx][1] = "DONE"
                else:
                    self.panel_status[panelIdx][1] = "ERR"

        if(self.panel_status[panelIdx][2] == "NULL"):
            pass
        else:
            oppanel=[ self.panel_status[panelIdx][0], self.panel_status[panelIdx][1] ]
            roomID = int( self.panel_status[panelIdx][2].strip('R') )
            self.roomMonitor[roomID].reviewStats(oppanel)

        if(subSys == "CON"):
            self.panel_status[panelIdx][3] = self.panel_status[panelIdx][3] + "\nCONSYS Subsystem Output:\n" + message
        elif(subSys == "BPC"):
            self.panel_status[panelIdx][3] = self.panel_status[panelIdx][3] + "\nBPC Subsystem Output:\n" + message
        else:
            self.panel_status[panelIdx][3] = self.panel_status[panelIdx][3] + "\nUNKNWN Output:\n" + message
        self.poutput[panelIdx].setText(_translate("ControlSystem", self.panel_status[panelIdx][3]))

# -------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":

    # ---------------------------------------------------- #
    # Standard Commands Available to All Panels
    STDCMDS = {
    "reset"     : "sudo reboot",
    "statuscon" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "statusbpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "normcon"   : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/consys4.3.py",
    "normbpc"   : "DISPLAY=:0 python pd3d/csec/repos/ControlSystem/Software/Python/consys/consys4.3bpc.py -s 0 -st 30 -lp 85 -hp 145",
    "test"      : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status.py"
    }

    # ---------------------------------------------------- #
    # Room 1 Shell Command Key :
    roomKey1 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    # Room 2 Shell Command Key :
    roomKey2 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    # Room 3 Shell Command Key :
    roomKey3 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    # Room 4 Shell Command Key :
    roomKey4 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    # Room 5 Shell Command Key :
    roomKey5 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    # Room 6 Shell Command Key :
    roomKey6 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    # Room 7 Shell Command Key :
    roomKey7 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    # Room 8 Shell Command Key :
    roomKey8 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    # Room 9 Shell Command Key :
    roomKey9 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    roomKey10 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    roomKey11 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }

    roomKey12 = {
    "int1con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int1bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py",
    "int2con" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3.py",
    "int2bpc" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status4.3bpc.py"
    }


    global keyChain
    keyChain = [ roomKey1, roomKey2, roomKey3, roomKey4, roomKey5, roomKey6, roomKey7, roomKey8, roomKey9, roomKey10, roomKey11, roomKey12 ]

    # ---------------------------------------------------- #
    # CSEC Testing Setup Properties :
    PANELS = 8
    FILE = "ip_addrs.csv"

    global outputChannel
    outputChannel = []
    for index in range(2*PANELS):
        outputChannel.append("NULL")

    try:
        appplication = QtWidgets.QApplication(sys.argv)
        appplication.setStyle('Fusion')

        ControlSystem = QtWidgets.QWidget()
        CSEC = GUI(PANELS, FILE, STDCMDS)
        CSEC.setup(ControlSystem)
        ControlSystem.show()

        sys.exit(appplication.exec_())

    except Exception as e:
        sys.stderr.write("SSH connection error: {0}".format(e))
