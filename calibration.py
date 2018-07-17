import cv2

import constants as c
import vision_utils as vu
import camera_settings as cs
import processing
import calibration_server


def open_camera():
	cap = cv2.VideoCapture(c.CAMERA_ID)
	cap.set(3, c.CAMERA_RESOLUTION[0])
	cap.set(4, c.CAMERA_RESOLUTION[1])
	cap.set(5, c.CAMERA_FPS)
	rval, _ = cap.read()
	if not rval: raise RuntimeError("rval test failed")
	return cap


def main():	
	processing.load_settings(c.SETTINGS_FILE)
	cs.apply_settings()
	
	cap = open_camera()
	
	server = calibration_server.CalibrationServer()
	server.start()
		
	rval = True
	
	print("starting...")
	
	try:
		while rval:
			if c.RELOAD_CAMERA:
				print("reloading camera...")
				cap.release()
				cap = open_camera()
				c.RELOAD_CAMERA = False
			vu.start_time('reading')
			rval, frame = cap.read()
			vu.end_time('reading')
			data, processed_frame = processing.process(frame, True)
			
			cv2.imshow('k', processed_frame)
			cv2.waitKey(1)
	except KeyboardInterrupt:
		print("wrapping up!")
		vu.report()
	finally:
		server.stop()
		cap.release()


main()

