

#!/bin/bash
 
ram=$(systemd-cgtop | grep kamailio | awk '{print substr($4, 1, length($4)-3)}') 

if [ $ram -le 230 ]; then
	status=0
	statustext="Memory usage is OK"
elif [ $ram -gt 230 ] && [ $ram -lt 270  ]; then
	status=1
	statustext="Memory usage is WARN"
else
	status=2
	statustext="Memory usage is CRIT"
fi 

echo "$status Kamailio_memory_usage memory=$ram $ram Mb - $statustext"

