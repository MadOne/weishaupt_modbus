"""init."""

import warnings

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONST
from .modbusobject import ModbusAPI

PLATFORMS: list[str] = [
    "number",
    "select",
    "sensor",
    #    "switch",
]


# Return boolean to indicate that initialization was successful.
# return True
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up entry."""
    # Store an instance of the "connecting" class that does the work of speaking
    # with your actual devices.
    # hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub.Hub(hass, entry.data["host"])
    mbapi = ModbusAPI(entry)
    await mbapi.connect()
    entry.runtime_data = mbapi

    # This creates each HA object for each platform your device requires.
    # It's done by calling the `async_setup_entry` function in each platform module.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    entry.runtime_data.close()
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        try:
            hass.data[CONST.DOMAIN].pop(entry.entry_id)
        except KeyError:
            warnings.warn("KeyError: " + str(CONST.DOMAIN))

    return unload_ok
