from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

# from time import gmtime, strftime
from .const import TYPES
from .hpconst import MODBUS_SYS_ITEMS
from .entities import BuildEntityList


async def async_setup_entry(
    hass: HomeAssistant,
    # config: ConfigType,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    Entries = []

    async_add_entities(
        BuildEntityList(Entries, config_entry, MODBUS_SYS_ITEMS, TYPES.NUMBER),
        update_before_add=True,
    )
