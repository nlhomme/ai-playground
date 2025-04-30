import logging
import datetime
from pathlib import Path

# 99,9% made by Alexandra Zaharia
# https://alexandra-zaharia.github.io/posts/fix-python-logger-printing-same-entry-multiple-times/

class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted by Alexandra Zaharia from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(logsfolder: str, appname: str, logLevel: str):
    # Create logs folder if not exists
    Path(logsfolder).mkdir(parents=True, exist_ok=True)   

    # Create custom logger logging all five levels 
    logger = logging.getLogger(__name__)
    logger.setLevel(logLevel)

    # Define format for logs
    fmt = '%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)2d | %(message)s'

    # Create stdout handler for logging to the console (logs all five levels)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logLevel)
    stdout_handler.setFormatter(CustomFormatter(fmt))

    # Create file handler for logging to a file (logs all five levels)
    today = datetime.date.today()
    file_handler = logging.FileHandler(logsfolder + '/' + appname + '_{}.log'.format(today.strftime('%Y_%m_%d')))
    file_handler.setLevel(logLevel)
    file_handler.setFormatter(logging.Formatter(fmt))

    # Add both handlers to the logger
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    return logger
