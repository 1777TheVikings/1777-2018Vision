import unittest
import cv2

import constants as c
import camera_settings as cs
import processors.contour_processor


class TestContourProcessorMethods(unittest.TestCase):
    def setUp(self):
        cs.load_settings(c.SETTINGS_FILE)
        self.processor = processors.contour_processor.Processor()
    
    def test_theoretical_image_detection_rate(self):
        """ Tests theoretical detection rate (no background interference) on test images.
            A passing detection is defined by exactly one contour being detected.
            At least 80% of images must pass for this test to pass.
        """
        img1 = cv2.imread("test_images/theoretical_1.jpg")
        img2 = cv2.imread("test_images/theoretical_2.jpg")
        img3 = cv2.imread("test_images/theoretical_3.jpg")
        img4 = cv2.imread("test_images/theoretical_4.jpg")
        img5 = cv2.imread("test_images/theoretical_5.jpg")
        
        detection_percentage = 0.0
        
        for i in [img1, img2, img3, img4, img5]:
            frame = cv2.resize(i, (0, 0), fx=0.33, fy=0.33)
            data = self.processor.process(frame)[0]
            if len(data) == 1:
                detection_percentage += 0.2
        
        print("Theoretical detection rate for still images: {}".format(detection_percentage))
        self.assertTrue(detection_percentage >= 0.8)
    
    def test_actual_video_detection_rate(self):
        """ Tests actual detection rate on a test video.
            A passing detection is defined by exactly one contour being detected.
            At least 65% of frames must pass for this test to pass.
        """
        cap = cv2.VideoCapture("test_videos/test_video.mp4")
        
        rval, _ = cap.read()
        if not rval:
            raise RuntimeError("rval test failed")
        
        rval = True
        total_frames = 0.0
        detected_frames = 0.0
        
        try:
            while rval:
                rval, frame = cap.read()
                if not rval:
                    break
                frame = cv2.resize(frame, (0, 0), fx=0.33, fy=0.33)
                data = self.processor.process(frame)[0]
                
                total_frames += 1.0
                if len(data) == 1.0:
                    detected_frames += 1.0
        finally:
            cap.release()
        
        print("Actual detection rate for videos: {}".format(detected_frames / total_frames))
        self.assertTrue(detected_frames / total_frames >= 0.65)


if __name__ == "__main__":
    unittest.main()
