import numpy  # only imported for type checking
import cv2
import os
import json
from math import sqrt

import constants as c
import camera_settings as cs
import vision_utils as vu


""" Performs the main bulk of the vision processing.
	
	frame      - A numpy.ndarray (image/frame from webcam or file)
	annotate   - Whether to annotate the output frame with
		         vision processing info
	
	Returns a tuple containing, in this order, the results of
	the vision processing and the resulting frame (potentially
	with annotation). If annotation is not requested, the output
	frame is the masked/blurred/denoised image.
"""
def process(frame, annotate):
	if type(frame) is not numpy.ndarray:
		raise ValueError("'frame' should be of the type numpy.ndarray")
	if type(annotate) is not bool:
		raise ValueError("'annotate' should be a boolean value")
	
	vu.start_time('blur')
	blurred = cv2.blur(frame, (15, 15))
	vu.end_time('blur')
	
	vu.start_time('hsl')
	hsl_filtered = cv2.inRange(cv2.cvtColor(blurred, cv2.COLOR_BGR2HLS),
				   (int(c.VISION_SETTINGS['hue'][0]),
				    int(c.VISION_SETTINGS['luminance'][0]),
				    int(c.VISION_SETTINGS['saturation'][0])),
				   (int(c.VISION_SETTINGS['hue'][1]),
				    int(c.VISION_SETTINGS['luminance'][1]),
				    int(c.VISION_SETTINGS['saturation'][1])))
	vu.end_time('hsl')
	
	vu.start_time('denoise')
	eroded = cv2.erode(hsl_filtered, None, (-1, -1), iterations=5, borderType=cv2.BORDER_CONSTANT, borderValue=(-1))
	dilated = cv2.dilate(hsl_filtered, None, (-1, -1), iterations=5, borderType=cv2.BORDER_CONSTANT, borderValue=(-1))
	vu.end_time('denoise')
	
	vu.start_time('contours')
	contour_image, contours, hierarchy = cv2.findContours(dilated, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
	
	contours_hulls = []
	for i in contours:
		contours_hulls.append(cv2.convexHull(i))	
	
	contours_filtered = filter_contours(contours_hulls)	
	data_out = vu.process_contours(contours_filtered)
	vu.end_time('contours')
	
	if annotate:
		output_frame = frame
		cv2.drawContours(output_frame, contours_hulls, -1, (255, 0, 0), 1)
		cv2.drawContours(output_frame, contours_filtered, -1, (0, 255, 0), 3)
		for i in data_out:
			cv2.circle(output_frame, (i.x, i.y), 3, (0, 255, 0), -1)
			cv2.putText(output_frame, str(i.angle), (i.x + 20, i.y + 20), cv2.FONT_HERSHEY_SIMPLEX,
				    2, (255, 255, 255), 2, cv2.LINE_AA)
	else:
		output_frame = dilated
	
	return (data_out, output_frame)


""" Contour filtering stolen from GRIP output code.
	
	contours - Contours as a list of numpy.ndarray
	
	Returns all valid contours as a list of numpy.ndarray.
"""
def filter_contours(contours):
	if type(contours) is not list:
		raise ValueError("'contours' should be a list; input is of type " + str(type(contours)))
	
	# TODO: Move hardcoded values to constants.py
	
	output = []
	for contour in contours:
		x,y,w,h = cv2.boundingRect(contour)
		if w < int(c.VISION_SETTINGS['width'][0]) or w > int(c.VISION_SETTINGS['width'][1]):  # min/max width
			continue
		if h < int(c.VISION_SETTINGS['height'][0]) or h > int(c.VISION_SETTINGS['height'][1]):  # min/max height
			continue
		
		area = cv2.contourArea(contour)
		if area < int(c.VISION_SETTINGS['area'][0]) or area > int(c.VISION_SETTINGS['area'][1]):  # min/max area
			continue
		
		output.append(contour)
	
	return output


""" Load vision settings from a file.
	
	file_name - Relative path to a JSON file containing
				vision processing settings (e.g. the
				stuff returned from the website on
				calibration.py)
	
	Does not return a value.
"""
def load_settings(file_name, force_reload=True):
	f = open(file_name, "r")
	data = json.load(f)
	f.close()
	c.VISION_SETTINGS = data
	cs.apply_settings()
	if force_reload:
		c.RELOAD_CAMERA = True


""" Save vision settings to a file.
	
	file_name - Relative path to a JSON file to store
				vision processing settings (e.g. the
				stuff returned from the website on
				calibration.py)
	
	Does not return a value.
"""
def save_settings(file_name, reload=True):
	f = open(file_name, "w")
	json.dump(c.VISION_SETTINGS, f)
	f.close()
	if reload:
		cs.apply_settings()
		c.RELOAD_CAMERA = True
