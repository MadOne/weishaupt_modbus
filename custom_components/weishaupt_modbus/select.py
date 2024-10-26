"""Select."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import TYPES
from .hpconst import MODBUS_SYS_ITEMS
from .entities import BuildEntityList, MyCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Select entry setup."""
    _modbus_api = config_entry.runtime_data
    coordinator = MyCoordinator(hass, _modbus_api, MODBUS_SYS_ITEMS)
    await coordinator.async_config_entry_first_refresh()

    entries = []

    async_add_entities(
        await BuildEntityList(
            entries, config_entry, MODBUS_SYS_ITEMS, TYPES.SELECT, coordinator
        ),
        update_before_add=True,
    )
