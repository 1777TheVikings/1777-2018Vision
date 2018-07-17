import os
import json
from enum import Enum
from typing import NoReturn

import constants as c


def set(setting: str, value: str) -> NoReturn:
	os.system("v4l2-ctl -w -c " + setting + "=" + value)


led_preset = Enum("led_preset", "off solid slow_blink fast_blink")


def control_led(preset: str) -> NoReturn:
	if preset == led_preset.off:
		set("led1_mode", "0")
	elif preset == led_preset.solid:
		set("led1_mode", "1")
	elif preset == led_preset.slow_blink:
		set("led1_mode", "2")
		set("led1_frequency", "25")
	elif preset == led_preset.fast_blink:
		set("led1_mode", "2")
		set("led1_frequency", "70")


def apply_settings() -> NoReturn:
	for k in sorted(c.VISION_SETTINGS.keys(), reverse=True):
		if k[:4] == "cam_":
			set(k[4:], c.VISION_SETTINGS[k])


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
