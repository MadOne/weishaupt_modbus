from dataclasses import dataclass
from datetime import timedelta

@dataclass(frozen=True)
class MainConstants:
    DOMAIN = "weishaupt_integ"
    SCAN_INTERVAL = timedelta(minutes=1)
    UNIQUE_ID = "unique_id"
    APPID = 100

CONST = MainConstants()

@dataclass(frozen=True)
class FormatConstants:
    TEMPERATUR = "Temperatur"
    PERCENTAGE = "Prozent"
    NUMBER = "Nummer"
    STATUS = "Status"

FORMATS = FormatConstants()

@dataclass(frozen=True)
class TypeConstants:
    SENSOR = "Sensor"
    SELECT = "Select"
    NUMBER = "Number"

TYPES = TypeConstants()

