import enum


class UnitScale(enum.Enum):
    Tera = "T"
    Giga = "G"
    Mega = "M"
    Kilo = "k"
    NoScale = ""
    Centi = "c"
    Mili = "m"
    Micro = "u"
    Nano = "n"
    Pico = "p"


class ElectricUnit(enum.Enum):
    Volt = "V"
    Ampere = "A"
    Ohm = "Ohm"
    Farad = "F"
    Coulomb = "Q"
    Hezt = "Hz"
    Henry = "H"
    Watts = "W"
    Celcius = "Celcius"
    HFE = "HFE"
    Faraheit = "Faraheit"
    Percentage = "%"


class DMMMode(enum.Enum):
    CurrentAC = 1
    CurrentDC = 2
    VoltageAC = 3
    VoltageDC = 4
    Resistance = 5
    Diode = 6
    Capacitance = 7
    Frequency = 8
    Temperature = 9
    Inductance = 10
    Continuity = 11


class DMMCaptureMode(enum.Enum):
    Period = 0
    Hold = 1
    Min = 2
    Max = 3
    Avg = 4
    Relative = 4


class DMMRangeMode(enum.Enum):
    Auto = 0
    Manual = 1


class DMMOptions(enum.Enum):
    Beep = 0
    AutoPowerOff = 1
    LowBatteryWarning = 2
