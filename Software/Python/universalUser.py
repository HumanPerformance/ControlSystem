"""
universalUser.py

The following script has been design to demo the capability of automatically detecting the user directory of a linux operating system so that programs run easily across devices

Fluvio L. Lobo Fenoglietto 05/22/2016
"""

from os.path import expanduser

home = expanduser("~")
print home


"""
References
1- Automaticcally detect the home and user folder of the device/os - http://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
"""
