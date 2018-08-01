"""
protocolDefinitions.py

The following module consists of a list of commands or definitions to be used in the communication between devices and the control system

Michael Xynidis
Fluvio L Lobo Fenoglietto
11/10/2017
"""


### ASCII Byte Codes -- used for communication protocol
## General Commands
ENQ		= chr(0x05)       # Enquiry: "Are you ready for commands?"										[resp: ACK | NAK]
ACK             = chr(0x06)       # Positive Acknowledgement: "Command/Action successful."						[resp: ACK | NAK]
NAK             = chr(0x15)       # Negative Acknowledgement: "Command/Action UNsuccessful."					[resp: ACK | NAK]

### Device Control Commands
## Diagnostic Functions ============================================================================================================= //
DEVICEID       	= chr(0x11)       # Device Identification                                    					[resp: Device Code]
SDCHECK         = chr(0x12)       # System Check: "Run system check and report"              					[resp: ACK | NAK]
SENDWAV         = chr(0x13)       # Send .WAV file (audio recording) via serial port         					[resp: ACK | NAK]
DELVOLATILE     = chr(0x14)       # Erase volatile files (all)                               					[resp: ACK | NAK]
SENDRAW         = chr(0x37)       # send raw file...

## Device-Specific Functions ======================================================================================================== //                     
STARTREC        = chr(0x16)       # Start Recording                                          				[resp: ACK | NAK]
STARTCREC       = chr(0x32)       # Start Custom Recording                                                              [resp: ACK | NAK]         
STARTMREC       = chr(0x38)
STOPREC         = chr(0x17)       # Stop Recording                                           				[resp: ACK | NAK]
STARTPLAY       = chr(0x18)       # Start Playback                                           				[resp: ACK | NAK]
STOPPLAY        = chr(0x19)       # Stop Playback                                            				[resp: ACK | NAK]
STARTHBMONITOR  = chr(0x1B)       # Start Monitoring Heart Beat                              				[resp: ACK | NAK]
STOPHBMONITOR   = chr(0x1C)       # Stop Monitoring Heart Beat                               				[resp: ACK | NAK]
STARTBLEND      = chr(0x1F)       # Start Blending
STOPBLEND       = chr(0x20)       # Stop Blending
PSTRING         = chr(0x31)       # Parse String
RECMODE         = chr(0x41)       # Parse recording mode
SETIDLE         = chr(0x26)       # set to idle

## Simulation Functions ============================================================================================================= // 
AORSTE          = chr(0x50)         # Aortic stenosis
S4GALL          = chr(0x51)         # S4 gallop
ESMSYN          = chr(0x52)         # Playback of Synthetic, Early Systolic Heart Murmur                 			[resp: ACK | NAK]
KOROT1          = chr(0x53)         # Playback of Korotkoff Sound                                        			[resp: ACK | NAK]
KOROT2          = chr(0x54)         # Playback of Korotkoff Sound                                        			[resp: ACK | NAK]
KOROT3          = chr(0x55)         # Playback of Korotkoff Sound                                        			[resp: ACK | NAK]
KOROT4          = chr(0x56)         # Playback of Korotkoff Sound                                        			[resp: ACK | NAK]
RECAOR          = chr(0x57)         # ...
RECMIT          = chr(0x58)         # ...
RECPUL          = chr(0x59)         # ...
RECTRI          = chr(0x60)         # ...

STARTSIM        = chr(0x70)       # simulation byte
STOPSIM         = chr(0x71)       # simulation byte
