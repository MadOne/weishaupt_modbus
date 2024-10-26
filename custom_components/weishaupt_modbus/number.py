"""Number."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
# from homeassistant.helpers.typing import DiscoveryInfoType

# from time import gmtime, strftime
from .const import TYPES
from .hpconst import MODBUS_SYS_ITEMS
from .entities import BuildEntityList, MyCoordinator
# from .modbusobject import ModbusAPI


async def async_setup_entry(
    hass: HomeAssistant,
    # config: ConfigType,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    # discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    _modbus_api = config_entry.runtime_data
    coordinator = MyCoordinator(hass, _modbus_api, MODBUS_SYS_ITEMS)
    await coordinator.async_config_entry_first_refresh()

    entries = []

    async_add_entities(
        await BuildEntityList(
            entries, config_entry, MODBUS_SYS_ITEMS, TYPES.NUMBER, coordinator
        ),
        update_before_add=True,
    )
