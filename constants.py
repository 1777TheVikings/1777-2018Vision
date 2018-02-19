import os  # used for reading environment variables


# Horizontal field of view of the camera in degrees.
# Current value is set for Microsoft Lifecam HD-3000.
FOV = 60.0

# ID of the camera. Override this using the environment
# variable VISION_CAMERA_ID when not using the Jetson,
# or when using a device with multiple cameras.
try:
	CAMERA_ID = os.environ["VISION_CAMERA_ID"]
	print "Camera ID manually set to " + CAMERA_ID
except KeyError:
	CAMERA_ID = 0

# Resolution of the camera, set as (width, height)
CAMERA_RESOLUTION = (640.0, 480.0)

# FPS of the camera. Keep in mind that for many
# cameras, actual FPS is highly dependant on lighting.
CAMERA_FPS = 30.0

# Calculated based on previous values
DEGREES_PER_PIXEL = FOV / CAMERA_RESOLUTION[0]

# IP of the robot, same as used to configure it on IE
NT_IP = "roboRIO-1777-FRC.local"

# Recording location. Override this using the
# environment variable VISION_RECORD_LOCATION when
# not using the Jetson (e.g. when calibrating or
# recording testing vids on a laptop).
try:
	RECORD_LOCATION = os.environ["VISION_RECORD_LOCATION"]
	print "Record location manually set to " + RECORD_LOCATION
except KeyError:
	RECORD_LOCATION = "/media/nvidia/My Files/Recordings"

# Location of the vision processing settings file.
# Override this using the environment variable
# VISION_SETTINGS_FILE when not using the Jetson
# (e.g. when calibrating on a laptop).
try:
	SETTINGS_FILE = os.environ["VISION_SETTINGS_FILE"]
	print "Settings file location manually set to " + SETTINGS_FILE
except KeyError:
	SETTINGS_FILE = "/media/nvidia/My Files/vision_settings.json"

# Vision processing info (shouldn't be manually set)
VISION_SETTINGS = {}

# Request the main thread to reload the camera
# (definitely shouldn't be manually set)
RELOAD_CAMERA = False
