import RPi.GPIO as GPIO ## Import GPIO library

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
button = 40

GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
count = 0

while True:
	GPIO.wait_for_edge(button, GPIO.FALLING)
	count += 1
	print "button pressed", count, "times"

GPIO.cleanup()

print "Done" ## When loop is complete, print "Done"