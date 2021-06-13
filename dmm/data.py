import abc
from typing import TYPE_CHECKING, Dict, Any

from .definitions import *


class DMMData(abc.ABC):
    __slots__ = (
        "raw",
        "value",
        "unit",
        "scale",
        "operation_mode",
        "capture_mode",
        "range_mode",
        "is_beep",
        "bar_sign",
        "bar_value",
        "special_options",
    )
    if TYPE_CHECKING:
        raw: bytes
        value: float
        unit: ElectricUnit
        scale: UnitScale
        operation_mode: DMMMode
        capture_mode: DMMCaptureMode
        range_mode: DMMRangeMode
        is_beep: bool
        bar_sign: bool
        bar_value: float
        special_options: Dict[str, Any]

    @abc.abstractclassmethod
    def deserialize(cls, data: bytes) -> "DMMData":
        """Deserialize raw data to appropriate data class

        Args:
            data (bytes): Raw data

        Returns:
            DMMData: Represent DMM data
        """

    def __str__(self) -> str:
        return f"{self.value} {self.scale.value}{self.unit.value}"
