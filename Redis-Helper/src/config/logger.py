import logging
import os

def get_logger(name: str = "simple_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Stream handler for console output
        stream_handler = logging.StreamHandler()
        # File handler for application.log in two levels up directory
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        log_file_path = os.path.join(base_dir, 'application.log')
        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)  # Console output
        logger.addHandler(file_handler)    # File output
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
