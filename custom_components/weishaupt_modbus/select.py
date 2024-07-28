"""Select platform for wemportal component."""

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import wp
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Select entry setup."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    async_add_entities(
        [
            Sys_Betriebsart(host, port),
            HK_Konfiguration(host, port),
        ],
        update_before_add=True,
    )


class Sys_Betriebsart(SelectEntity):
    """Representation of a WEM Portal Sensor."""

    _attr_name = "Systembetriebsart"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    options = ["AUTOMATIK", "HEIZEN", "KÜHLEN", "SOMMER", "STANDBY", "2.WEZ", "FEHLER"]
    _attr_current_option = "FEHLER"

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self.async_internal_will_remove_from_hass_port = port

    async def async_select_option(self, option: str) -> None:
        """Call the API to change the parameter value."""

        self._attr_current_option = option

        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        # await self.coordinator.async_request_refresh()
        whp = wp.heat_pump("10.10.1.225", 502)
        whp.connect()
        self._attr_current_option = whp.Sys_Betriebsart

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "System")},
        }


class HK_Konfiguration(SelectEntity):
    """Representation of a WEM Portal Sensor."""

    _attr_name = "Konfiguration"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    options = [
        "AUS",
        "PUMPENKREIS",
        "MISCHKREIS",
        "SOLLWERT (PUMPE M1)",
        "FEHLER",
    ]
    _attr_current_option = "FEHLER"

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_select_option(self, option: str) -> None:
        """Call the API to change the parameter value."""

        self._attr_current_option = option

        self.async_write_ha_state()

    async def async_update(
        self,
    ) -> None:
        """Update Entity Only used by the generic entity update service."""
        # await self.coordinator.async_request_refresh()
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_current_option = whp.HK_Konfiguration

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }
