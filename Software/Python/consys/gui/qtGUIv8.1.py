'''
The Control System Graphical User Interface built for the sponsors of
PD3D, at the Institute for Simulation and Training
University of Central Florida
@RestrictedLicense

Author  : Edward Daniel Nichols
Date    : July 28nd, 2018 AD
'''

from PyQt5 import QtCore, QtGui, QtWidgets
import paramiko as miko
import sys, time

# ---------------------------------------------------- #
class TUNNEL(QtCore.QThread):
    '''
    PURPOSE:
    Thread object to setup and complete independent SSH session with a server for a single command at a time.
    It must be initialized, directed, and then run. Within the context of a QThread; SSH client based on paramiko.

    INPUTS:
    __init___()
        - chnl: Index of GLOBAL array where to place the output.                                             (Int from PANEL.[command])
    direct()
        - ADDR: The IP address of the SSH server to access.                                                  (String from PANEL.[command])
        - CMD: The single command, in the proper format, that is to be executed.                             (String from PANEL.[command])

    OUTPUT:
    run()
        - outputChannel[self.chnl]: Reading from the socket's stdout, or else an error message.              (String to GLOBAL Array)
        - outputrdy: Flag prompting panel object to read output placed in outputChannel.                     (Signal to PANEL.pulloutput)

    DIRECT REFERENCE:
        - PANEL.checkstatus: For a PANEL within a ROOM, send the "status" command string to SSH terminal.    (Class Method: Input)
        - PANEL.interaction1: For a PANEL within a ROOM, send the "int1" command string to SSH terminal.     (Class Method: Input)
        - PANEL.interaction2: For a PANEL within a ROOM, send the "int2" command string to SSH terminal.     (Class Method: Input)
        - PANEL.pulloutput: For a PANEL within a ROOM, read prepared output and pass to ROOM object.         (Class Method: Output(s))
    '''
    outputrdy = QtCore.pyqtSignal()
    # ----------------------
    def __init__(self, chnl):
        super(TUNNEL, self).__init__()
        self.chnl = chnl
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
            print("Debugging_TUNNEL_panel" + str(self.chnl+1) + "_cmd: \t\t" + str(self.cmd))
            self.ssh.connect(self.addr, username= self.usr, password= self.pwrd)
            self.ssh_stdin, self.ssh_stdout, self.ssh_stderr = self.ssh.exec_command(self.cmd)

        except Exception as e:
            sys.stderr.write("SSH connection error: {0}".format(e))
            outputChannel[self.chnl] = "FATAL: SSH Connection Failed"
            self.outputrdy.emit()

        if self.ssh_stdout:

            output =  self.ssh_stdout.read()
            outputChannel[self.chnl] = output
            self.outputrdy.emit()
            print("Debugging_TUNNEL_panel" + str(self.chnl+1) + "_outputrdy:\t" + str(output) )
            self.ssh.close()
        else:
            outputChannel[self.chnl] = "ERROR: NULL"
            self.outputrdy.emit()
            print("Debugging_TUNNEL_panel" + str(self.chnl+1) + "_outputrdy: ERROR: NULL")
            self.ssh.close()

