# Augmented Stethoscope Implementation
The operation of the Augmented Stethoscope (AS) relies on python scripts and modules laid-out in this directory.

> **NOTE:** All of the python scripts, modules, and functions in this repository have been optimized for the Raspberry Pi hardware and Raspbian OS

---
## Requirements
1.  Install the _python-bluez_ library
    ```
    sudo apt install python-bluez
    ```
    
---   
## Troubleshooting

*   **ERROR:** `ImportError: No module named bluetooth`
    *   **WHEN:** Executing **ANY** python script importing _stethoscopeBTProtocol.py_
    *   **PROBLEM:** The _python-bluez_ library has nopt been installed
    *   **SOLUTION:** Install _python-bluez_ as shown under **Requirement #1**
