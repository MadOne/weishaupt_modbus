"""Helpers for entity migration"""

import logging

from homeassistant.util import slugify
from homeassistant.helpers import entity_registry as er
from homeassistant.const import CONF_PREFIX

from .const import (
    CONF_DEVICE_POSTFIX,
    CONF_NAME_DEVICE_PREFIX,
    CONF_NAME_TOPIC_PREFIX,
    CONST,
    TYPES,
)
from .hpconst import reverse_device_list
from .items import ModbusItem
from .configentry import MyConfigEntry

logging.basicConfig()
log = logging.getLogger(__name__)


def create_old_id(config_entry: MyConfigEntry, modbus_item: ModbusItem):
    """created an entity ID according to old style"""
    if config_entry.data[CONF_NAME_DEVICE_PREFIX]:
        name_device_prefix = config_entry.data[CONF_PREFIX] + "_"
    else:
        name_device_prefix = ""

    if config_entry.data[CONF_NAME_TOPIC_PREFIX]:
        name_topic_prefix = reverse_device_list[modbus_item.device] + "_"
    else:
        name_topic_prefix = ""

    entity_name = name_topic_prefix + name_device_prefix + modbus_item.name

    return slugify(entity_name)


def create_new_entity_id(
    config_entry: MyConfigEntry, modbus_item: ModbusItem, platform: str
):
    """created an entity ID according to new style"""
    dev_postfix = "_" + config_entry.data[CONF_DEVICE_POSTFIX]
    if dev_postfix == "_":
        dev_postfix = ""

    device_name = modbus_item.device + dev_postfix

    if config_entry.data[CONF_NAME_DEVICE_PREFIX]:
        name_device_prefix = CONST.DEF_PREFIX + "_"
    else:
        name_device_prefix = ""

    if config_entry.data[CONF_NAME_TOPIC_PREFIX]:
        name_topic_prefix = reverse_device_list[modbus_item.device] + "_"
    else:
        name_topic_prefix = ""

    entity_name = name_topic_prefix + name_device_prefix + modbus_item.translation_key

    return str(platform + "." + slugify(device_name + "_" + entity_name))


def create_unique_id(config_entry: MyConfigEntry, modbus_item: ModbusItem):
    """created an UID according to old style"""
    dev_postfix = "_" + config_entry.data[CONF_DEVICE_POSTFIX]

    if dev_postfix == "_":
        dev_postfix = ""

    return str(config_entry.data[CONF_PREFIX] + modbus_item.name + dev_postfix)


def migrate_entities(
    config_entry: MyConfigEntry,
    modbusitems: ModbusItem,
):
    """Build entity list.

    function builds a list of entities that can be used as parameter by async_setup_entry()
    type of list is defined by the ModbusItem's type flag
    so the app only holds one list of entities that is build from a list of ModbusItem
    stored in hpconst.py so far, will be provided by an external file in future
    """
    entity_registry = er.async_get(config_entry.runtime_data.hass)

    for _useless, item in enumerate(modbusitems):
        platform = ""
        match item.type:
            # here the entities are created with the parameters provided
            # by the ModbusItem object
            case TYPES.SENSOR | TYPES.NUMBER_RO | TYPES.SENSOR_CALC:
                platform = "sensor"
            case TYPES.SELECT:
                platform = "select"
            case TYPES.NUMBER:
                platform = "number"

        old_id = create_old_id(config_entry, item)
        old_uid = create_unique_id(config_entry, item)
        new_entity_id = create_new_entity_id(config_entry, item, platform)
        old_entity_id = entity_registry.async_get_entity_id(
            platform, CONST.DOMAIN, old_uid
        )

        if new_entity_id == old_entity_id:
            log.info("already migrated")
            return

        if old_entity_id is not None:
            entity_registry.async_update_entity(
                old_entity_id,
                new_entity_id=new_entity_id,
            )

            log.info(
                "Init UID:%s, platform:%s old ID:%s --> %s new ID:%s",
                old_uid,
                platform,
                old_id,
                old_entity_id,
                new_entity_id,
            )
