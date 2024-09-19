from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import TYPES
from .hpconst import MODBUS_SYS_ITEMS
from .entities import BuildEntityList

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Select entry setup."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    Entries = []

    async_add_entities(BuildEntityList(Entries, host, port, MODBUS_SYS_ITEMS,TYPES.SELECT), update_before_add=True)
