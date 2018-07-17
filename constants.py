import os  # used for reading environment variables


# Generate an MJPG stream that emulates an Axis Camera.
STREAM = True

# Record all videos.
RECORD = True

# Annotate the stream with vision processing info
ANNOTATE = True

# Connect to NetworkTables and stream data to there.
NT_OUTPUT = False

# Display a window with the stream output. Disable at
# competition to increase framerate, since graphical
# output requires delays (cv2.waitKey).
WINDOW = True

# Uses the processing module specified in $PROCESSOR.py.
# This uses dynamic module loading, so don't add a file
# extension to this. Modules are searched for in
# the folder "processors".
PROCESSOR = "contour_processor"


# Horizontal field of view of the camera in degrees.
# Current value is set for Microsoft Lifecam HD-3000.
FOV = 60.0

# ID of the camera. Override this using the environment
# variable VISION_CAMERA_ID when not using the Jetson,
# or when using a device with multiple cameras.
try:
	CAMERA_ID = os.environ["VISION_CAMERA_ID"]
	print("Camera ID manually set to {}".format(CAMERA_ID))
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
	print("Record location manually set to {}".format(RECORD_LOCATION))
except KeyError:
	RECORD_LOCATION = "/media/nvidia/Files/Recordings"

# Location of the vision processing settings file.
# Override this using the environment variable
# VISION_SETTINGS_FILE when not using the Jetson
# (e.g. when calibrating on a laptop).
try:
	SETTINGS_FILE = os.environ["VISION_SETTINGS_FILE"]
	print("Settings file location manually set to {}".format(SETTINGS_FILE))
except KeyError:
	SETTINGS_FILE = "/media/nvidia/Files/vision_settings.json"

# Vision processing info (shouldn't be manually set)
VISION_SETTINGS = {}

# Request the main thread to reload the camera
# (definitely shouldn't be manually set)
RELOAD_CAMERA = False
