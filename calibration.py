import cv2
from typing import NoReturn

import constants as c
import camera_settings as cs
import calibration_server
from processors.contour_processor import Processor


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
    cs.load_settings(c.SETTINGS_FILE)
    cs.apply_settings()
    
    cap = open_camera()
    
    # server = calibration_server.CalibrationServer()
    # server.start()
    
    rval = True
    
    processor = Processor()
    print("starting...")
    
    try:
        while rval:
            if c.RELOAD_CAMERA:
                print("reloading camera...")
                cap.release()
                cap = open_camera()
                c.RELOAD_CAMERA = False
            rval, frame = cap.read()
            data, processed_frame = processor.process(frame, annotate=True)
            
            cv2.imshow('k', processed_frame)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        print("wrapping up!")
    finally:
        # server.stop()
        cap.release()


main()
