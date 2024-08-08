"""Platform for Wattio integration testing."""

from __future__ import annotations

import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT  # STATE_ON
from homeassistant.core import HomeAssistant

# from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import wp
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


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
            WW_SGReady(host, port),
        ],
        update_before_add=True,
    )


class WW_SGReady(SwitchEntity):
    """Representation of Switch Sensor."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, host, port) -> None:
        """Initialize the sensor."""
        self._host = host
        self._port = port
        self._attr_state = "off"

    _attr_name = "SG-Ready"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True

    @property
    def is_on(self):
        """Return is_on status."""
        if self._attr_state == "on":
            return True
        return False

    async def async_turn_on(self):
        """Turn On method."""
        # self._attr_state = "on"
        # whp = wp.heat_pump(self._host, self._port)
        # whp.connect()
        # whp.WW_SGReady = 1
        # self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn Off method."""
        # self._attr_state = "off"
        # whp = wp.heat_pump(self._host, self._port)
        # whp.connect()
        # whp.WW_SGReady = 0
        # self.async_write_ha_state()

    async def async_update(self):
        """Update switch."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        if whp.WW_SGReady == 1:
            self._attr_state = "on"
        elif whp.WW_SGReady == 0:
            self._attr_state = "off"
        self._attr_state = whp.WW_SGReady

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Warmwasser")},
            "name": "Wärmepumpe-Warmwasser",
            "manufacturer": "Weishaupt",
        }
