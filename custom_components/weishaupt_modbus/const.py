from dataclasses import dataclass
from datetime import timedelta
from homeassistant.const import UnitOfEnergy, UnitOfTemperature

@dataclass(frozen=True)
class MainConstants:
    DOMAIN = "weishaupt_integ"
    SCAN_INTERVAL = timedelta(minutes=1)
    UNIQUE_ID = "unique_id"
    APPID = 100

CONST = MainConstants()

@dataclass(frozen=True)
class FormatConstants:
    TEMPERATUR = UnitOfTemperature.CELSIUS
    ENERGY = UnitOfEnergy.KILO_WATT_HOUR
    PERCENTAGE = "%"
    NUMBER = "Wert"
    STATUS = "Status"
    VOLUMENSTROM = "m³/h"
    KENNLINIE = ""

FORMATS = FormatConstants()

@dataclass(frozen=True)
class TypeConstants:
    SENSOR = "Sensor"
    SELECT = "Select"
    NUMBER = "Number"

TYPES = TypeConstants()

