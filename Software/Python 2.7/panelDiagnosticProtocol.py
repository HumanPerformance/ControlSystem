"""
panelDiagnosticProtocol.py

Panel Diagnostic Protocol

The following module contains functions used to diagnosed the status of an instrument panel and its associated devices/modules

Fluvio L. Lobo Fenoglietto
01/11/2017
"""

# ==============================================
# Import Libraries and/or Modules
# ==============================================
# Python modules
import  sys
import  os
import  serial
import  time
from    os.path                import expanduser

# PD3D Modules
from    timeStamp              import fullStamp
from    configurationProtocol  import *
