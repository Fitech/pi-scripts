import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
button = 40

GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
count = 0

while True:
	input_state = GPIO.input(button)
	if input_state == False:
		count += 1
		print "button pressed", count, "times"
		time.sleep(0.2)

GPIO.cleanup()

print "Done" ## When loop is complete, print "Done"