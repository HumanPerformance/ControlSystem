"""
protocolDefinitions.py

The following module consists of a list of commands or definitions to be used in the communication between devices and the control system

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/26/2016
"""
# Definition                    Name                        Value           Class
# ----------                    ----                        -----           -----
CHK = chr(0x01)         #       System Check                0x01            ORG     
ENQ = chr(0x05)         #       Enquiry                     0x05            STD
EOT = chr(0x04)         #       End of Transmission         0x04            STD
ACK = chr(0x06)         #       Positive Acknowledgement    0x06            STD
NAK = chr(0x15)         #       Negative Acknowledgement    0x15            STD
CAN = chr(0x18)         #       Cancel Current Command      0x18            STD
ESC = chr(0x1B)         #       Escape                      0x1B            STD
DC1_STRTREC = chr(0x11) #       Start Recording             0x11            ORG
DC2_STPREC = chr(0x12)  #       Stop Recording              0x12            ORG
DC3_STRTPLY = chr(0x13) #       Start Playback              0x13            ORG
DC4_STPPLY = chr(0x14)  #       Stop Playback               0x14            ORG

# Legend
# STD - Standard terminology / Standard reference for command
# ORG - Original or custom-made command and reference
