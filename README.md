# Control System
The Control System (CS) module of our Smart Instrument Panel (SIP) consists of a micro-computer/controller equipped with WiFi and Bluetooth antennas, and Ethernet and USB ports for the <b> relay and collection of data </b> to/from the Control Room (CR) and other Smart Devices (SDs) integrated to the SIP.

## Functionality
The CS;
> Receives direct commands from the CR <br />
> Translates CR commands into scenario instructions via the configuration XML <br />
> Relays scenario instructions to integrated SDs <br />
> Retrieves SDs data after termination of scenario <br />

### Command Relay
The CS mediates the commands sent from the CR. Mediation encompasses: <b>receipt</b>, <b>translation</b> and <b>transmission</b>.
> 1. The CS receives a command 
![OPERATION](https://github.com/pd3d/ControlSystem/blob/master/Documentation/Operation/operation001.png)
