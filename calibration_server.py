import threading
import json
from bottle import get, post, request, TEMPLATE_PATH, jinja2_view
from bottle import run as run_server

import processing
import constants as c
from vision_utils import WSGIRefServerStoppable


TEMPLATE_PATH[:] = ["."]


class CalibrationServer(threading.Thread):
	def __init__(self):
		super(CalibrationServer, self).__init__()
		self.server = WSGIRefServerStoppable(host="0.0.0.0", port=5800)  # Can only use ports 5800-5810 for miscellaneous communications
	
	def run(self):
		run_server(server=self.server, debug=True)
	
	def stop(self):
		self.server.stop()
	
	@staticmethod
	@get("/")
	@jinja2_view("main.html")
	def main_page():
		return c.VISION_SETTINGS
	
	@staticmethod
	@post("/recv")
	def receive_data():
		resp = json.loads(request.body.read())
		c.VISION_SETTINGS = resp
		processing.save_settings(c.SETTINGS_FILE)
		return "good"
