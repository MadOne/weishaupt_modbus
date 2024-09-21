from dataclasses import dataclass
from datetime import timedelta
from homeassistant.const import UnitOfEnergy, UnitOfTemperature, UnitOfTime, UnitOfVolumeFlowRate, PERCENTAGE

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
    PERCENTAGE = PERCENTAGE
    NUMBER = "Wert"
    STATUS = "Status"
    VOLUMENSTROM = UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR
    KENNLINIE = ""
    TIME_MIN = UnitOfTime.MINUTES
    TIME_H = UnitOfTime.HOURS

FORMATS = FormatConstants()

@dataclass(frozen=True)
class TypeConstants:
    SENSOR = "Sensor"
    SELECT = "Select"
    NUMBER = "Number"

TYPES = TypeConstants()

