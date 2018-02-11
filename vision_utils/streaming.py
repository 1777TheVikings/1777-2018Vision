from bottle import get, response, ServerAdapter
from bottle import run as run_server
from Queue import Full, Empty
import threading

import sys
sys.path.append('..')
import constants as c

BOUNDARY = "myboundary"
CRLF = "\r\n"
FRAME_QUEUE = None
VIEWER_COUNT = 0
ALL_STREAMS = []
STOP_STREAMS = False


class MJPGstream(object):
	def __init__(self, frame_queue, width, height):
		global VIEWER_COUNT
		self.frame_queue = frame_queue
		self.stream_width = width
		self.stream_height = height
		VIEWER_COUNT += 1
	
	def __iter__(self):
		global ALL_STREAMS
		ALL_STREAMS.append(self)
		return self
	
	def next(self):
		if STOP_STREAMS:
			raise StopIteration
		
		data = self.frame_queue.get()
		
		# Add the frame boundary to the output
		out = "--" + BOUNDARY + CRLF

		# Add the jpg frame header
		out += "Content-type: image/jpeg" + CRLF

		# Add the frame content length
		out += "Content-length: " + str(len(data)) + CRLF + CRLF

		# Add the actual binary jpeg frame data
		return out + data

	def stop(self):
		global VIEWER_COUNT
		global ALL_STREAMS
		VIEWER_COUNT -= 1
		ALL_STREAMS.remove(self)


# found at https://stackoverflow.com/questions/11282218/bottle-web-framework-how-to-stop
class WSGIRefServerStoppable(ServerAdapter):
	server = None

	def run(self, handler):
		from wsgiref.simple_server import make_server, WSGIRequestHandler
		if self.quiet:
			class QuietHandler(WSGIRequestHandler):
				def log_request(*args, **kw): pass
		    		self.options['handler_class'] = QuietHandler
		self.server = make_server(self.host, self.port, handler, **self.options)
		self.server.serve_forever()

	def stop(self):
		STOP_STREAMS = True
		self.server.shutdown()


class MJPGserver(threading.Thread):
	def __init__(self, frame_queue):
		global FRAME_QUEUE
		super(MJPGserver, self).__init__()
		FRAME_QUEUE = frame_queue
		self.server = WSGIRefServerStoppable(host="0.0.0.0", port=1190)

	def run(self):
		run_server(server=self.server, debug=True)

	def stop(self):
		self.server.stop()

	@staticmethod
	@get("/")
	def index():
		return '<html><body><img src="/mjpg" /></body></html>'

	@staticmethod
	@get("/mjpg")
	def mjpeg():
		response.content_type = "multipart/x-mixed-replace;boundary=" + BOUNDARY
		return iter(MJPGstream(FRAME_QUEUE, c.CAMERA_RESOLUTION[0], c.CAMERA_RESOLUTION[1]))
