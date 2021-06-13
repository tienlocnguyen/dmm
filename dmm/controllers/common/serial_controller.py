from dmm.data import DMMData
import logging

import serial

from dmm.controller import DMMControllerBase


logger = logging.getLogger(__file__)


class DMMSerialController(DMMControllerBase):
    BAUDRATE: int = 2400
    STOPBITS: int = serial.STOPBITS_ONE
    PARITY: int = serial.PARITY_NONE

    def __init__(self, serial_port: str) -> None:
        DMMControllerBase.__init__(self)
        self.serial = serial.Serial()
        self.serial.port = serial_port
        self.serial.baudrate = self.BAUDRATE
        self.serial.stopbits = self.STOPBITS
        self.serial.parity = self.PARITY

    def _connect(self) -> None:
        self.serial.open()

    def _disconnect(self) -> None:
        self.serial.close()


class DMMSerialFixedLengthController(DMMSerialController):
    FRAME_SIZE: int = 14

    def _recv(self) -> DMMData:
        logger.debug("Read data from DMM")
        print("Read data from DMM")
        return self.serial.read(self.FRAME_SIZE)
