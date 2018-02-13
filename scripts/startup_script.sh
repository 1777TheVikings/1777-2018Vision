#!/bin/bash

source /home/nvidia/.profile
workon 2018
cd /home/nvidia/1777-2018Vision

echo "waiting for camera..."
while [ "$( ls /dev/video* 2> /dev/null )" = "" ]
do
	echo "..."
	sleep 1
done
echo "camera found"

python main.py
