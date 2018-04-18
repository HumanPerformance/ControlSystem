"""
protocolDefinitions.py

The following module consists of a list of commands or definitions to be used in the communication between devices and the control system

Michael Xynidis
Fluvio L Lobo Fenoglietto
09/26/2016
"""
# Definition                            Name                                                Value           Class
# ----------                            ----                                                -----           -----
ENQ = chr(0x05)                 #       Enquiry                                             0x05            STD
EOT = chr(0x04)                 #       End of Transmission                                 0x04            STD
ACK = chr(0x06)                 #       Positive Acknowledgement                            0x06            STD
NAK = chr(0x15)                 #       Negative Acknowledgement                            0x15            STD
CAN = chr(0x18)                 #       Cancel Current Command                              0x18            STD

# Device Control Commands
#   We have extended the four (4) standard "device control" commands by means of a two-byte communication protocol

DC1 = chr(0x11)                 #       Device Identification
#                                                                                           0xFF            ORG

DC2 = chr(0x12)                 #       Start Data Stream                                   0x12            STD
#                                                                                           0xFF            ORG

DC3 = chr(0x13)                 #       Stop Data Stream                                    0x01            ORG
#                                                                                           0xFF            ORG

DC4 = chr(0x14)                 #       Simulation Functions                                0x14            STD
#                                                                                           0xFF            ORG

# Legend
# STD - Standard terminology / Standard reference for command
# ORG - Original or custom-made command and reference
