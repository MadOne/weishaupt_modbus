"""Number."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import TYPES
from .hpconst import DEVICELISTS
from .entities import build_entity_list
from .coordinator import MyCoordinator
from . import MyConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    _modbus_api = config_entry.runtime_data.modbus_api

    # start with an empty list of entries
    entries = []

    for _useless, device in enumerate(DEVICELISTS):
        # we create one communicator per device and entry platform. This allows better scheduling than one
        coordinator = MyCoordinator(hass, _modbus_api, device, config_entry)
        #
        await coordinator.async_config_entry_first_refresh()

        entries = await build_entity_list(
            entries, config_entry, device, TYPES.NUMBER, coordinator
        )

    async_add_entities(
        entries,
        update_before_add=True,
    )
