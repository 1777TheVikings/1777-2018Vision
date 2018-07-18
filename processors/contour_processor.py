import cv2
from numpy import ndarray  # only imported for type checking
from typing import Tuple, List

import constants as c
import vision_utils as vu
from processor import ProcessorBase


class Processor(ProcessorBase):
    """ Processes images using HSV filtering and contours.
    """
    
    """ Performs the main bulk of the vision processing.
        
        frame      - A numpy.ndarray (image/frame from webcam or file)
        annotate   - Whether to annotate the output frame with
                 vision processing info

        Returns a tuple containing, in this order, the results of
        the vision processing and the resulting frame (potentially
        with annotation). If annotation is not requested, the output
        frame is the masked/blurred/denoised image.
    """
    
    def process(self, frame: ndarray, **kwargs) -> Tuple[List[vu.ContourInfo], ndarray]:
        blurred = cv2.blur(frame, (15, 15))
        
        hsl_filtered = cv2.inRange(cv2.cvtColor(blurred, cv2.COLOR_BGR2HLS),
                                   (int(c.VISION_SETTINGS['hue'][0]),
                                    int(c.VISION_SETTINGS['luminance'][0]),
                                    int(c.VISION_SETTINGS['saturation'][0])),
                                   (int(c.VISION_SETTINGS['hue'][1]),
                                    int(c.VISION_SETTINGS['luminance'][1]),
                                    int(c.VISION_SETTINGS['saturation'][1])))
        
        eroded = cv2.erode(hsl_filtered, None, (-1, -1), iterations=5, borderType=cv2.BORDER_CONSTANT, borderValue=(-1))
        dilated = cv2.dilate(eroded, None, (-1, -1), iterations=5, borderType=cv2.BORDER_CONSTANT,
                             borderValue=(-1))
        
        contour_image, contours, _ = cv2.findContours(dilated, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
        
        contours_hulls = [cv2.convexHull(cnt) for cnt in contours]
        contours_filtered = [cnt for cnt in contours_hulls if self.filter_contour(cnt)]
        
        data_out = [vu.ContourInfo(cnt) for cnt in contours_filtered]
        data_out.sort(key=vu.get_nearness_to_center)
        
        if "annotate" in kwargs and kwargs["annotate"]:
            output_frame = frame
            cv2.drawContours(output_frame, contours_hulls, -1, (255, 0, 0), 1)
            cv2.drawContours(output_frame, contours_filtered, -1, (0, 255, 0), 3)
            for i in data_out:
                cv2.circle(output_frame, (i.x, i.y), 3, (0, 255, 0), -1)
                cv2.putText(output_frame, str(i.angle), (i.x + 20, i.y + 20), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            output_frame = dilated
        
        return data_out, output_frame
    
    @staticmethod
    def filter_contour(contour: ndarray) -> bool:
        """ Contour filtering stolen from GRIP output code.

                contours - Contour as a numpy.ndarray

                Returns True if the contour is valid, False otherwise.
        """
        x, y, w, h = cv2.boundingRect(contour)
        if w < int(c.VISION_SETTINGS['width'][0]) or w > int(c.VISION_SETTINGS['width'][1]):  # min/max width
            return False
        if h < int(c.VISION_SETTINGS['height'][0]) or h > int(c.VISION_SETTINGS['height'][1]):  # min/max height
            return False
        
        area = cv2.contourArea(contour)
        if area < int(c.VISION_SETTINGS['area'][0]) or area > int(c.VISION_SETTINGS['area'][1]):  # min/max area
            return False
        
        return True
