import subprocess
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread

# Edit these for how many people/devices you want to track
occupant = ["NOME"]

# MAC addresses for our phones
address = ["00:00:00:00:00:00"]

#GPIO pin that we use 
pin = 14

# Sleep once right when this script is called to give the Pi enough time
# to connect to the network
#sleep(60)

# Some arrays to help minimize streaming and account for devices
# disappearing from the network when asleep
firstRun = [1] * len(occupant)
presentSent = [0] * len(occupant)
notPresentSent = [0] * len(occupant)
counter = [0] * len(occupant)

def initGPIO():
    # setting a current mode
    GPIO.setmode(GPIO.BCM)

    #removing the warings 
    GPIO.setwarnings(False)

    #setting the mode for all pins so all will be switched on 
    GPIO.setup(pin, GPIO.OUT)

def turnOn():
    #setting the GPIO to HIGH or 1 or true
    GPIO.output(pin,  GPIO.LOW)

def turnOff():
    #setting the GPIO to LOW or 0 or false
    GPIO.output(pin,  GPIO.HIGH)

def finishGPIO():
    #cleaning all GPIO's 
    GPIO.cleanup()


initGPIO()
turnOff()

# Function that checks for device presence
def whosHere(i):

    # 5 second pause to allow main thread to finish arp-scan and populate output
    sleep(10)

    # Loop through checking for devices and counting if they're not present
    while True:

        # Exits thread if Keyboard Interrupt occurs
        if stop == True:
            print("Exiting Thread")
            finishGPIO()
            exit()
        else:
            pass

        # If a listed device address is present print and stream
        if address[i] in output:
            print(occupant[i] + "'s device is connected to your network")
            if presentSent[i] == 0:
                print(occupant[i] + " present streamed")
                turnOn()
                # Reset counters so another stream isn't sent if the device
                # is still present
                firstRun[i] = 0
                presentSent[i] = 1
                notPresentSent[i] = 0
                counter[i] = 0
                sleep(5)
            else:
                # If a stream's already been sent, just wait for 15 minutes
                counter[i] = 0
                sleep(5)
        # If a listed device address is not present, print and stream
        else:
            print(occupant[i] + "'s device is not present")
            # Only consider a device offline if it's counter has reached 5
            # This is the same as 15 minutes passing
            if counter[i] == 5 or firstRun[i] == 1:
                turnOff()
                firstRun[i] = 0
                if notPresentSent[i] == 0:
                    # Stream that device is not present
                    print(occupant[i] + " not present streamed")
                    # Reset counters so another stream isn't sent if the device
                    # is still present
                    notPresentSent[i] = 1
                    presentSent[i] = 0
                    counter[i] = 0
                else:
                    # If a stream's already been sent, wait 5 seconds
                    counter[i] = 0
                    sleep(5)
            # Count how many 5 second intervals have happened since the device 
            # disappeared from the network
            else:
                counter[i] = counter[i] + 1
                print(occupant[i] + "'s counter at " + str(counter[i]))
                sleep(5)


# Main thread

try:

    # Initialize a variable to trigger threads to exit when True
    global stop
    stop = False

    # Start the thread(s)
    # It will start as many threads as there are values in the occupant array
    for i in range(len(occupant)):
        t = Thread(target=whosHere, args=(i,))
        t.start()

    while True:
        # Make output global so the threads can see it
        global output
        # Assign list of devices on the network to "output"
        output = subprocess.getoutput("sudo arp-scan -l")
        # Wait 5 seconds between scans
        sleep(5)

except KeyboardInterrupt:
    # On a keyboard interrupt signal threads to exit
    stop = True
    finishGPIO()
    exit()
