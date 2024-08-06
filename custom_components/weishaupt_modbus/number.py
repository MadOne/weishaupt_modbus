"""Number platform for wemportal component."""

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType

from . import wp
from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the wemportal component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
) -> None:
    """Set up Numbers."""
    hass.data.setdefault(DOMAIN, {})
    # hub = hass.data[DOMAIN][config_entry.entry_id]
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    # port = config_entry.data.get[CONF_PORT]
    # host = "10.10.1.225"
    # port = "502"
    async_add_entities(
        [WW_Normal(host, port), WW_Absenk(host, port)], update_before_add=True
    )


class WW_Normal(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "WW Normal"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 40
    _attr_native_max_value = 60
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        whp = wp.heat_pump(host, port)
        whp.connect()
        self._attr_native_value = whp.WW_Normal
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.WW_Normal = int(value)

        self._attr_native_value = whp.WW_Normal
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.WW_Normal

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Warmwasser")},
        }


class WW_Absenk(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "WW Absenk"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 30
    _attr_native_max_value = 40
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        whp = wp.heat_pump(host, port)
        whp.connect()
        self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.WW_Absenk = int(value)

        self._attr_native_value = whp.WW_Absenk
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.WW_Absenk

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Warmwasser")},
        }
