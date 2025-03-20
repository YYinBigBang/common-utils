import os
import sys
import time
import logging
from functools import wraps


class Logger:
    """Singleton class for logging."""
    _instance = None  # for saving the only instance of the logger

    def __new__(cls, enable_console=True, enable_file=True, *args, **kwargs):
        """
        :param enable_console: Whether to enable the console output.
        :param enable_file: whether to enable the file output.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._enable_console_flag = enable_console
            cls._instance._enable_file_flag = enable_file
        return cls._instance

    def __init__(self, enable_console=True, enable_file=True):
        """Initialize the logger."""
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        # Create a logger
        self.logger = logging.getLogger(__name__)

        if not self.logger.handlers:
            # Create a logging format
            formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

            # Output to the command line.
            if self._enable_console_flag:
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(formatter)
                console_handler.setLevel(logging.DEBUG)
                self.logger.addHandler(console_handler)

            # Output to the file.
            if self._enable_file_flag:
                curr_date = time.strftime("%Y%m%d")
                log_path = './Logger'
                log_name = f'{curr_date}.log'
                log_file = os.path.join(log_path, log_name)
                os.makedirs(log_path, exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_handler.setLevel(logging.DEBUG)  # Set the level of the file handler
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Return the logger instance."""
        return self.logger


def timelog(func):
    """Decorator to log the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = Logger().get_logger()
        logger.info(f'[Phase: {func.__name__}] ------------- START')
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            execution_time = time.time() - start_time
            logger.info(f"[Phase: {func.__name__}] ------------- END in {execution_time:.3f}(s)")
    return wrapper
    
