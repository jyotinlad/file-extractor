from datetime import datetime
from logging import getLogger, FileHandler, Formatter, StreamHandler, INFO
from os import path
from sys import stdout


class Logger:

    LOG_FILENAME = "{}.multiprocess.log".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    LOG_FILE = path.join("..", "logs", LOG_FILENAME)

    def __init__(self):
        pass

    @classmethod
    def get(cls):
        log = getLogger()
        log.setLevel(INFO)

        # output log to console
        handler = StreamHandler(stdout)
        handler.setLevel(INFO)
        formatter = Formatter('%(levelname)s %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)

        # output log to file
        fh = FileHandler(cls.LOG_FILE)
        fh.setLevel(INFO)
        formatter = Formatter('%(asctime)s %(levelname)s %(message)s', "%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formatter)
        log.addHandler(fh)

        return log
