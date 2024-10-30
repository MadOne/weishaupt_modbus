"""init."""

import warnings

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_PREFIX

from .const import CONST, CONF_DEVICE_POSTFIX, CONF_KENNFELD_FILE, CONF_HK2, CONF_HK3, CONF_HK4, CONF_HK5
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


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Migrate old entry."""
    warnings.warn("Check if migration of config entries is necessary.")
    if config_entry.version > 2:
        # This means the user has downgraded from a future version
        return False

    if config_entry.version < 3:
        warnings.warn("Version 1 detected")
        new_data = {**config_entry.data}
        warnings.warn("Minor version 1 detected")
        new_data[CONF_PREFIX] = CONST.DEF_PREFIX
        new_data[CONF_DEVICE_POSTFIX] = ""
        new_data[CONF_KENNFELD_FILE] = CONST.DEF_KENNFELDFILE
        new_data[CONF_HK2] = False
        new_data[CONF_HK3] = False
        new_data[CONF_HK4] = False
        new_data[CONF_HK5] = False
        
        warnings.warn("Update entries")

        hass.config_entries.async_update_entry(
            config_entry, data=new_data, minor_version=1, version=2
        )

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
