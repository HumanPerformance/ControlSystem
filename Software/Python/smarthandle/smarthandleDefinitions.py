"""
smarthandleDefinitions.py

04/18/2018 Upgraded the protocol definitions for the smart handles

Fluvio L Lobo Fenoglietto
04/18/2018
"""
# Definition                            Name                                                Value           Class
# ----------                            ----                                                -----           -----
ID    = "sh"                            # Device ID for the smart handles
START = "g"                             # START data collection                             "g"             ORG
STOP  = "s"                             # STOP data collection                              "s"             ORG

"""
ENQ = chr(0x05)                 #       Enquiry                                             0x05            STD
EOT = chr(0x04)                 #       End of Transmission                                 0x04            STD
ACK = chr(0x06)                 #       Positive Acknowledgement                            0x06            STD
NAK = chr(0x15)                 #       Negative Acknowledgement                            0x15            STD
CAN = chr(0x18)                 #       Cancel Current Command                              0x18            STD
"""
