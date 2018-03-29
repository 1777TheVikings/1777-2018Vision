# FRC Team 1777 Vision Code

This is team #1777 Viking's vision processing code for the 2018 Power Up game. This code is intended to be run on a NVIDIA Jetson TX1 using a Logitech C920 webcam for video input; however, any computer with a V4L2-compliant webcam should work for testing. This code uses OpenCV 3.4.0 and Python 2.7.12 (should work on any 2.7 subversion).

Your Jetson (or other coprocessing SoC of choice) should be configured to run `main.py` on startup. See `scripts/startup_script.sh` for an example. `calibration.py` is a trimmed-down version of that code, with an added web server serving an easy-to-use calibration tool. This tool allows teams to quickly change the camera/pipeline settings during testing (or on the field; see [Calibration on a laptop](#calibration-on-a-laptop) below for more info).


## Hardware and software requirements

While this code is intended for use on the NVIDIA Jetson TX1 using a Logitech C920 webcam, any coprocessing SoC (e.g. Raspberry Pi, Tinkerboard) with a V4L2-compliant webcam will work. If using a Jetson, an SD card is strongly recommended for storing recordings and camera/pipeline settings.

This code should run using Python 2.7.* with OpenCV 3.* bindings. (The pip libraries use OpenCV 2.4, so you must compile OpenCV from source to run this code without modifications.) Beyond that, the following packages must be installed:

- pynetworktables
- Jinja2
- bottle
- numpy


## Data outputs

The relative angle to the nearest detected Power Cube (CCW is positive, similar to the Pigeon IMU) is sent to the NetworkTables index `vision_angle`. If multiple Cubes are detected, the one nearest to the center of the screen is used for the angle calculations.

The annotated output of the vision processing is, by default, streamed at `http://<IP-of-your-computer>:1190/mjpg`. This port may need to be changed to be compliant to FRC port rules if a USB camera is directly attached to the RoboRIO. If streaming is undesirable, disable it by setting `STREAM` to False in `main.py`.

All video is recorded to the directory listed in `RECORD_LOCATION` of `constants.py`. This can be changed directly by editing the variable or by setting the `VISION_RECORD_LOCATION` environment variable (preferrable for testing on a separate computer). In our case, the value is preset to save videos to an SD card labelled "My Files".


## Camera/pipeline settings

Various settings for the camera and the vision processing pipeline can be found in `vision_settings.json`. The file path can be manually edited in `SETTINGS_FILE` of `constants.py` or with the environment variable `VISION_SETTINGS_FILE`. By default, the file path directs to a copy of the settings file on an SD card (the reason for this will be made clear later), not the file in this repository. Move the file and/or edit the path accordingly.


## Calibration

By running `calibration.py`, a web server will be opened at `https://<IP-of-your-computer>:5800`. This URL hosts a control panel that can be used to quickly change the major camera and vision pipeline settings. Simply drag the slider to the desired settings and click "Submit" to update the pipeline. The new settings are saved to `vision_settings.json` based on the path set in `SETTINGS_FILE` of `constants.py`.

#### Calibration on a laptop

The official FRC competitions provide a 30 minute window for vision processing calibration before qualification matches start. However, bringing your entire robot out to calibration may not be possible (last-minute mechanical changes, inspections, laziness, etc.). A convenient alternative is to download this repository on a laptop running Ubuntu (any Linux distro will probably work as long as it has the V4L2 drivers installed):

1. When setting up this code on your Jetson, set `VISION_SETTINGS` in `constants.py` to point towards an SD card. (A USB stick works, but isn't preferred due to susceptibility to vibrations.)
2. Download this repository on a laptop running Linux.
3. Insert your SD card and put `vision_settings.json` on it.
4. Set the environment variable `VISION_SETTINGS_FILE` to point towards your SD card.
5. Run `calibration.py` and use the web interface to set the files.
6. Once done, eject the SD card and put it into your Jetson.

Voila! Instead of bringing your entire robot out to the field for calibration, a laptop with a USB webcam will suffice. This makes it much quicker to calibrate and allows your build team to perform last-minute changes to the robot without interruption.
