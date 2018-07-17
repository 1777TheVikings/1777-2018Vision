import os
import json
from enum import Enum
from typing import NoReturn

import constants as c


def call_v4l2(setting: str, value: str) -> NoReturn:
    os.system("v4l2-ctl -w -c " + setting + "=" + value)


class LEDPreset(Enum):
    OFF = 1
    SOLID = 2
    SLOW_BLINK = 3
    FAST_BLINK = 4


def control_led(preset: LEDPreset) -> NoReturn:
    if preset == LEDPreset.OFF:
        call_v4l2("led1_mode", "0")
    elif preset == LEDPreset.SOLID:
        call_v4l2("led1_mode", "1")
    elif preset == LEDPreset.SLOW_BLINK:
        call_v4l2("led1_mode", "2")
        call_v4l2("led1_frequency", "25")
    elif preset == LEDPreset.FAST_BLINK:
        call_v4l2("led1_mode", "2")
        call_v4l2("led1_frequency", "70")


def apply_settings() -> NoReturn:
    for k in sorted(c.VISION_SETTINGS.keys(), reverse=True):
        if k[:4] == "cam_":
            call_v4l2(k[4:], c.VISION_SETTINGS[k])


""" Load vision settings from a file.
    
    file_name - Relative path to a JSON file containing
                vision processing settings (e.g. the
                stuff returned from the website on
                calibration.py)
    
    Does not return a value.
"""


def load_settings(file_name: str, force_reload: bool = True) -> NoReturn:
    f = open(file_name, "r")
    data = json.load(f)
    f.close()
    c.VISION_SETTINGS = data
    apply_settings()
    if force_reload:
        c.RELOAD_CAMERA = True


""" Save vision settings to a file.
    
    file_name - Relative path to a JSON file to store
                vision processing settings (e.g. the
                stuff returned from the website on
                calibration.py)
    
    Does not return a value.
"""


def save_settings(file_name: str, reload: bool = True) -> NoReturn:
    f = open(file_name, "w")
    json.dump(c.VISION_SETTINGS, f)
    f.close()
    if reload:
        apply_settings()
        c.RELOAD_CAMERA = True
