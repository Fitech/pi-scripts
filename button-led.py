import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(15, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
button = 40

GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)

GPIO.output(15,True)## Switch on pin 15

GPIO.wait_for_edge(button, GPIO.FALLING)

GPIO.output(15,False)## Switch off pin 15

GPIO.cleanup()

print "Done" ## When loop is complete, print "Done"