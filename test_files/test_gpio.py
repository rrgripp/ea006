import RPi.GPIO as GPIO
import time

# setting a current mode
GPIO.setmode(GPIO.BCM)

#removing the warings 
GPIO.setwarnings(False)

#creating a list (array) with the number of GPIO's that we use 
pin = 14

#setting the mode for all pins so all will be switched on 
GPIO.setup(pin, GPIO.OUT)

#setting the GPIO to HIGH or 1 or true
GPIO.output(pin,  GPIO.HIGH)

#wait 0,5 second
time.sleep(0.5)

#setting the GPIO to LOW or 0 or false
GPIO.output(pin,  GPIO.LOW)

#wait 0,5 second
time.sleep(0.5)

#cleaning all GPIO's 
GPIO.cleanup()