# ---------------------------------------------------- #
class PANEL(QtCore.QObject):
    '''
    PURPOSE:
    The core CSEC augmented device panel concept. Holds the methods required of a panel, to conduct
    distinct augmented device "interactions" with a user and pass the output to the system.
    It leverages the TUNNEL threading object to open an SSH terminal with a panel. It must be
    initialized, and given a room key as it is placed into a ROOM where its methods become connected to
    the GUI buttons of the ROOM it is in. When TUNNEL output ready flag is raised after running a
    button command, the panel object then pulls the output from the global outputChannel array to actually
    send it to the system for status review. Within the context of a QObject.

    INPUTS:
    __init__()
        - panelIdentity: Unique ID of the PANEL, based on order of IP address list for panels.               (Int from GUI.__init__)
        - panelAddr: The IP address of the PANEL (SSH) server to access, probably a Raspberry Pi             (String from GUI.__init__)
        - commands: The dictionary of standard commands available to all PANELs.                             (Dict from GUI.__init__)
    setRoomkey()
        - roomKey: The dictionary of the specific commands available to the PANEL as a result of             (Dict from GUI.retrievePanel)
                     which ROOM it is in.

    OUTPUT:
    pulloutput()
        - rawOutput: Flag with box containing the ID of the panel and the result from the terminal           (Signal [Int, String] to GUI.panelEndJob)
                     at the end of a TUNNEL prompting the system "panelEndJob" sequence to set the
                     status of the panel - which determines GUI color for a PANEL in a ROOM.

    DIRECT REFERENCE:
        - GUI.__init__: Initialize the control system, loading the initial configuration including           (Class Method: Input(s))
                     number of panels, their IP addresses, and the commands available.
        - GUI.retrievePanel: When a panel is associated with a new ROOM, panel recieves the ROOM's           (Class Method: Input)
                     specified dictionary for available commands.
        - self.checkstatus/interaction1/interaction2: When GUI button is pressed, execute the panel          (Class Method: Output)
                     command by starting a TUNNEL. The local TUNNEL flag is connected.
                     When TUNNEL has recieved a reply, flag is raised and the raw message is emitted as
                     part of a new system-wide flag.

    '''
    rawOutput = QtCore.pyqtSignal(int, str)

    def __init__(self, panelIdentity, panelAddr, commands):
        super(PANEL, self).__init__()
        self.panel = panelIdentity
        self.panelAddr = panelAddr
        self.panelChnl = panelIdentity-1

        self.commands = dict()
        self.commands = commands

    def setRoomkey(self, roomKey ):
        self.roomKey = dict()
        self.roomKey = roomKey

    def pulloutput(self):
        print("Debugging_pulloutput to in emit.rawOutput to panelEndJob")
        self.rawOutput.emit( self.panel, str( outputChannel[self.panelChnl] ) )

    def checkstatus(self):
        print("Debugging_sending connect command to generate a rawOutput")
        self.thread = TUNNEL(self.panelChnl)
        self.thread.direct(self.commands["status"], self.panelAddr)
        self.thread.outputrdy.connect(lambda: self.pulloutput())
        self.thread.start()

    def interaction1(self):
        print("Debugging_sending int1 command to generate a rawOutput")
        self.thread = TUNNEL(self.panelChnl)
        self.thread.direct(self.roomKey["int1"], self.panelAddr)
        self.thread.outputrdy.connect(lambda: self.pulloutput())
        self.thread.start()

    def interaction2(self):
        print("Debugging_sending int2 command to generate a rawOutput")
        self.thread = TUNNEL(self.panelChnl)
        self.thread.direct(self.roomKey["int2"], self.panelAddr)
        self.thread.outputrdy.connect(lambda: self.pulloutput())
        self.thread.start()

    def reboot(self):
        print("Debugging_sending reboot command to generate a rawOutput")
        self.thread = TUNNEL(self.panelChnl)
        self.thread.direct(self.commands["reboot"], self.panelAddr)
        self.thread.outputrdy.connect(lambda: self.pulloutput())
        self.thread.start()

