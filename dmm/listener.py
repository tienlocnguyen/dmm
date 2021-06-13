import abc
import logging


from .data import DMMData


class DMMListenerBase(abc.ABC):
    @abc.abstractmethod
    def on_received_data(self, data: DMMData) -> None:
        """Handle received DMM data

        Args:
            data (DMMData): DMM data
        """

    @abc.abstractmethod
    def on_error(self, error_code: int) -> None:
        """Handle error when receive data

        Args:
            error_code (int): Error code
        """


class DMMLogListener(DMMListenerBase):
    def __init__(self, logger: logging.Logger = None, log_level: int = logging.INFO):
        self.logger = logger or logging.getLogger("DMMLogListener")
        self.log_level = log_level

    def on_received_data(self, data: DMMData) -> None:
        self.logger.log(self.log_level, f"Received: {data}")

    def on_error(self, error_code: int) -> None:
        self.logger.error(f"Got error with code: {error_code}")
