#!/bin/bash
while true
do
	if ! ps ax | grep "python3\ server.py"
	then
		echo "Starting PIPO server..."
		sudo python3 /home/pi/pipo_core/server.py
	fi
	sleep 1
done
