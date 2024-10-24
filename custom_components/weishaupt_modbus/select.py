"""Select."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import TYPES
from .entities import BuildEntityList
from .hpconst import MODBUS_SYS_ITEMS


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Select entry setup."""
    Entries = []

    async_add_entities(
        BuildEntityList(Entries, config_entry, MODBUS_SYS_ITEMS, TYPES.SELECT),
        update_before_add=True,
    )