# ---------------------------------------------------- #
class ROOM(QtCore.QObject):
    '''
    PURPOSE:
    The system monitor for each room under the control system; wherein every room has its own dictionary of
    available commands, set as a room key. It is a host that directly routes its GUI button signals
    to the appropriate panel and reviews its status when the commands are complete - if a panel is
    actually associated. It raises a flag and prompts a GUI action when it identifies certain status strings.
    It must be initialized, setup with a room number, associated with a panel, and connected to GUI buttons
    in the grid of the same index. Within the context of a QObject.

    INPUTS:
    setup()
        - roomNumber: The internal ID of the room, identical to the index of the roomMonitor and the         (Int from GUI.setup)
                     index of the grid of GUI widgets associated with the room.
    associatePanel()
        - panel: The index of the panel from the selection drop down menu in the GUI grid for the room.      (Int from GUI.selectPanelR[])
                     The input is prompted by the flag raised when the user makes a selection. The value
                     is stored, so that the room remembers which panel it is hosting.
    reviewStats()
        - operation: The string written to the panel_status array to summarize the state of the panel        (String from GUI.XXX_Condition)
                     itself. It is based on predefined keywords agreed upon by convention; where each
                     keyword prompts a unique action. One of the places to update when creating new
                     user interactions or panel functions.

    OUTPUT:
    associatePanel()
        - retrieve: A flag containing the room number and the index of the PANEL object for the panel        (Signal [Int, Int] to GUI.retrievePanel)
                     being associated - raised when the user selects a panel from the room's panel
                     selection drop down menu. Counter-intuitive, but it prompts the system to make a
                     new set of commands available to the new and appropriate PANEL object.
    statuscheck_btn()/int1_btn()/int2_btn()
        - XXX_btntoggled: A flag containing the room number and the PANEL that is on file as being           (Signal [Int, Int] to GUI.XXX_btnCondition)
                     associated with the room. It is raised when one of the room's GUI buttons are
                     pressed and is routed through to the system to execute the appropriate command on
                     the associated PANEL itself.
    reviewStats()
        - XXX_status: A flag containing the room number and the PANEL object that is on file as being        (Signal [Int, Int] to GUI.XXX_statusCondition)
                     associated with the room. It is raised when the TUNNEL object the associated
                     PANEL created to fulfill a command directed by the system finishes running and
                     it raises its output ready flag local to the PANEL object. This signal directs the
                     system to update the GUI grid for the room with the panel in it to a COLOR depending
                     on the conclusion of the TUNNEL. Based on the specific output keyword.

                     **KEYWORDS**
                     AOK:   Successful Panel Event                              GREEN
                     SSH:   SSH Error                                           RED
                     ERR:   Panel Event Error                                   RED
                     UPD:   Panel Updating.                                     YELLOW
                     REST:  Panel Reseting
                     INT0:  Panel attempting to connect.                        YELLOW
                     INT1:  Panel conducting interaction1.                      BLUE
                     INT2:  Panel conducting interaction2.                      PURPLE

    DIRECT REFERENCE:
        - GUI.setup(): The GUI.roomMonitor array houses the ROOM objects for each of the room grids in the   (Class Method: Input(s))
                     the layout of the GUI. The drop down menu's index is connected to the associatePanel
                     function which activates the system retrievePanel function.
        - GUI.retrievePanel(): This function pushes the roomKey of the same room number to the PANEL         (Class Method: Output)
                     object being associated with the ROOM object. It is called when the retrieve flag
                     is emitted by the ROOM object when a new room is associated.
        - GUI.XXX_Condition(): This is the function that updates the panel_status array to reflect the
                     action the PANEL object is in the process of conducting.

    '''
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

    def reviewStats(self, operation="NULL"):
        print("Debugging_reviewStats\t\t for panel" + str(self.operatingPanel) + " in room" + str(self.identity+1) )
        self.status = operation

        if  (self.status=="AOK" or self.status=="CNCT"):
            self.AOKstatus.emit(self.identity, self.operatingPanel)
        elif(self.status=="ERR"):
            self.ERRstatus.emit(self.identity, self.operatingPanel)
        else:
            pass

