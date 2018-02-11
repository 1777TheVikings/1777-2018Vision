import datetime
import os.path
import constants as c


""" Utility function for generating recording filenames based
    on the current date and time.

	Takes no arguments.
	
	Returns a string specifying the absolute path to
	record a video to.
"""
def generateFilename():
	dir = c.RECORD_LOCATION
	fileName = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S") + ".avi"
	return os.path.join(dir, fileName)
