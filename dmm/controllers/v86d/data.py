import logging
from ctypes import *
import math

from typing import Tuple, Dict, Any, Optional

from dmm.parsers.fixed_size_data import FixedSizeRawData, FixedSizeData
from dmm.definitions import (
    ElectricUnit,
    UnitScale,
    DMMRangeMode,
    DMMMode,
    DMMCaptureMode,
)

logger = logging.getLogger(__file__)

_pointer_mapping = {0x30: 1.0, 0x31: 0.001, 0x32: 0.01, 0x34: 0.1}


class V86DRawData(FixedSizeRawData):
    _fields_ = [
        ("sign", c_ubyte),
        ("value", c_ubyte * 4),
        ("sp", c_ubyte),
        ("pointer", c_ubyte),
        ("RS232", c_ubyte, 1),
        ("HOLD", c_ubyte, 1),
        ("REL", c_ubyte, 1),
        ("AC", c_ubyte, 1),
        ("DC", c_ubyte, 1),
        ("AUTO", c_ubyte, 1),  # Auto range
        ("reserve_1", c_ubyte, 1),
        ("reserve_2", c_ubyte, 1),
        ("reserve_3", c_ubyte, 1),
        ("nano", c_ubyte, 1),
        ("BAT", c_ubyte, 1),  # Low battery indicator
        ("APO", c_ubyte, 1),  # Auto Power Off mode
        ("MIN", c_ubyte, 1),  # MIN mode
        ("MAX", c_ubyte, 1),  # MAX mode
        ("reserve_4", c_ubyte, 1),
        ("reserve_5", c_ubyte, 1),
        ("reserve_6", c_ubyte, 1),
        ("percentage", c_ubyte, 1),
        ("diode", c_ubyte, 1),
        ("beep", c_ubyte, 1),
        ("mega", c_ubyte, 1),
        ("kilo", c_ubyte, 1),
        ("mili", c_ubyte, 1),
        ("micro", c_ubyte, 1),
        ("farenheit", c_ubyte, 1),
        ("celcius", c_ubyte, 1),
        ("fara", c_ubyte, 1),
        ("hz", c_ubyte, 1),
        ("hfe", c_ubyte, 1),
        ("ohm", c_ubyte, 1),
        ("ampere", c_ubyte, 1),
        ("voltage", c_ubyte, 1),
        ("bar_value", c_ubyte, 7),
        ("bar_sign", c_ubyte, 1),
        ("termial", c_short),
    ]

    _pack_ = 1

    def _calculate_value(self) -> float:
        mul = 1.0 if self.sign == 0x2B else -1.0
        value = bytes(self.value)
        # check infinite value
        if b"?" in value:
            v = mul * math.inf
        else:
            v = mul * int(self.value) * _pointer_mapping[self.pointer]

        return v

    def _parse_unit(self) -> Optional[ElectricUnit]:
        unit = None
        if self.farenheit:
            unit = ElectricUnit.Faraheit
        elif self.celcius:
            unit = ElectricUnit.Celcius
        elif self.fara:
            unit = ElectricUnit.Farad
        elif self.hz:
            unit = ElectricUnit.Hezt
        elif self.hfe:
            unit = ElectricUnit.HFE
        elif self.ohm:
            unit = ElectricUnit.Ohm
        elif self.ampere:
            unit = ElectricUnit.Ampere
        elif self.voltage:
            unit = ElectricUnit.Volt
        elif self.percentage:
            unit = ElectricUnit.Percentage
        return unit

    def _parse_range_mode(self) -> DMMRangeMode:
        if self.AUTO:
            mode = DMMRangeMode.Auto
        else:
            mode = DMMRangeMode.Manual
        return mode

    def _parse_capture_mode(self) -> Optional[DMMCaptureMode]:
        if self.MIN:
            mode = DMMCaptureMode.Min
        elif self.MAX:
            mode = DMMCaptureMode.Max
        elif self.HOLD:
            mode = DMMCaptureMode.Hold
        elif self.REL:
            mode = DMMCaptureMode.Relative
        else:
            mode = DMMCaptureMode.Period
        return mode

    def _parse_unit_scale(self) -> UnitScale:
        if self.mega:
            scale = UnitScale.Mega
        elif self.kilo:
            scale = UnitScale.Kilo
        elif self.mili:
            scale = UnitScale.Mili
        elif self.micro:
            scale = UnitScale.Micro
        elif self.nano:
            scale = UnitScale.Nano
        else:
            scale = UnitScale.NoScale
        return scale

    def _parse_operation_mode(self, unit: Optional[ElectricUnit]) -> Optional[DMMMode]:
        mode = None
        if unit == ElectricUnit.Ampere:
            if self.AC == 1:
                # CurrentAC
                mode = DMMMode.CurrentAC
            elif self.DC == 1:
                # CurrentDC
                mode = DMMMode.CurrentDC
        elif unit == ElectricUnit.Volt:
            if self.AC:
                # VoltageAC
                mode = DMMMode.VoltageAC
            elif self.DC:
                # VoltageDC
                mode = DMMMode.VoltageDC
        # Resistance
        elif unit == ElectricUnit.Ohm:
            mode = DMMMode.Resistance
        # Diode
        elif self.diode == 1:
            if unit == ElectricUnit.Percentage:
                mode = DMMMode.Continuity
            elif unit == ElectricUnit.Ohm:
                mode = DMMMode.Diode
        # Capacitance
        elif unit == ElectricUnit.Farad:
            mode = DMMMode.Capacitance
        # Frequency
        elif unit == ElectricUnit.Hezt:
            mode = DMMMode.Frequency
        # Temperature
        elif unit in [ElectricUnit.Celcius, ElectricUnit.Faraheit]:
            mode = DMMMode.Temperature
        # Inductance
        elif unit == ElectricUnit.HFE:
            mode = DMMMode.Inductance

        return mode

    def _is_beep(self) -> bool:
        return self.beep == 1

    def _parse_bar_info(self) -> Tuple[bool, float]:
        return (self.bar_sign, self.bar_value)

    def _parse_options(self) -> Dict[str, Any]:
        is_low_battery = self.BAT == 1
        return {"is_low_battery": is_low_battery}


class V86DData(FixedSizeData):
    RawDataCls = V86DRawData
