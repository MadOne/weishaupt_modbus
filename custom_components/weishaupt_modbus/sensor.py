"""Setting uop my sensor entities."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import TYPES
from .hpconst import DEVICELISTS
from .entities import build_entity_list
from .coordinator import MyCoordinator

logging.basicConfig()
log = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    # config: ConfigType,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    #    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    _modbus_api = config_entry.runtime_data

    entries = []

    for _useless, device in enumerate(DEVICELISTS):
        coordinator = MyCoordinator(hass, _modbus_api, device, config_entry)
        await coordinator.async_config_entry_first_refresh()

        entries = await build_entity_list(
            entries, config_entry, device, TYPES.NUMBER_RO, coordinator
        )
        entries = await build_entity_list(
            entries, config_entry, device, TYPES.SENSOR_CALC, coordinator
        )

        log.debug("Adding sensor entries to entity list ..")
        entries = await build_entity_list(
            entries, config_entry, device, TYPES.SENSOR, coordinator
        )

    async_add_entities(
        entries,
        update_before_add=True,
    )
