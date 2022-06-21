
#!/usr/bin/env python 

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

data = json.loads(sharedMemory)
for el in data:
	if el == "result":
		usedMemorySize = data[el][5]
		totalMemorySize = data[el][4]
		maxUsedSize = data[el][2]
		freeMemSize = data[el][1]
		fragments = data[el][0]
			
print ("0 kamailio_max_used_shared_memory count="+str(maxUsedSize[22:])+ " " + str(maxUsedSize))
print ("0 kamailio_free_memory_size count="+str(freeMemSize[18:])+ " " + str(freeMemSize))
print ("0 kamailio_fragments count="+str(fragments[18:])+ " " + str(fragments))
print ("0 kamailio_total_shared_memory count="+str(totalMemorySize[19:])+ " " + str(totalMemorySize))
print ("0 kamailio_used_shared_memory count="+str(usedMemorySize[18:])+ " " + str(usedMemorySize))
print ("0 number_of_registrations count="+str(numberOfRegistrations[:-1])+" "+str(numberOfRegistrations[:-1]))
print ("0 web_sockets count="+str(webSockets[:-1]) + " "+str(webSockets[:-1]))


print ("0 kamailio_max_used_shared_memory count="+str(maxUsedSizeMB))
print ("0 kamailio_free_memory_size count="+str(freeMemSizeMB))
print ("0 kamailio_total_shared_memory count="+str(totalMemorySizeMB))
print ("0 kamailio_fragments count="+str(fragments[18:])+ " " + str(fragments))
print ("0 number_of_registrations count="+str(numberOfRegistrations[:-1])+" "+str(numberOfRegistrations[:-1]))
print ("0 web_sockets count="+str(webSockets[:-1]) + " "+str(webSockets[:-1]))

if usedMemorySizeMB < maxUsedSizeMB:
        print ("0 kamailio_used_shared_memory count=" " "+str(usedMemorySizeMB))
elif maxUsedSizeMB < usedMemorySizeMB < c:
        print ("1 kamailio_used_shared_memory count=" " "+str(usedMemorySizeMB))
else:
     	print ("2 kamailio_used_shared_memory count=" " "+str(usedMemorySizeMB))
