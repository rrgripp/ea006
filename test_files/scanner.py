import subprocess
import re
from time import sleep
from threading import Thread

#pattern = re.compile(r'([0-9a-fA-F]{2}\:){5}[0-9a-fA-F]{2}')
pattern = re.compile(r'[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}\:[0-9a-fA-F]{2}')

# Function that checks for device presence
def check():

    # 30 second pause to allow main thread to finish arp-scan and populate output
    sleep(10)

    # Loop through checking for devices and counting if they're not present
    while True:

        # Exits thread if Keyboard Interrupt occurs
        if stop == True:
            print("Exiting Thread")
            exit()
        else:
            pass
        
        mac_addressess = re.findall(pattern, output)
        
        print(mac_addressess)
        
        devices = len(mac_addressess) - 2
        print(str(devices) + " dispositivos conectados")
        sleep(10)

# Main thread

try:

    # Initialize a variable to trigger threads to exit when True
    global stop
    stop = False

    # Start the thread(s)
    # It will start as many threads as there are values in the occupant array
    t = Thread(target=check)
    t.start()

    while True:
        # Make output global so the threads can see it
        global output
        # Assign list of devices on the network to "output"
        output = subprocess.getoutput("sudo arp-scan -l")
        # Wait 30 seconds between scans
        sleep(10)

except KeyboardInterrupt:
    # On a keyboard interrupt signal threads to exit
    stop = True
    exit()

