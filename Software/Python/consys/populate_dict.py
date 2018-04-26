#
# Populate dict variable with a list obtained
# from an external file
#

fileName = "ip_addrs.csv"                   # File where IP's are stored (doesn't have to be .csv)
panel_ip = dict()                           # Create empty dictionary
i=1                                         # Start counter

with open( fileName, 'r' ) as f:            # Open file 
    for ip in f:                            # Iterate over the contents
        name = "panel{}".format(i)          # Construct panel name
        panel_ip[ name ] = ip.strip('\n')   # Store into dictionary
        i=i+1                               # Increment counter
