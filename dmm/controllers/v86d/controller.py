import logging

import serial

from dmm.controllers.common.serial_controller import DMMSerialFixedLengthController
from .data import V86DData


logger = logging.getLogger(__file__)


class V86DController(DMMSerialFixedLengthController):
    BAUDRATE = 2400
    STOPBITS = serial.STOPBITS_ONE
    PARITY = serial.PARITY_NONE
    FRAME_SIZE = 14

    def _recv(self) -> V86DData:
        raw_data = self.serial.read(self.FRAME_SIZE)
        data = V86DData.deserialize(raw_data)
        return data  # type: ignore
