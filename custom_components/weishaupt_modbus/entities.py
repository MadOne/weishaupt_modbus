"""Build entitiy List and Update Coordinator."""

import logging

from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT, CONF_PREFIX
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_DEVICE_POSTFIX,
    CONF_HK2,
    CONF_HK3,
    CONF_HK4,
    CONF_HK5,
    CONF_NAME_DEVICE_PREFIX,
    CONF_NAME_TOPIC_PREFIX,
    CONST,
    DEVICES,
    FORMATS,
    TYPES,
)
from .coordinator import MyCoordinator
from .hpconst import reverse_device_list
from .items import ModbusItem
from .kennfeld import PowerMap
from .modbusobject import ModbusAPI, ModbusObject
from . import MyConfigEntry

logging.basicConfig()
log = logging.getLogger(__name__)


async def check_available(modbus_item: ModbusItem, config_entry: MyConfigEntry) -> bool:
    """function checks if item is valid and available"""
    log.debug("Check if item %s is available ..", modbus_item.name)
    if config_entry.data[CONF_HK2] is False:
        if modbus_item.device is DEVICES.HZ2:
            return False

    if config_entry.data[CONF_HK3] is False:
        if modbus_item.device is DEVICES.HZ3:
            return False

    if config_entry.data[CONF_HK4] is False:
        if modbus_item.device is DEVICES.HZ4:
            return False

    if config_entry.data[CONF_HK5] is False:
        if modbus_item.device is DEVICES.HZ5:
            return False

    _modbus_api = config_entry.runtime_data.modbus_api
    mbo = ModbusObject(_modbus_api, modbus_item)
    _useless = await mbo.value
    if modbus_item.is_invalid is False:
        log.debug("Check availability item %s successful ..", modbus_item.name)
        return True
    return False


async def build_entity_list(
    entries,
    config_entry: MyConfigEntry,
    modbusitems: ModbusItem,
    item_type,
    coordinator: MyCoordinator,
):
    """Build entity list.

    function builds a list of entities that can be used as parameter by async_setup_entry()
    type of list is defined by the ModbusItem's type flag
    so the app only holds one list of entities that is build from a list of ModbusItem
    stored in hpconst.py so far, will be provided by an external file in future
    """

    for index, item in enumerate(modbusitems):
        if item.type == item_type:
            if (
                await check_available(modbusitems[index], config_entry=config_entry)
                is True
            ):
                match item_type:
                    # here the entities are created with the parameters provided
                    # by the ModbusItem object
                    case TYPES.SENSOR | TYPES.NUMBER_RO:
                        log.debug(
                            "Add item %s to entity list ..", modbusitems[index].name
                        )
                        entries.append(
                            MySensorEntity(
                                config_entry, modbusitems[index], coordinator, index
                            )
                        )
                    case TYPES.SENSOR_CALC:
                        pwrmap = PowerMap(config_entry)
                        await pwrmap.initialize()
                        log.debug(
                            "Add item %s to entity list ..", modbusitems[index].name
                        )
                        entries.append(
                            MyCalcSensorEntity(
                                config_entry,
                                modbusitems[index],
                                coordinator,
                                index,
                                pwrmap,
                            )
                        )
                    case TYPES.SELECT:
                        entries.append(
                            MySelectEntity(
                                config_entry, modbusitems[index], coordinator, index
                            )
                        )
                    case TYPES.NUMBER:
                        entries.append(
                            MyNumberEntity(
                                config_entry, modbusitems[index], coordinator, index
                            )
                        )

    return entries