# ---------------------------------------------------- #
class GUI(object):
    '''
    PURPOSE:
    Explanation of the reason for the object. Then, a description of the procedure required for the
    object to properly achieve its purpose; give the order of how the methods the object contains are
    employed. Mention package or module specific dependencies.

    INPUTS:
    function1()
        - input1 required for function 1: description&purpose                                                    (Type)
        - input2 required for function 1: description&purpose                                                    (Type)
    function2()
        - input3 required for function 2: description&purpose                                                    (Type)

    OUTPUT:
    function1()
        - output1 given by function1: description&purpose                                                        (Type)
    function3()
        - output2 given by function3: description&purpose                                                        (Type)

    DIRECT REFERENCE:
        - OBJECT1.functionA(): description of relationship, purpose for call                                     (Scope: Relation)
        - OBJECT1.functionB(): description of relationship, purpose for call                                     (Scope: Relation)
        - OBJECT2.functionA(): description of relationship, purpose for call                                     (Scope: Relation)
    '''

    def __init__(self, systems, file, commands):
        self.systems = systems

        self.commands = dict()
        self.commands = commands

        self.ipADDRS = dict()
        self.ipADDRS = self.getADDRs(file)

        self.panels=[]
        for index in range(self.systems):
            panelID = "panel" + str(index+1)
            self.panels.append( PANEL( index+1,
                                       self.ipADDRS[panelID],
                                       self.commands) )

        self.panel_status=[]
        # print("Initializing... " + str(self.systems) + " systems.")
        for index in range(systems):
            # Format: PANEL_STATE, ROOM_ASSOC, OUTPUT_STRING
            self.panel_status.append(["NULL", "NULL", ""])

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

        for i in range(0,4):
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
                self.roomMonitor[index].int1btntoggled.connect(self.interaction1btnCondition)
                self.roomMonitor[index].int2btntoggled.connect(self.interaction2btnCondition)
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

        # menu.addSeparator()
        # menu.addAction("Fetch Data from All", ControlSystem.close)
        # for index in range(0,12):
        #     actionItem = "Fetch from Room " + str(index+1)
        #     menu.addAction(actionItem, ControlSystem.close)
        for index in range(0, self.systems):
            actionItem = "Reset Panel " + str(index+1)
            menu.addAction(actionItem, self.panels[index].reboot)
        menu.addSeparator()
        menu.addAction("Show Full Screen", ControlSystem.showFullScreen)
        menu.addAction("Show Window", ControlSystem.showNormal)
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
        self.primaryGrid.addLayout(self.controlLayout, 0, 0, 4, 1)
        self.windowLayout.addLayout(self.primaryGrid)

        # -------------------------- Translate Text to Locality Language:
        self.initTranslateGUI(ControlSystem)

        # -------------------------- Arrange Connections:
        for index in range(self.systems):
            self.panels[index].rawOutput.connect(self.panelEndJob)

        for index in range(0, 12):
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

        for index in range(0,12):
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
            panel = "Panel IP:\t\t\t\t\t" + self.ipADDRS["panel"+str(index+1)]

            self.paddr[index].setText(_translate("ControlSystem", panel))
            self.poutput[index].setText(_translate("ControlSystem", self.panel_status[index][2]))
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
                name = "panel{}".format(i)             # Construct panel name
                IPs[ name ] = ip.strip('\n')        # Store into dictionary
                i=i+1                               # Increment counter
        return IPs

    # ---------------------------------------------------- #
    def retrievePanel(self, roomID, panelID):
        print("Debugging_retrievePanel for selection index" + str(panelID) + "_for room" + str(roomID+1))
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

            if  (self.panel_status[panelID][1] == "NULL"):
                self.statusR[roomID].clicked.connect(lambda: self.roomMonitor[roomID].statuscheck_btn() )
                self.int1R[roomID].clicked.connect(lambda: self.roomMonitor[roomID].int1_btn())
                self.int2R[roomID].clicked.connect(lambda: self.roomMonitor[roomID].int2_btn())
                self.panels[panelID].setRoomkey(keyChain[roomID])
                self.panel_status[panelID][1] = "R" + str(roomID)
            else:
                prevAssoc = int( self.panel_status[panelID][1].strip('R') )
                self.selectPanelR[prevAssoc].setCurrentIndex(0)
                self.statusR[prevAssoc].clicked.disconnect()
                self.int1R[prevAssoc].clicked.disconnect()
                self.int2R[prevAssoc].clicked.disconnect()

                self.statusR[roomID].clicked.connect(lambda: self.roomMonitor[roomID].statuscheck_btn() )
                self.int1R[roomID].clicked.connect(lambda: self.roomMonitor[roomID].int1_btn())
                self.int2R[roomID].clicked.connect(lambda: self.roomMonitor[roomID].int2_btn())
                self.panels[panelID].setRoomkey(keyChain[roomID])
                self.panel_status[panelID][1] = "R" + str(roomID)

    # ---------------------------------------------------- #
    def AOKstatusCondition(self, roomID, panelID):
        print("Debugging_AOKstatusCondition\t for panel" + str(panelID) + " in room" + str(roomID+1) )
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate

        if self.statusR[roomID].isChecked():
            self.statusR[roomID].setText(_translate("ControlSystem", "Ready"))
            self.statusR[roomID].setStyleSheet(self.greenbg)
            self.room[roomID].setStyleSheet(self.greenbg)

            self.statusR[roomID].setEnabled(True)
            self.int1R[roomID].setEnabled(True)
            self.int2R[roomID].setEnabled(True)
        else:
            pass

    # ---------------------------------------------------- #
    def ERRstatusCondition(self, roomID, panelID):
        print("Debugging_ERRstatusCondition\t for panel" + str(panelID) + " in room" + str(roomID+1) )
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
    def statbtnCondition(self, roomID, panelID):
        print("Debugging_statbtnCondition\t for panel" + str(panelID) + " in room" + str(roomID+1) )
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate
        if self.statusR[roomID].isChecked():
            self.room[roomID].setStyleSheet(self.yellowbg)

            self.statusR[roomID].setEnabled(False)
            self.statusR[roomID].setStyleSheet(self.yellowbg)
            self.statusR[roomID].setText(_translate("ControlSystem", "Connecting..."))

            self.panel_status[panelIdx][0] = "CNCT"
            self.panel_status[panelIdx][2] = "Connecting...\n"
            self.poutput[panelIdx].setText(_translate("ControlSystem", self.panel_status[panelIdx][2]))
            self.panels[panelIdx].checkstatus()
        else:
            self.statusR[roomID].setText(_translate("ControlSystem", "Connect"))
            self.statusR[roomID].setStyleSheet(self.greybg)
            self.room[roomID].setStyleSheet(self.greybg)
            self.int1R[roomID].setEnabled(False)
            self.int2R[roomID].setEnabled(False)

    # ---------------------------------------------------- #
    def interaction1btnCondition(self, roomID, panelID):
        print("Debugging_int1btnCondition\t for panel" + str(panelID) + " in room" + str(roomID+1) )
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate

        if self.statusR[roomID].isChecked():
            self.room[roomID].setStyleSheet(self.bluebg)

            self.statusR[roomID].setEnabled(False)
            self.statusR[roomID].setStyleSheet(self.bluebg)
            self.statusR[roomID].setText(_translate("ControlSystem", "Running Int: 1"))

            self.int1R[roomID].setEnabled(False)
            self.int2R[roomID].setEnabled(False)

            self.panel_status[panelIdx][0] = "INT1"
            self.panel_status[panelIdx][2] = "Interaction 1...\n"
            self.poutput[panelIdx].setText(_translate("ControlSystem", self.panel_status[panelIdx][2]))
            self.panels[panelIdx].interaction1()

        else:
            pass

    # ---------------------------------------------------- #
    def interaction2btnCondition(self, roomID, panelID):
        print("Debugging_int2btnCondition\t for panel" + str(panelID) + " in room" + str(roomID+1) )
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate

        if self.statusR[roomID].isChecked():
            self.room[roomID].setStyleSheet(self.purpbg)

            self.statusR[roomID].setEnabled(False)
            self.statusR[roomID].setStyleSheet(self.purpbg)
            self.statusR[roomID].setText(_translate("ControlSystem", "Running Int: 2"))

            self.int1R[roomID].setEnabled(False)
            self.int2R[roomID].setEnabled(False)

            self.panel_status[panelIdx][0] = "INT2"
            self.panel_status[panelIdx][2] = "Interaction 2...\n"
            self.poutput[panelIdx].setText(_translate("ControlSystem", self.panel_status[panelIdx][2]))
            self.panels[panelIdx].interaction2()

        else:
            pass

    # ---------------------------------------------------- #
    def panelEndJob(self, panelID, rawMessage):
        print("Debugging_panelEndJob\t\t for panel" + str(panelID))
        panelIdx = panelID - 1
        _translate = QtCore.QCoreApplication.translate

        edits = rawMessage.strip("b'")
        review = edits.split("\\n")
        message = edits.replace("\\n", "\n")
        message = "\n" + message

        if( rawMessage == "b'CNCT\\n'" ):
            self.panel_status[panelIdx][0] = "CNCT"
            message = "Connected to Panel " + str(panelID) + "..."
        else:
            # **KEYWORDS**
            # AOK:   Successful Panel Event                              GREEN
            # SSH:   SSH Error                                           RED
            # ERR:   Panel Event Error                                   RED
            # DONE:  Panel Updating.                                     YELLOW

            if any("AOK" in s for s in review):
                self.panel_status[panelIdx][0] = "AOK"
            elif any("DONE" in s for s in review):
                self.panel_status[panelIdx][0] = "DONE"
            else:
                self.panel_status[panelIdx][0] = "ERR"

        if(self.panel_status[panelIdx][1] == "NULL"):
            pass
        else:
            operation = self.panel_status[panelIdx][0]
            roomID = int( self.panel_status[panelIdx][1].strip('R') )
            self.roomMonitor[roomID].reviewStats(operation)

        self.panel_status[panelIdx][2] = self.panel_status[panelIdx][2] + "Panel Output:\n" + message
        self.poutput[panelIdx].setText(_translate("ControlSystem", self.panel_status[panelIdx][2]))

