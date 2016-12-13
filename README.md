# Control System
The Control System (CS) module of our Smart Instrument Panel (SIP) consists of a micro-computer/controller equipped with WiFi and Bluetooth antennas, and Ethernet and USB ports for the <b> relay and collection of data </b> to/from the Control Room (CR) and other Smart Devices (SDs) integrated to the SIP.

## Functionality
The CS;
> + Receives direct commands from the CR <br />
> + Translates CR commands into scenario instructions via the configuration XML <br />
> + Relays scenario instructions to integrated SDs <br />
> + Retrieves SDs data after termination of scenario <br />

### Command Relay
The CS mediates the commands sent from the CR. Mediation encompasses: <b>receipt</b>, <b>translation</b> and <b>transmission</b>.<br />
><b>1.0</b> The CS receives a command from the CR. For instance, "Run Scenario #5" (Figure 1) <br />
><b>2.0</b> Using the XML configuration file, the CS; <br />

>><b>2.1</b> Identifies itself within a list of SIPs and CSs <br />
>><b>2.2</b> Identifies input scenario within an indexed list of scenarios <br />
>><b>2.3</b> Pulls list of SDs integrated to the corresponding SIP <br />
>><b>2.4</b> Pulls scenario instructions and parameters to be sent to the SDs <br />

><b>3.0</b> Triggers SDs as specified by scenario instructions and parameters <br />

![OPERATION](https://github.com/pd3d/ControlSystem/blob/master/Documentation/Operation/operation001.png)
<b> Figure 1. Command Relay Diagram </b>
