import datetime
import logging
from logging.handlers import TimedRotatingFileHandler


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.fromtimestamp(
            record.created, datetime.timezone.utc
        ).astimezone()
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f %z")

    def format(self, record):
        log_fmt = "[%(asctime)s] %(levelname)-7s %(funcName)s: %(message)s"
        formatter = logging.Formatter(log_fmt, datefmt=self.formatTime(record))
        return formatter.format(record)


def setup_logging():
    handler = TimedRotatingFileHandler(
        "app.log", when="midnight", interval=1, backupCount=0
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(CustomFormatter())

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CustomFormatter())

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addHandler(console_handler)
