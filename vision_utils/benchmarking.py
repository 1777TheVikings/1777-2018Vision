import cv2
import collections
from typing import NoReturn

exec_times = collections.defaultdict(lambda: [0, 0])
timers_in_progress = {}


def add_to_execution_times(timer_name: str, time: float) -> NoReturn:
    global exec_times
    new_time_total = (exec_times[timer_name][1] * exec_times[timer_name][0]) + time
    exec_times[timer_name][0] += 1
    exec_times[timer_name][1] = new_time_total / exec_times[timer_name][0]


def start_time(timer_name: str) -> NoReturn:
    global timers_in_progress
    timers_in_progress[timer_name] = cv2.getTickCount()


def end_time(timer_name: str) -> NoReturn:
    end = cv2.getTickCount()
    add_to_execution_times(timer_name,
                           (end - timers_in_progress[timer_name]) / cv2.getTickFrequency())


def report() -> NoReturn:
    total_time = 0
    for i in exec_times.values():
        total_time += i[1]
    
    top_line = "Average time per frame: {} seconds".format(str(total_time))
    avg_fps_line = "Average frames per second: {} fps".format(str(1 / total_time))
    longest_type = max({i: len(i) for i in exec_times.keys()}.values())
    remaining_len = max(len(top_line), len(avg_fps_line)) - (longest_type + 3)
    print(top_line)
    print(avg_fps_line)
    print("=" * len(top_line))
    for i in exec_times.keys():
        str_out = i.ljust(longest_type + 1) + "| "
        percent = exec_times[i][1] / total_time
        str_out += "#" * int(round((remaining_len - 6) * percent))
        last_len = remaining_len - int(round((remaining_len - 6) * percent))
        str_out += (" %.1f%%" % (percent * 100)).rjust(last_len)
        print(str_out)
