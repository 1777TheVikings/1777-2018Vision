import cv2
import time
import threading
import signal
from queue import Queue, Full
from networktables import NetworkTables as nt

import constants as c
import camera_settings as cs
import vision_utils as vu
import processing


# found at https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
class GracefulKiller:
	kill_now = False
	def __init__(self):
		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)
	
	def exit_gracefully(self, signum, frame):
		print("suicide is bad, mk?")
		self.kill_now = True


def open_camera():
	cap = cv2.VideoCapture(c.CAMERA_ID)
	cap.set(3, c.CAMERA_RESOLUTION[0])
	cap.set(4, c.CAMERA_RESOLUTION[1])
	cap.set(5, c.CAMERA_FPS)
	rval, _ = cap.read()
	if not rval: raise RuntimeError("rval test failed")
	return cap


def main():
	killer = GracefulKiller()
	
	cs.control_led(cs.led_preset.slow_blink)
	# NetworkTables connections appear to be async, so
	# we should set this up first to minimize startup time.
	if NT_OUTPUT:
		print("connecting to networktables")
		nt.initialize(server=c.NT_IP)
		sd = nt.getTable("SmartDashboard")
	
	cap = open_camera()
	processing.load_settings(c.SETTINGS_FILE)	
	
	if RECORD:
		print("starting recording...")
		record = cv2.VideoWriter(vu.generateFilename(),
					 cv2.VideoWriter_fourcc(*"MJPG"),
					 c.CAMERA_FPS,
					 (int(c.CAMERA_RESOLUTION[0]),
					  int(c.CAMERA_RESOLUTION[1])))
	
	if STREAM:
		print("starting video stream...")
		server_queue = Queue(maxsize=2)
		server = vu.MJPGserver(server_queue)
		server.start()
		
	if NT_OUTPUT:
		if not nt.isConnected():
			cs.control_led(cs.led_preset.fast_blink)
			print("waiting for networktables...")
			while not nt.isConnected():
				time.sleep(100)  # prevents flooding the CPU
		print("networktables ready")
		# initialize NT variables bc Shuffleboard gets angery if we don't
		sd.putBoolean("vision_angle", 999)  # this will never be legitimately returned
		sd.putBoolean("vision_shutdown", False)
	
	cs.control_led(cs.led_preset.solid)
	print("starting...")
	
	rval = True
	
	try:
		while rval:
			if killer.kill_now:
				raise KeyboardInterrupt
			
			if c.RELOAD_CAMERA:
				print("reloading camera...")
				cap.release()
				cap = open_camera()
				c.RELOAD_CAMERA = False
			vu.start_time('reading')
			rval, frame = cap.read()
			vu.end_time('reading')
			data, processed_frame = processing.process(frame, ANNOTATE)
			
			if WINDOW:
				cv2.imshow('k', processed_frame)
				cv2.waitKey(1)
			
			if NT_OUTPUT:
				sd.putNumber('vision_angle', data[0].angle)
				if sd.getBoolean("vision_shutdown", False):
					raise KeyboardInterrupt
			
			if RECORD:
				vu.start_time("recording")
				record.write(processed_frame)
				vu.end_time("recording")
			
			if STREAM:
				vu.start_time("streaming")
				try:
					server_queue.put(cv2.imencode(".jpg", processed_frame)[1].tostring(), False)
				except Full:
					pass
				vu.end_time("streaming")
	except KeyboardInterrupt:
		print("wrapping up!")
		vu.report()
	finally:
		record.release()
		cap.release()
		nt.shutdown()
		if STREAM:
			server.stop()
		cs.control_led(cs.led_preset.off)


main()

