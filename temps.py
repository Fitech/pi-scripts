#!/usr/bin/env python3

import os
import glob
import time
import MySQLdb
from datetime import datetime, date
from time import strftime
from mixpanel import Mixpanel

mp = Mixpanel('60dff8e0ce93d4470ab7ff10bc9d5142')

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Variables for MySQL
db = MySQLdb.connect(host="localhost", user="root",passwd="WatchTheOilBurner451", db="temperatures")
cur = db.cursor()

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_f

readingAB = "A"
tempAf = 0
tempBf = 0
 
while True:

	if readingAB == "A":
		tempBf = tempBf+.5
		tempAf = read_temp()
		tempA = str(tempAf)
		print(tempA)
		if (tempAf > tempBf):
			burnerOn = 'TRUE'
		else:
			burnerOn = 'FALSE'

		nextRead = "B"
		datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
		print datetimeWrite
		sql = ("""INSERT INTO tempLog (datetime,temperature,burner_on) VALUES (%s,%s,%s)""",(datetimeWrite,tempA,burnerOn))
		print "temp A"

		mp.track('pi', 'Temp Reading', {
		    'Temperature': tempA,
		    'Burner': burnerOn
		})
		
		print sql
		try:
			print "Writing to database..."
			# Execute the SQL command
			cur.execute(*sql)
			# Commit your changes in the database
			db.commit()
			print "Write Complete"

		except:
			# Rollback in case there is any error
			db.rollback()
			print "Failed writing to database"

	else:
		tempAf = tempAf+.5
		tempBf = read_temp()
		tempB = str(tempBf)
		print(tempB)
		if (tempBf > tempAf):
			burnerOn = 'TRUE'
		else:
			burnerOn = 'FALSE'

		nextRead = "A"
		datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
		print datetimeWrite
		sql = ("""INSERT INTO tempLog (datetime,temperature,burner_on) VALUES (%s,%s,%s)""",(datetimeWrite,tempB,burnerOn))
		print "temp B"

		mp.track('pi', 'Temp Reading', {
		    'Temperature': tempB,
		    'Burner': burnerOn
		})

		print sql
		try:
			print "Writing to database..."
			# Execute the SQL command
			cur.execute(*sql)
			# Commit your changes in the database
			db.commit()
			print "Write Complete"

		except:
			# Rollback in case there is any error
			db.rollback()
			print "Failed writing to database"

	readingAB = nextRead
	time.sleep(180)
