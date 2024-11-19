"""my config entry"""

from dataclasses import dataclass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
# from .modbusobject import ModbusAPI


@dataclass
class MyData:
    """My config data"""

    modbus_api: any
    config_dir: str
    hass: HomeAssistant


type MyConfigEntry = ConfigEntry[MyData]
