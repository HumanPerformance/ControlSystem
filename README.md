# Control System
The Control System (CS) module of our Smart Instrument Panel (SIP) consists of a micro-computer/controller equipped with WiFi and Bluetooth antennas, and Ethernet and USB ports for the <b> relay and collection of data </b> to/from the Control Room (CR) and other Smart Devices (SDs) integrated to the SIP.

## Within our Family of Devices
Device hierarchy has been defined by control and represented below through indentations. For instance, the CS has control over the Smart Stethoscope (SS).
> Smart Instrument Panel (SIP)
>> <b> Control System (CS) </b> 
>>> Smart Stethoscope (SS) <br />
>>> Smart Thermometer (ST) <br />
>>> Smart Oximeter (SO) <br />
>>> Smart Scope Panel (SSP)
>>>> Smart Handle (SH)

## Functionality
The CS;
> + Receives direct commands from the CR <br />
> + Translates CR commands into scenario instructions via the configuration XML <br />
> + Relays scenario instructions to integrated SDs <br />
> + Retrieves SDs data after termination of scenario <br />

### Command Relay
The CS mediates the commands sent from the CR. Mediation encompasses: <b>receipt</b>, <b>translation</b> and <b>transmission</b>.<br />
><b>1.0</b> The CS receives a command from the CR. For instance, "Run Scenario #5"<br />
><b>2.0</b> Using the XML configuration file, the CS; <br />

>><b>2.1</b> Identifies itself within a list of SIPs and CSs <br />
>><b>2.2</b> Identifies input scenario within an indexed list of scenarios <br />
>><b>2.3</b> Pulls list of SDs integrated to the corresponding SIP <br />
>><b>2.4</b> Pulls scenario instructions and parameters to be sent to the SDs <br />

><b>3.0</b> Triggers SDs as specified by scenario instructions and parameters <br />

In other words, the process of <b>receipt</b> (as the name indicates) consists of receiving commands or messages from the CR.
The proces of <b>translation</b> consists on using the information from the CR command to access the configuration XML and extract the instrument list, scenario instructions and parameters, which are then passed to the SDs as part of the <b>transmission</b>. The entire process has been depicted in <b>Figure 1</b>.

![OPERATION](https://github.com/pd3d/ControlSystem/blob/master/Documentation/Operation/operation001.png)
<b> Figure 1. Command Relay Diagram </b>