# -------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":

    # ---------------------------------------------------- #
    # Standard Commands Available to All Panels
    STDCMDS = {
    "reboot"    : "sudo reboot",
    "status"    : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/connectionTest.py",
    "normcon"   : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/consys4.3.py",
    "normbpc"   : "DISPLAY=:0 python pd3d/csec/repos/ControlSystem/Software/Python/consys/consys4.3bpc.py -s 0 -st 30 -lp 85 -hp 145",
    }

    # ---------------------------------------------------- #
    # Room 1 Shell Command Key :
    roomKey1 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status5.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/aokTest.py"
    }

    # Room 2 Shell Command Key :
    roomKey2 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/connectionTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status5.py"
    }

    # Room 3 Shell Command Key :
    roomKey3 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/status5.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/errorTest.py"
    }

    # Room 4 Shell Command Key :
    roomKey4 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/aokTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/errorTest.py"
    }

    # Room 5 Shell Command Key :
    roomKey5 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/connectionTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/aokTest.py"
    }

    # Room 6 Shell Command Key :
    roomKey6 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/aokTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/aokTest.py"
    }

    # Room 7 Shell Command Key :
    roomKey7 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/aokTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/connectionTest.py"
    }

    # Room 8 Shell Command Key :
    roomKey8 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/errorTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/errorTest.py"
    }

    # Room 9 Shell Command Key :
    roomKey9 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/errorTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/aokTest.py"
    }

    roomKey10 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/aokTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/errorTest.py"
    }

    roomKey11 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/connectionTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/errorTest.py"
    }

    roomKey12 = {
    "int1" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/errorTest.py",
    "int2" : "python pd3d/csec/repos/ControlSystem/Software/Python/consys/connectionTest.py"
    }


    global keyChain
    keyChain = [ roomKey1, roomKey2, roomKey3, roomKey4, roomKey5, roomKey6, roomKey7, roomKey8, roomKey9, roomKey10, roomKey11, roomKey12 ]

    # ---------------------------------------------------- #
    # CSEC Testing Setup Properties :
    PANELS = 12
    FILE = "AddressBook.csv"

    global outputChannel
    outputChannel = []
    for index in range(PANELS):
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
