#!/bin/bash

exec > /tmp/startup_script_log
exec 2>&1

cd /home/nvidia/
source .profile
source .virtualenvs/2018/bin/activate
cd 1777-2018Vision

echo "waiting for camera..."
while [ "$( ls /dev/video* 2> /dev/null )" = "" ]
do
	echo "..."
	sleep 1
done
echo "camera found"

echo "waiting for SD card..."
while [ ! -e "/media/nvidia/My Files/vision_settings.json" ]
do
	echo "..."
	sleep 1
done
echo "SD card found"

nice -n -10 python main.py &

exit 0
