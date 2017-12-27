#!/bin/bash
while true
do
	if ! ps ax | grep "python3\ server.py"
	then
		echo "Starting PIPO server..."
		sudo python3 server.py
	fi
	sleep 1
done
