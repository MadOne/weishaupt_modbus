"""Setting uop my sensor entities."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# from homeassistant.helpers.typing import DiscoveryInfoType
from .const import TYPES
from .entities import BuildEntityList, MyCoordinator
from .hpconst import MODBUS_SYS_ITEMS


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

    entries = []

    entries = BuildEntityList(
        entries, config_entry, MODBUS_SYS_ITEMS, TYPES.NUMBER_RO, coordinator
    )
    entries = BuildEntityList(
        entries, config_entry, MODBUS_SYS_ITEMS, TYPES.SENSOR_CALC, coordinator
    )
    async_add_entities(
        BuildEntityList(
            entries, config_entry, MODBUS_SYS_ITEMS, TYPES.SENSOR, coordinator
        ),
        update_before_add=True,
    )