class MyEntity(Entity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
    should_poll
    async_update
    async_added_to_hass
    available

    The base class for entities that hold general parameters
    """

    _config_entry = None
    _modbus_item = None
    _divider = 1
    # _attr_name = None
    _attr_unique_id = ""
    _attr_should_poll = True
    _attr_translation_key = ""
    _attr_has_entity_name = True
    _dev_device = ""
    _modbus_api = None

    def __init__(
        self, config_entry: MyConfigEntry, modbus_item: ModbusItem, modbus_api: ModbusAPI
    ) -> None:
        """Initialize the entity."""
        self._config_entry = config_entry
        self._modbus_item = modbus_item

        dev_postfix = ""
        dev_postfix = "_" + self._config_entry.data[CONF_DEVICE_POSTFIX]

        if dev_postfix == "_":
            dev_postfix = ""

        dev_prefix = CONST.DEF_PREFIX
        dev_prefix = self._config_entry.data[CONF_PREFIX]

        if self._config_entry.data[CONF_NAME_DEVICE_PREFIX]:
            name_device_prefix = self._config_entry.data[CONF_PREFIX] + "_"
        else:
            name_device_prefix = ""

        if self._config_entry.data[CONF_NAME_TOPIC_PREFIX]:
            name_topic_prefix = reverse_device_list[self._modbus_item.device] + "_"
        else:
            name_topic_prefix = ""

        name_prefix = name_topic_prefix + name_device_prefix

        self._attr_translation_key = self._modbus_item.translation_key
        self._attr_translation_placeholders = {"prefix": name_prefix}

        # self._attr_name = None  # name_prefix + self._modbus_item.name
        self._attr_unique_id = dev_prefix + self._modbus_item.name + dev_postfix
        self._dev_device = self._modbus_item.device + dev_postfix
        self._modbus_api = modbus_api

        if self._modbus_item._format != FORMATS.STATUS:
            self._attr_native_unit_of_measurement = self._modbus_item._format

            match self._modbus_item._format:
                case FORMATS.ENERGY:
                    self._attr_state_class = SensorStateClass.TOTAL_INCREASING
                case (
                    FORMATS.TEMPERATUR
                    | FORMATS.POWER
                    | FORMATS.PERCENTAGE
                    | FORMATS.TIME_H
                    | FORMATS.TIME_MIN
                    | FORMATS.UNKNOWN
                ):
                    self._attr_state_class = SensorStateClass.MEASUREMENT

            if self._modbus_item.resultlist is not None:
                self._attr_native_min_value = self._modbus_item.get_number_from_text(
                    "min"
                )
                self._attr_native_max_value = self._modbus_item.get_number_from_text(
                    "max"
                )
                self._attr_native_step = self._modbus_item.get_number_from_text("step")
                self._divider = self._modbus_item.get_number_from_text("divider")
                self._attr_device_class = self._modbus_item.get_text_from_number(-1)

    def calc_temperature(self, val: float) -> float:
        """Calcualte temperature."""
        match val:
            case None:
                return None
            case -32768:
                # No Sensor installed, remove it from the list
                return -1
            case -32767:
                # Sensor broken set return value to -99.9 to inform user
                return -99.9
            case 32768:
                # Dont know. seems to be zero..
                return None
            case range(-500, 5000):
                # Valid Temperatur range
                return int(val) / self._divider
            case _:
                # to optimize, seems to be Einerkomplement
                if val > 32768:
                    val = val - 65536
                return int(val) / self._divider

    def calc_percentage(self, val: float) -> float:
        """Calculate percentage."""
        if val is None:
            return None
        if val == 65535:
            return None
        return int(val) / self._divider

    def translate_val(self, val) -> float:
        """Translate modbus value into sensful format."""
        if val is None:
            return val
        match self._modbus_item.format:
            case FORMATS.TEMPERATUR:
                return self.calc_temperature(val)
            case FORMATS.PERCENTAGE:
                return self.calc_percentage(val)
            case FORMATS.STATUS:
                return self._modbus_item.get_translation_key_from_number(val)
            case FORMATS.UNKNOWN:
                return int(val)
            case _:
                return int(val) / self._divider

    def retranslate_val(self, value) -> int:
        """Re-translate modbus value into sensful format."""
        val = None
        match self._modbus_item.format:
            # logically, this belongs to the ModbusItem, but doing it here
            case FORMATS.STATUS:
                val = self._modbus_item.get_number_from_translation_key(value)
            case _:
                val = value * self._divider
        return val

    async def set_translate_val(self, value) -> None:
        """Translate and writes a value to the modbus."""
        val = self.retranslate_val(value)

        await self._modbus_api.connect()
        mbo = ModbusObject(self._modbus_api, self._modbus_item)
        await mbo.setvalue(val)

    def my_device_info(self) -> DeviceInfo:
        """Build the device info."""
        return {
            "identifiers": {(CONST.DOMAIN, self._dev_device)},
            # "name": self._dev_device,
            "translation_key": self._dev_device,
            "sw_version": "Device_SW_Version",
            "model": "Device_model",
            "manufacturer": "Weishaupt",
        }


class MySensorEntity(CoordinatorEntity, SensorEntity, MyEntity):
    """Class that represents a sensor entity.

    Derived from Sensorentity
    and decorated with general parameters from MyEntity
    """

    _attr_native_unit_of_measurement = None
    _attr_device_class = None
    _attr_state_class = None

    def __init__(
        self,
        config_entry: MyConfigEntry,
        modbus_item: ModbusItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        super().__init__(coordinator, context=idx)
        self.idx = idx
        MyEntity.__init__(self, config_entry, modbus_item, coordinator._modbus_api)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.translate_val(self._modbus_item.state)
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)


class MyCalcSensorEntity(MySensorEntity):
    """class that represents a sensor entity.

    Derived from Sensorentity
    and decorated with general parameters from MyEntity
    """

    # calculates output from map
    my_map = None

    def __init__(
        self,
        config_entry: MyConfigEntry,
        modbus_item: ModbusItem,
        coordinator: MyCoordinator,
        idx,
        pwrmap: PowerMap,
    ) -> None:
        MySensorEntity.__init__(self, config_entry, modbus_item, coordinator, idx)
        self.my_map = pwrmap

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.translate_val(self._modbus_item.state)
        self.async_write_ha_state()

    def calc_power(self, val, x, y):
        """Calculate heating power from power map."""
        if val is None:
            return val
        return (val / 100) * self.my_map.map(x, y)

    def translate_val(self, val):
        """Translate a value from the modbus."""
        # this is necessary to avoid errors when re-connection heatpump
        if val is None:
            return None
        if len(val) < 3:
            return None
        if val[0] is None:
            return None
        if val[1] is None:
            return None
        if val[2] is None:
            return None

        val_0 = self.calc_percentage(val[0])
        val_x = self.calc_temperature(val[1])
        if val_x is None:
            return None
        val_x = val_x / 10
        val_y = self.calc_temperature(val[2])
        if val_y is None:
            return None
        val_y = val_y / 10

        match self._modbus_item.format:
            case FORMATS.POWER:
                return round(self.calc_power(val_0, val_x, val_y))
            case _:
                if val_0 is None:
                    return None
                return round(val_0 / self._divider)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MySensorEntity.my_device_info(self)


class MyNumberEntity(CoordinatorEntity, NumberEntity, MyEntity):
    """class that represents a sensor entity derived from Sensorentity
    and decorated with general parameters from MyEntity
    """

    _attr_native_unit_of_measurement = None
    _attr_device_class = None
    _attr_state_class = None
    _attr_native_min_value = 10
    _attr_native_max_value = 60

    def __init__(
        self,
        config_entry: MyConfigEntry,
        modbus_item: ModbusItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, modbus_item, coordinator._modbus_api)

        if self._modbus_item.resultlist is not None:
            self._attr_native_min_value = self._modbus_item.get_number_from_text("min")
            self._attr_native_max_value = self._modbus_item.get_number_from_text("max")
            self._attr_native_step = self._modbus_item.get_number_from_text("step")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.translate_val(self._modbus_item.state)
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        await self.set_translate_val(value)
        self._modbus_item.state = int(self.retranslate_val(value))
        self._attr_native_value = self.translate_val(self._modbus_item.state)
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)


class MySelectEntity(CoordinatorEntity, SelectEntity, MyEntity):
    """class that represents a sensor entity derived from Sensorentity
    and decorated with general parameters from MyEntity
    """

    options = []
    _attr_current_option = "FEHLER"

    def __init__(
        self,
        config_entry: MyConfigEntry,
        modbus_item: ModbusItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, modbus_item, coordinator._modbus_api)
        self.async_internal_will_remove_from_hass_port = self._config_entry.data[
            CONF_PORT
        ]
        # option list build from the status list of the ModbusItem
        self.options = []
        for _useless, item in enumerate(self._modbus_item._resultlist):
            self.options.append(item.translation_key)

    async def async_select_option(self, option: str) -> None:
        # the synching is done by the ModbusObject of the entity
        await self.set_translate_val(option)
        self._modbus_item.state = int(self.retranslate_val(option))
        self._attr_current_option = self.translate_val(self._modbus_item.state)
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_current_option = self.translate_val(self._modbus_item.state)
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)
