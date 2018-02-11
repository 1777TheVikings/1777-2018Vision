import cv2
import networktables as nt

from constants import *
import vision_utils as vu
import processing


# Generate an MJPG stream that emulates an Axis Camera.
STREAM = False

# Annotate the stream with vision processing info
ANNOTATE = True


def main():
	cap = cv2.VideoCapture("../test_samples/test_video.mp4")
	
	rval, _ = cap.read()
	if not rval: raise RuntimeError("rval test failed")
	
	rval = True
	
	print "starting..."
	
	try:
		while rval:
			vu.start_time('reading')
			rval, frame = cap.read()
			frame = cv2.resize(frame, (0, 0), fx=0.33, fy=0.33)
			vu.end_time('reading')
			data, processed_frame = processing.process(frame, ANNOTATE)
			# if data != []:
			# 	print data[0].angle
			cv2.imshow('k', processed_frame)
			cv2.waitKey(1)
	except KeyboardInterrupt:
		print "wrapping up!"
		vu.report()
	finally:
		cap.release()


main()

