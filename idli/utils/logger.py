import logging
import os
from datetime import datetime as dt
from cloghandler import ConcurrentRotatingFileHandler

LOGGING_DIR = 'logs'
LOGGER_FILE = 'log-'

class Logger:
    def __init__(self, module=''):

        today_datetime = dt.now()
        today_date = dt.date(today_datetime)
        string_date = str(today_date)

        if module == '':
            file_name = LOGGER_FILE + string_date
        else:
            file_name = LOGGER_FILE + module + '-' + string_date

        logger = logging.getLogger(file_name)  # log_namespace can be replaced with your namespace
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            file_name = os.path.join(LOGGING_DIR,
                                     '%s.log' % file_name)  # usually I keep the LOGGING_DIR defined in some global settings file
            handler = ConcurrentRotatingFileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(module)s:%(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)
        self._logger = logger

    def get(self):
        return self._logger



if __name__ == "__main__":
    logger = Logger().get()
    logger.info("This is a test message")
