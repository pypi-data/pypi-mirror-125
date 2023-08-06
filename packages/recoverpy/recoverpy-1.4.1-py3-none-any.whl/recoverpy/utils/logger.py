import logging
from datetime import datetime


class Logger:
    """Encapsulates all logging related methods.

    Attributes:
        _log_path (str): Local path for search results saving.
        _log_enabled (bool): Last saved file to inform user.
        _logger (logging.Logger): Wrapped Logger object.
    """

    def __init__(self):
        """Initialize Logger."""
        self.log_path = None
        self.log_enabled = False
        self._logger = None

    def start_logging(self):
        """Initiate and configure the logger object."""
        time = datetime.now().strftime("%Y-%m-%d-%H%M%S")

        log_file_name = f"{self.log_path}recoverpy-{time}.log"

        self._logger = logging.getLogger("main")
        self._logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_file_name)
        file_handler.setLevel(logging.DEBUG)

        self._logger.addHandler(file_handler)

    def write(self, log_type: str, text: str):
        """Use logger object to write to file.

        Args:
            log_type (str): Log level
            text (str): Message
        """
        if not self.log_enabled:
            return

        if log_type == "debug":
            self._logger.debug(text)
        elif log_type == "info":
            self._logger.info(text)
        elif log_type == "warning":
            self._logger.warning(text)
        elif log_type == "error":
            self._logger.error(text)
        elif log_type == "critical":
            self._logger.critical(text)


LOGGER = Logger()
