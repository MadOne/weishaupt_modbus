"""Setting uop my sensor entities."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import TYPES
from .hpconst import MODBUS_SYS_ITEMS
from .entities import BuildEntityList, MyCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    # config: ConfigType,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    #    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    _modbus_api = config_entry.runtime_data
    coordinator = MyCoordinator(hass, _modbus_api, MODBUS_SYS_ITEMS)
    await coordinator.async_config_entry_first_refresh()

    entries = []

    entries = await BuildEntityList(
        entries, config_entry, MODBUS_SYS_ITEMS, TYPES.NUMBER_RO, coordinator
    )
    entries = await BuildEntityList(
        entries, config_entry, MODBUS_SYS_ITEMS, TYPES.SENSOR_CALC, coordinator
    )
    async_add_entities(
        await BuildEntityList(
            entries, config_entry, MODBUS_SYS_ITEMS, TYPES.SENSOR, coordinator
        ),
        update_before_add=True,
    )
