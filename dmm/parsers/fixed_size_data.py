import logging
from ctypes import *
from typing import Tuple, Dict, Any, Optional

from dmm.data import DMMData
from dmm.definitions import *

logger = logging.getLogger(__file__)


class FixedSizeRawData(Structure):
    def _calculate_value(self) -> float:
        raise NotImplementedError

    def _parse_unit(self) -> Optional[ElectricUnit]:
        raise NotImplementedError

    def _parse_range_mode(self) -> DMMRangeMode:
        raise NotImplementedError

    def _parse_capture_mode(self) -> Optional[DMMCaptureMode]:
        raise NotImplementedError

    def _parse_unit_scale(self) -> UnitScale:
        raise NotImplementedError

    def _parse_operation_mode(self, unit: Optional[ElectricUnit]) -> Optional[DMMMode]:
        raise NotImplementedError

    def _parse_bar_info(self) -> Tuple[bool, float]:
        raise NotImplementedError

    def _is_beep(self) -> bool:
        raise NotImplementedError

    def _parse_options(self) -> Dict[str, Any]:
        raise NotImplementedError


class FixedSizeData(DMMData):
    RawDataCls = FixedSizeRawData

    def __init__(self, **kwargs: Any) -> None:
        for s in self.__slots__:
            setattr(self, s, kwargs[s])

    @classmethod
    def deserialize(cls, buf: bytes) -> Optional["FixedSizeData"]:  # type: ignore [override]
        try:
            raw = cls.RawDataCls.from_buffer_copy(buf)
            if raw is not None:
                unit = raw._parse_unit()
                bar_sign, bar_value = raw._parse_bar_info()
                return FixedSizeData(
                    raw=buf,
                    value=raw._calculate_value(),
                    unit=unit,
                    scale=raw._parse_unit_scale(),
                    operation_mode=raw._parse_operation_mode(unit),
                    capture_mode=raw._parse_capture_mode(),
                    range_mode=raw._parse_range_mode(),
                    is_beep=raw._is_beep(),
                    bar_value=bar_sign,
                    bar_sign=bar_value,
                    special_options=raw._parse_options(),
                )
        except:
            logger.error(
                f'Parse fail: {(", ".join("0x{:02x}".format(x) for x in buf))}'
            )
            return None
