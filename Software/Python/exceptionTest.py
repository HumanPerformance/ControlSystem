"""
Exception Test
"""

try:
    rfObject.readline()
except Exception as instance:
    eType = type(instance)
    print eType
