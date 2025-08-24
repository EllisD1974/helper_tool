# logger.py
import logging

_logger = None

def get_logger(name=None):
    global _logger
    if _logger is None:
        _logger = logging.getLogger(name or "app")
        _logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(levelname)-8s - %(name)s:%(funcName)s - %(message)s')

        fh = logging.FileHandler('app.log')
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        _logger.addHandler(fh)
        _logger.addHandler(ch)

    return _logger
