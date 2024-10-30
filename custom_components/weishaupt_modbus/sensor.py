"""Setting uop my sensor entities."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import TYPES
from .hpconst import ITEMLISTS
from .entities import build_entity_list, MyCoordinator


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

    for index, item in enumerate(ITEMLISTS):
        coordinator = MyCoordinator(hass, _modbus_api, item)
        await coordinator.async_config_entry_first_refresh()

        entries = await build_entity_list(
            entries, config_entry, item, TYPES.NUMBER_RO, coordinator
        )
        entries = await build_entity_list(
            entries, config_entry, item, TYPES.SENSOR_CALC, coordinator
        )

        entries = await build_entity_list(
            entries, config_entry, item, TYPES.SENSOR, coordinator
        )

    async_add_entities(
        entries,
        update_before_add=True,
    )
