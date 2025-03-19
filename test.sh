#!/bin/bash

$PID=`/bin/ps -fu $USER| grep "AttendenceBot" | grep -v "grep" | awk '{print $2'}`

if [ -z $PID ];
then
	echo "Test 1"
	echo "$PID"


fi

