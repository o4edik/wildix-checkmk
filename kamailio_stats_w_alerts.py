#!/bin/python3 

import subprocess
import json

numberOfRegistrations=subprocess.check_output('kamctl online | wc -l', shell=True)
webSockets=subprocess.check_output('kamcmd ws.dump | grep "ws:" | wc -l',shell=True)
sharedMemory=subprocess.check_output('kamctl stats shmem', shell=True)

totalMemorySize = 0
usedMemorySize = 0
maxUsedSize = 0
fragments = 0
freeMemSize = 0
MB = 1024*1024
#msm_perc = 5.0
# The usedMemorySize tresholds for an alerts (added by Ed Ocheretnyi)
o = 2.30 # treshold for usedMemorySize as % from totalMemorySize (e.g. 2.3%)
w = 3.00 # warning treshold for usedMemorySize as % from totalMemorySize (e.g. 2.3%)

# The tresholds for an alerts of maxUsedSize memory
a = 2.8
b = 4.0



data = json.loads(sharedMemory)
for el in data:
	if el == "result":
		usedMemorySize = data[el][5][18:]
		totalMemorySize = data[el][4][19:]
		maxUsedSize = data[el][2][22:]
		freeMemSize = data[el][1][18:]
		fragments = data[el][0][18:]
       # Convert bytes in to Mbytes for futher convenient usage in checkmk 
		usedMemorySizeMB =  round(int(usedMemorySize)/MB,2)
		totalMemorySizeMB = round(int(totalMemorySize)/MB,2)		
		maxUsedSizeMB = round(int(maxUsedSize)/MB,2)
		freeMemSizeMB = round(int(freeMemSize)/MB,2)
		usm_perc = round((1-(totalMemorySizeMB - usedMemorySizeMB)/totalMemorySizeMB)*100,2) # calculate the % of usedMemorySize allocated in totalMemorySizeMB
		msm_perc = round((maxUsedSizeMB/totalMemorySizeMB)*100,2)  # calculate % of maxUsedSize allocated in totalMemorySizeMB


#print ("0 kamailio_max_used_shared_memory count="+str(maxUsedSizeMB)+ " " + str(maxUsedSizeMB))
print ("0 kamailio_free_memory_size count="+str(freeMemSizeMB)+ " " + str(freeMemSizeMB))
print ("0 kamailio_total_shared_memory count="+str(totalMemorySizeMB)+ " " + str(totalMemorySizeMB))

print ("0 kamailio_fragments count="+str(fragments)+ " " + str(fragments))
print ("0 kamailio_number_of_registrations count="+str(int(numberOfRegistrations[:-1]))+" "+str(int(numberOfRegistrations[:-1])))
print ("0 kamailio_web_sockets count="+str(webSockets[:-1]) + " "+str(webSockets[:-1]))

if usm_perc <= o:
	print ("0 kamailio_used_shared_memory count=" " "+str(usedMemorySizeMB)+ " " + str(usedMemorySizeMB))
elif o <= usm_perc <= w:
	print ("1 kamailio_used_shared_memory count=" " "+str(usedMemorySizeMB)+ " " + str(usedMemorySizeMB))
else:
	print ("2 kamailio_used_shared_memory count=" " "+str(usedMemorySizeMB)+ " " + str(usedMemorySizeMB))

if msm_perc <= a:
    print("0 kamailio_max_used_shared_memory count="+str(maxUsedSizeMB)+ " " + str(maxUsedSizeMB))
elif a <= msm_perc <= b:
    print("1 kamailio_max_used_shared_memory count="+str(maxUsedSizeMB)+ " " + str(maxUsedSizeMB))
else:
    print("2 kamailio_max_used_shared_memory count="+str(maxUsedSizeMB)+ " " + str(maxUsedSizeMB))
