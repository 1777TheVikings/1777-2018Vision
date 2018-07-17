import cv2
import time
import signal
import importlib
from queue import Queue, Full
from networktables import NetworkTables
from typing import NoReturn

import constants as c
import camera_settings as cs
import vision_utils as vu


# found at https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *_) -> NoReturn:
        print("suicide is bad, mk?")
        self.kill_now = True


def open_camera() -> cv2.VideoCapture:
    cap = cv2.VideoCapture(c.CAMERA_ID)
    cap.set(3, c.CAMERA_RESOLUTION[0])
    cap.set(4, c.CAMERA_RESOLUTION[1])
    cap.set(5, c.CAMERA_FPS)
    rval, _ = cap.read()
    if not rval:
        raise RuntimeError("rval test failed")
    return cap


def main() -> NoReturn:
    killer = GracefulKiller()

    cs.control_led(cs.LEDPreset.SLOW_BLINK)
    # NetworkTables connections appear to be async, so
    # we should set this up first to minimize startup time.
    if c.NT_OUTPUT:
        print("connecting to networktables")
        NetworkTables.initialize(server=c.NT_IP)
        sd = NetworkTables.getTable("SmartDashboard")

    cap = open_camera()
    cs.load_settings(c.SETTINGS_FILE)

    if c.RECORD:
        print("starting recording...")
        record = cv2.VideoWriter(vu.generate_filename(),
                                 cv2.VideoWriter_fourcc(*"MJPG"),
                                 c.CAMERA_FPS,
                                 (int(c.CAMERA_RESOLUTION[0]),
                                  int(c.CAMERA_RESOLUTION[1])))

    if c.STREAM:
        print("starting video stream...")
        server_queue = Queue(maxsize=2)
        server = vu.MJPGserver(server_queue)
        server.start()

    if c.NT_OUTPUT:
        if not NetworkTables.isConnected():
            cs.control_led(cs.LEDPreset.FAST_BLINK)
            print("waiting for networktables...")
            while not NetworkTables.isConnected():
                time.sleep(100)  # prevents flooding the CPU
        print("networktables ready")
        # initialize NT variables bc Shuffleboard gets angery if we don't
        # noinspection PyUnboundLocalVariable
        sd.putBoolean("vision_angle", 999)  # this will never be legitimately returned
        sd.putBoolean("vision_shutdown", False)

    processing_module = importlib.import_module("processors." + c.PROCESSOR)
    processor = processing_module.Processor()

    cs.control_led(cs.LEDPreset.SOLID)
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
            rval, frame = cap.read()
            data, processed_frame = processor.process(frame, annotate=c.ANNOTATE)

            if c.WINDOW:
                cv2.imshow('k', processed_frame)
                cv2.waitKey(1)

            if c.NT_OUTPUT:
                if len(data) > 0:
                    sd.putNumber('vision_angle', data[0].angle)
                if sd.getBoolean("vision_shutdown", False):
                    raise KeyboardInterrupt

            if c.RECORD:
                # noinspection PyUnboundLocalVariable
                record.write(processed_frame)

            if c.STREAM:
                try:
                    # noinspection PyUnboundLocalVariable
                    server_queue.put(cv2.imencode(".jpg", processed_frame)[1].tostring(), False)
                except Full:
                    pass
    except KeyboardInterrupt:
        print("wrapping up!")
    finally:
        record.release()
        cap.release()
        NetworkTables.shutdown()
        if c.STREAM:
            # noinspection PyUnboundLocalVariable
            server.stop()
        cs.control_led(cs.LEDPreset.OFF)


main()
