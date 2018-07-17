import datetime
import os.path
import constants as c


def generate_filename() -> str:
    """ Utility function for generating recording filenames based
        on the current date and time.

        Takes no arguments.

        Returns a string specifying the absolute path to
        record a video to.
    """
    directory = c.RECORD_LOCATION
    file_name = datetime.datetime.utcnow().strftime("%y-%m-%d-%H-%M-%S") + ".avi"
    return os.path.join(directory, file_name)
