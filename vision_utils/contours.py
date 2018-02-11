import cv2
from math import sqrt
import sys
sys.path.append('..')
from constants import *


class ContourInfo(object):
	def __init__(self, contour):
		self.contour = contour
		self.calc_angle()
	
	def calc_angle(self):
		moments = cv2.moments(self.contour)
		self.x = int(moments['m10'] / moments['m00'])
		self.y = int(moments['m01'] / moments['m00'])
		
		midway = CAMERA_RESOLUTION[0] / 2
		if self.x < (midway):
			self.angle = DEGREES_PER_PIXEL * (midway - self.x)
		else:
			self.angle = -1 * (DEGREES_PER_PIXEL * (self.x - 320))


def _get_contour_dist_from_center(contour):
	coords = (contour.x, contour.y)
	center = (CAMERA_RESOLUTION[0] / 2, CAMERA_RESOLUTION[1] / 2)
	
	dist_x = abs(coords[0] - center[0])
	dist_y = abs(coords[1] - center[1])
	
	return sqrt((dist_x ** 2) + (dist_y ** 2))


""" Takes a list of contours and converts them into ContourInfo objects.

	contours - A list of contours (numpy.ndarray objects)
	
	Returns a list of ContourInfo objects.
"""
def process_contours(contours):
	output = []
	for c in contours:
		output.append(ContourInfo(c))
	
	output.sort(key=_get_contour_dist_from_center)
	
	return output
