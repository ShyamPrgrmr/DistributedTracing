import logging


def get_logger(name: str = "simple_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
