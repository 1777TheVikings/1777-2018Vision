import os
import json
import constants as c
from enum import Enum


def set(setting, value):
	os.system("v4l2-ctl -w -c " + setting + "=" + value)


led_preset = Enum("led_preset", "off solid slow_blink fast_blink")


def control_led(preset):
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


def apply_settings():
	for k in sorted(c.VISION_SETTINGS.iterkeys(), reverse=True):
		if k[:4] == "cam_":
			set(k[4:], c.VISION_SETTINGS[k])
