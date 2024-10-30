"""Number."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
# from homeassistant.helpers.typing import DiscoveryInfoType

# from time import gmtime, strftime
from .const import TYPES
from .hpconst import ITEMLISTS
from .entities import build_entity_list, MyCoordinator
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

    entries = []

    for _useless, item in enumerate(ITEMLISTS):
        coordinator = MyCoordinator(hass, _modbus_api, item)
        await coordinator.async_config_entry_first_refresh()

        entries = await build_entity_list(
            entries, config_entry, item, TYPES.NUMBER, coordinator
        )

    async_add_entities(
        entries,
        update_before_add=True,
    )
