from ctypes import sizeof
import math

import pytest

from dmm.definitions import *
from dmm.controllers.v86d.data import V86DData, V86DRawData


dc_270_2_mV = bytes(
    [0x2B, 0x32, 0x37, 0x30, 0x32, 0x20, 0x34, 0x31, 0x00, 0x40, 0x80, 0x1A, 0x0D, 0x0A]
)

temp_31_4_C = bytes(
    [0x2B, 0x30, 0x33, 0x31, 0x34, 0x20, 0x34, 0x20, 0x00, 0x00, 0x02, 0x04, 0x0D, 0x0A]
)

ac_2_3_uA = bytes(
    [0x2B, 0x30, 0x30, 0x32, 0x33, 0x20, 0x34, 0x29, 0x00, 0x80, 0x40, 0x00, 0x0D, 0x0A]
)

hfe_2_0_hFE = bytes(
    [0x2B, 0x30, 0x30, 0x30, 0x32, 0x20, 0x30, 0x00, 0x00, 0x00, 0x10, 0x00, 0x0D, 0x0A]
)

frequency_52_43_Hz = bytes(
    [0x2B, 0x35, 0x32, 0x34, 0x33, 0x20, 0x32, 0x20, 0x00, 0x00, 0x08, 0x00, 0x0D, 0x0A]
)

capa_0_46_nF = bytes(
    [0x2B, 0x30, 0x30, 0x34, 0x36, 0x20, 0x32, 0x20, 0x02, 0x00, 0x04, 0x00, 0x0D, 0x0A]
)

resistance_0_991_kOhm = bytes(
    [0x2B, 0x30, 0x39, 0x39, 0x31, 0x20, 0x31, 0x21, 0x00, 0x20, 0x20, 0x09, 0x0D, 0x0A]
)

resistance_inf_Ohm = bytes(
    [0x2B, 0x3F, 0x30, 0x3A, 0x3F, 0x20, 0x32, 0x21, 0x00, 0x10, 0x20, 0x3D, 0x0D, 0x0A]
)


def test_raw_parse():
    print(f"Size of V86D Raw Data: {sizeof(V86DRawData)}")
    vd_raw_data = V86DRawData.from_buffer_copy(dc_270_2_mV)
    print(vd_raw_data)


def test_parse_volt():
    vd_data = V86DData.deserialize(dc_270_2_mV)
    assert vd_data.unit == ElectricUnit.Volt
    assert vd_data.scale == UnitScale.Mili
    assert vd_data.operation_mode == DMMMode.VoltageDC
    assert vd_data.capture_mode == DMMCaptureMode.Period
    assert vd_data.range_mode == DMMRangeMode.Auto
    assert vd_data.is_beep == False
    assert vd_data.value == pytest.approx(270.2)


def test_parse_celcius():
    vd_data = V86DData.deserialize(temp_31_4_C)
    assert vd_data.unit == ElectricUnit.Celcius
    assert vd_data.scale == UnitScale.NoScale
    assert vd_data.operation_mode == DMMMode.Temperature
    assert vd_data.capture_mode == DMMCaptureMode.Period
    assert vd_data.range_mode == DMMRangeMode.Auto
    assert vd_data.is_beep == False
    assert vd_data.value == pytest.approx(31.4)


def test_parse_ampere():
    vd_data = V86DData.deserialize(ac_2_3_uA)
    assert vd_data.unit == ElectricUnit.Ampere
    assert vd_data.scale == UnitScale.Micro
    assert vd_data.operation_mode == DMMMode.CurrentAC
    assert vd_data.capture_mode == DMMCaptureMode.Period
    assert vd_data.range_mode == DMMRangeMode.Auto
    assert vd_data.is_beep == False
    assert vd_data.value == pytest.approx(2.3)


def test_parse_hfe():
    vd_data = V86DData.deserialize(hfe_2_0_hFE)
    assert vd_data.unit == ElectricUnit.HFE
    assert vd_data.scale == UnitScale.NoScale
    assert vd_data.operation_mode == DMMMode.Inductance
    assert vd_data.capture_mode == DMMCaptureMode.Period
    assert vd_data.range_mode == DMMRangeMode.Manual
    assert vd_data.is_beep == False
    assert vd_data.value == pytest.approx(2.0)


def test_parse_Hz():
    vd_data = V86DData.deserialize(frequency_52_43_Hz)
    assert vd_data.unit == ElectricUnit.Hezt
    assert vd_data.scale == UnitScale.NoScale
    assert vd_data.operation_mode == DMMMode.Frequency
    assert vd_data.capture_mode == DMMCaptureMode.Period
    assert vd_data.range_mode == DMMRangeMode.Auto
    assert vd_data.is_beep == False
    assert vd_data.value == pytest.approx(52.43)


def test_parse_Fara():
    vd_data = V86DData.deserialize(capa_0_46_nF)
    assert vd_data.unit == ElectricUnit.Farad
    assert vd_data.scale == UnitScale.Nano
    assert vd_data.operation_mode == DMMMode.Capacitance
    assert vd_data.capture_mode == DMMCaptureMode.Period
    assert vd_data.range_mode == DMMRangeMode.Auto
    assert vd_data.is_beep == False
    assert vd_data.value == pytest.approx(0.46)


def test_parse_ohm():
    vd_data = V86DData.deserialize(resistance_0_991_kOhm)
    assert vd_data.unit == ElectricUnit.Ohm
    assert vd_data.scale == UnitScale.Kilo
    assert vd_data.operation_mode == DMMMode.Resistance
    assert vd_data.capture_mode == DMMCaptureMode.Period
    assert vd_data.range_mode == DMMRangeMode.Auto
    assert vd_data.is_beep == False
    assert vd_data.value == pytest.approx(0.991)


def test_parse_inf_value():
    vd_data = V86DData.deserialize(resistance_inf_Ohm)
    assert vd_data.unit == ElectricUnit.Ohm
    assert vd_data.scale == UnitScale.Mega
    assert vd_data.operation_mode == DMMMode.Resistance
    assert vd_data.capture_mode == DMMCaptureMode.Period
    assert vd_data.range_mode == DMMRangeMode.Auto
    assert vd_data.is_beep == False
    assert vd_data.value == math.inf
