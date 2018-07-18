from typing import NoReturn
from http.server import BaseHTTPRequestHandler
from queue import Queue, Empty


BOUNDARY = "jpgboundary"
CRLF = "\r\n"
FRAME_QUEUE = None
VIEWER_COUNT = 0
ALL_STREAMS = []
STOP_STREAMS = False


class MJPGServer(BaseHTTPRequestHandler):
    # noinspection PyPep8Naming
    def do_GET(self):
        if self.path == "/mjpg":
            self.send_response(200)
            self.send_header("Content-type", "multipart/x-mixed-replace; boundary=--{}".format(BOUNDARY))
            self.end_headers()
            
            while True:
                global FRAME_QUEUE
                try:
                    data = FRAME_QUEUE.get(block=False)
                except Empty:
                    continue
                
                self.wfile.write("--{}".format(BOUNDARY))
                self.send_header("Content-type", "image/jpeg")
                self.send_header("Content-length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)


def set_frame_queue(queue: Queue) -> NoReturn:
    global FRAME_QUEUE
    FRAME_QUEUE = queue
