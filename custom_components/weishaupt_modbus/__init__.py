"""init."""

import json
import warnings

from attr import asdict

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PREFIX
from homeassistant.core import HomeAssistant

from .const import (
    CONF_DEVICE_POSTFIX,
    CONF_HK2,
    CONF_HK3,
    CONF_HK4,
    CONF_HK5,
    CONF_KENNFELD_FILE,
    CONF_NAME_DEVICE_PREFIX,
    CONF_NAME_TOPIC_PREFIX,
    CONST,
    FORMATS,
    TYPES,
)
from .hpconst import DEVICELISTS, RANGES
from .items import ModbusItem, StatusItem
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

    if True:
        create_string_json()

    # This creates each HA object for each platform your device requires.
    # It's done by calling the `async_setup_entry` function in each platform module.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Migrate old entry."""
    if config_entry.version > 3:
        # This means the user has downgraded from a future version
        return False

    # to ensure all update paths we have to check every version to not overwrite existing entries
    if config_entry.version < 4:
        warnings.warn("Old Version detected")
        new_data = {**config_entry.data}

    if config_entry.version < 2:
        warnings.warn("Version <2 detected")
        new_data[CONF_PREFIX] = CONST.DEF_PREFIX
        new_data[CONF_DEVICE_POSTFIX] = ""
        new_data[CONF_KENNFELD_FILE] = CONST.DEF_KENNFELDFILE
    if config_entry.version < 3:
        warnings.warn("Version <3 detected")
        new_data[CONF_HK2] = False
        new_data[CONF_HK3] = False
        new_data[CONF_HK4] = False
        new_data[CONF_HK5] = False
    if config_entry.version < 4:
        warnings.warn("Version <4 detected")
        new_data[CONF_NAME_DEVICE_PREFIX] = False
        new_data[CONF_NAME_TOPIC_PREFIX] = False

        hass.config_entries.async_update_entry(
            config_entry, data=new_data, minor_version=1, version=4
        )
        warnings.warn("Config entries updated to version 4")

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


def create_string_json():
    item: ModbusItem = None
    myStatusItem: StatusItem = None
    myEntity = {}
    myJson = {}
    mySensors = {}
    myNumbers = {}
    mySelects = {}

    # generate list of all mbitems
    DEVICELIST = []
    for devicelist in DEVICELISTS:
        DEVICELIST = DEVICELIST + devicelist

    for item in DEVICELIST:
        match item.type:
            case TYPES.SENSOR | TYPES.NUMBER_RO | TYPES.SENSOR_CALC:
                mySensor = {}
                mySensor["name"] = item.name
                if item.resultlist is not None:
                    if item.format is FORMATS.STATUS:
                        myValues = {}
                        for myStatusItem in item.resultlist:
                            myValues[myStatusItem.translation_key] = myStatusItem.text
                        mySensor["state"] = myValues.copy()
                mySensors[item.translation_key] = mySensor.copy()
            case TYPES.NUMBER:
                myNumber = {}
                myNumber["name"] = item.name
                if item.resultlist is not None:
                    if item.format is FORMATS.STATUS:
                        myValues = {}
                        for myStatusItem in item.resultlist:
                            myValues[myStatusItem.translation_key] = myStatusItem.text
                        myNumber["value"] = myValues.copy()
                myNumbers[item.translation_key] = myNumber.copy()
            case TYPES.SELECT:
                mySelect = {}
                mySelect["name"] = item.name
                if item.resultlist is not None:
                    if item.format is FORMATS.STATUS:
                        myValues = {}
                        for myStatusItem in item.resultlist:
                            myValues[myStatusItem.translation_key] = myStatusItem.text
                        mySelect["state"] = myValues.copy()
                mySelects[item.translation_key] = mySelect.copy()
    myEntity["sensor"] = mySensors
    myEntity["number"] = myNumbers
    myEntity["select"] = mySelects
    myJson["entity"] = myEntity

    # iterate over all devices in order to create a translation. TODO
    # for key, value in asdict(DEVICES).items():
    #    ...

    # load strings.json into string
    with open(
        "config/custom_components/weishaupt_modbus/strings.json",
        "r",
        # encoding="utf-8",
    ) as file:
        data = file.read()
    # create dict from json
    data_dict = json.loads(data)
    # overwrite entiy dict
    data_dict["entity"] = myEntity
    # write whole json to file again
    with open(
        "config/custom_components/weishaupt_modbus/strings.json",
        "w",
        # encoding="utf-8",
    ) as file:
        file.write(json.dumps(data_dict, indent=4, sort_keys=True, ensure_ascii=False))
