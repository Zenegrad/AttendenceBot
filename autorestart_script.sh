#!/bin/bash

#Check if server is running
PID=`/bin/ps -fu $USER| grep "AttendenceBot" | grep -v "grep" | awk '{print $2'}`
date=$(date '+%Y-%m-%d %H:%M:%S')

echo $PID

if [ -z "$PID" ]; 
then 
	echo "$date: Restarting server"
       	`screen -d -m -S "AttendenceBot" -L ./start.sh`;
else
	echo "$date: Server already running"
fi
