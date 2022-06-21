#!/usr/bin/python3

'''
For wms6 with Python3.9
Script requires module "psutil" for Python3.9

wget http://ftp.de.debian.org/debian/pool/main/p/python-psutil/python3-psutil_5.8.0-1_amd64.deb
dpkg -i ./python3-psutil_5.8.0-1_amd64.deb
'''

#It is check for file handler per process.
#And it is not plugin. Please place this file into local folder
#noc@wildix.com

import psutil
import os, os.path

CritLevel = 70
WarnLevel = 60
checkName = "File_handlers"
checkmkOutput=""
failsWarn = []
failsCrit = []
unknown = False
for proc in psutil.process_iter():
	try:
		processName = proc.name()
		processID = str(proc.pid)
		limitsData = ""
		with open('/proc/'+processID+'/limits') as f:
			for line in f:
				if line.find("Max open files") != -1:
					limitsData = line.replace("Max open files  "," ")
		while True:
			if limitsData.find("  ") == -1:
				break
			else:
				limitsData = limitsData.replace("  "," ")
		limitsData = limitsData.split(" ",2)
		if limitsData[0]=="":
			softLimit = int(limitsData[1])
		else:
			softLimit = int(limitsData[0])
		DIR ='/proc/'+processID+'/fd/'
		currentUsage = len([name for name in os.listdir(DIR)])
		if softLimit>0:
			currentUsagePercent = round(float(currentUsage)/softLimit*100,2)
		else:
			currentUsagePercent = 0
		if currentUsagePercent > CritLevel:
			failsCrit.append([str(processName)+"["+str(processID)+"]", currentUsagePercent, currentUsage, softLimit])
		elif currentUsagePercent > WarnLevel:
			failsWarn.append([str(processName)+"["+str(processID)+"]", currentUsagePercent, currentUsage, softLimit])
	except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
		unknown = True
if len(failsCrit)>0:
	checkmkOutput = "2 " + checkName + " - CRIT " + " ".failsWarn.join(failsCrit)
elif len(failsWarn)>0:
	checkmkOutput = "1 " + checkName + " - WARN " + " ".failsWarn.join(failsWarn)
elif unknown == False:
	checkmkOutput = "0 " + checkName + " - OK: file handlers usage is lower then " + str(WarnLevel) + "% "
else:
	checkmkOutput = "3 " + checkName + " - UNKNOWN: more likely agent has insufficients rights"

print(checkmkOutput)
