import warnings
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.components.select import SelectEntity
from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfEnergy, UnitOfTemperature
from homeassistant.helpers.device_registry import DeviceInfo
from .const import CONST, FORMATS, TYPES
from .modbusobject import ModbusObject
from .items import ModbusItem
from .hpconst import TEMPRANGE_STD, DEVICES
from .kennfeld import PowerMap


def BuildEntityList(entries, config_entry, modbusitems, type):
    # this builds a list of entities that can be used as parameter by async_setup_entry()
    # type of list is defined by the ModbusItem's type flag
    # so the app only holds one list of entities that is build from a list of ModbusItem
    # stored in hpconst.py so far, will be provided by an external file in future
    for index, item in enumerate(modbusitems):
        if item.type == type:
            match type:
                # here the entities are created with the parameters provided by the ModbusItem object
                case TYPES.SENSOR | TYPES.NUMBER_RO:
                    entries.append(MySensorEntity(config_entry, modbusitems[index]))
                case TYPES.SENSOR_CALC:
                    entries.append(MyCalcSensorEntity(config_entry, modbusitems[index]))
                case TYPES.SELECT:
                    entries.append(MySelectEntity(config_entry, modbusitems[index]))
                case TYPES.NUMBER:
                    entries.append(MyNumberEntity(config_entry, modbusitems[index]))

    return entries


class MyEntity:
    # The base class for entities that hold general parameters
    _config_entry = None
    _modbus_item = None
    _divider = 1
    _attr_name = ""
    _attr_unique_id = ""
    _attr_should_poll = True
    _dev_device = ""

    def __init__(self, config_entry, modbus_item) -> None:
        self._config_entry = config_entry
        self._modbus_item = modbus_item
        self._attr_name = self._modbus_item.name
        self._attr_unique_id = CONST.DOMAIN + self._attr_name
        self._dev_device = self._modbus_item.device

        if self._modbus_item._format != FORMATS.STATUS:
            self._attr_native_unit_of_measurement = self._modbus_item._format

            if self._modbus_item._format == FORMATS.ENERGY:
                self._attr_state_class = SensorStateClass.TOTAL_INCREASING
            if self._modbus_item._format == FORMATS.TEMPERATUR:
                self._attr_state_class = SensorStateClass.MEASUREMENT
            if self._modbus_item._format == FORMATS.POWER:
                self._attr_state_class = SensorStateClass.MEASUREMENT

            if self._modbus_item.resultlist != None:
                self._attr_native_min_value = self._modbus_item.getNumberFromText("min")
                self._attr_native_max_value = self._modbus_item.getNumberFromText("max")
                self._attr_native_step = self._modbus_item.getNumberFromText("step")
                self._divider = self._modbus_item.getNumberFromText("divider")
                self._attr_device_class = self._modbus_item.getTextFromNumber(-1)

    def calcTemperature(self, val: float):
        if val == None:
            return None
        if val == -32768:
            return -1
        if val == -32767:
            return -2
        if val == 32768:
            return None
        return val / self._divider

    def calcPercentage(self, val: float):
        if val == None:
            return None
        if val == 65535:
            return None
        return val / self._divider

    @property
    async def translateVal(self):
        # reads an translates a value from the modbus
        mbo = ModbusObject(self._config_entry, self._modbus_item)
        if mbo == None:
            return None
        val = await mbo.value
        match self._modbus_item.format:
            case FORMATS.TEMPERATUR:
                return self.calcTemperature(val)
            case FORMATS.PERCENTAGE:
                return self.calcPercentage(val)
            case FORMATS.STATUS:
                return self._modbus_item.getTextFromNumber(val)
            case _:
                if val == None:
                    return val
                return val / self._divider

    # @translateVal.setter
    async def settranslateVal(self, value):
        # translates and writes a value to the modbus
        mbo = ModbusObject(self._config_entry, self._modbus_item)
        if mbo == None:
            return
        val = None
        match self._modbus_item.format:
            # logically, this belongs to the ModbusItem, but doing it here
            case FORMATS.STATUS:
                val = self._modbus_item.getNumberFromText(value)
            case _:
                val = value * self._divider
        await mbo.setvalue(val)  # = val

    def my_device_info(self) -> DeviceInfo:
        # helper to build the device info
        return {
            "identifiers": {(CONST.DOMAIN, self._dev_device)},
            "name": self._dev_device,
            "sw_version": "Device_SW_Version",
            "model": "Device_model",
            "manufacturer": "Weishaupt",
        }


class MySensorEntity(SensorEntity, MyEntity):
    # class that represents a sensor entity derived from Sensorentity
    # and decorated with general parameters from MyEntity
    _attr_native_unit_of_measurement = None
    _attr_device_class = None
    _attr_state_class = None

    def __init__(self, config_entry, modbus_item) -> None:
        MyEntity.__init__(self, config_entry, modbus_item)

    async def async_update(self) -> None:
        # the synching is done by the ModbusObject of the entity
        self._attr_native_value = await self.translateVal

    @property
    def device_info(self) -> DeviceInfo:
        return MyEntity.my_device_info(self)


class MyCalcSensorEntity(MySensorEntity):
    # class that represents a sensor entity derived from Sensorentity
    # and decorated with general parameters from MyEntity
    # calculates output from map
    my_map = PowerMap()

    def __init__(self, config_entry, modbus_item) -> None:
        MySensorEntity.__init__(self, config_entry, modbus_item)

    async def async_update(self) -> None:
        # the synching is done by the ModbusObject of the entity
        self._attr_native_value = await self.translateVal

    def calcPower(self, val, x, y):
        if val == None:
            return val
        return (val / 100) * self.my_map.map(x, y)

    @property
    async def translateVal(self):
        # reads an translates a value from the modbus
        mbo = ModbusObject(self._config_entry, self._modbus_item)
        val = self.calcPercentage(await mbo.value)

        mb_x = ModbusItem(
            self._modbus_item.getNumberFromText("x"),
            "x",
            FORMATS.TEMPERATUR,
            TYPES.SENSOR_CALC,
            DEVICES.SYS,
            TEMPRANGE_STD,
        )
        mbo_x = ModbusObject(self._config_entry, mb_x)
        if mbo_x == None:
            return None
        t_temp = await mbo_x.value
        val_x = self.calcTemperature(t_temp) / 10
        mb_y = ModbusItem(
            self._modbus_item.getNumberFromText("y"),
            "y",
            FORMATS.TEMPERATUR,
            TYPES.SENSOR_CALC,
            DEVICES.WP,
            TEMPRANGE_STD,
        )
        mbo_y = ModbusObject(self._config_entry, mb_y)
        if mbo_y == None:
            return None
        t_temp = await mbo_y.value
        val_y = self.calcTemperature(t_temp) / 10

        match self._modbus_item.format:
            case FORMATS.POWER:
                return self.calcPower(val, val_x, val_y)
            case _:
                return val / self._divider

    @property
    def device_info(self) -> DeviceInfo:
        return MySensorEntity.my_device_info(self)


class MyNumberEntity(NumberEntity, MyEntity):
    # class that represents a sensor entity derived from Sensorentity
    # and decorated with general parameters from MyEntity
    _attr_native_unit_of_measurement = None
    _attr_device_class = None
    _attr_state_class = None
    _attr_native_min_value = 10
    _attr_native_max_value = 60

    def __init__(self, config_entry, modbus_item) -> None:
        MyEntity.__init__(self, config_entry, modbus_item)

        if self._modbus_item.resultlist != None:
            self._attr_native_min_value = self._modbus_item.getNumberFromText("min")
            self._attr_native_max_value = self._modbus_item.getNumberFromText("max")
            self._attr_native_step = self._modbus_item.getNumberFromText("step")

    async def async_set_native_value(self, value: float) -> None:
        await self.settranslateVal(value)
        self._attr_native_value = await self.translateVal
        self.async_write_ha_state()

    async def async_update(self) -> None:
        # the synching is done by the ModbusObject of the entity
        self._attr_native_value = await self.translateVal

    @property
    def device_info(self) -> DeviceInfo:
        return MyEntity.my_device_info(self)


class MySelectEntity(SelectEntity, MyEntity):
    # class that represents a sensor entity derived from Sensorentity
    # and decorated with general parameters from MyEntity
    options = []
    _attr_current_option = "FEHLER"

    def __init__(self, config_entry, modbus_item) -> None:
        MyEntity.__init__(self, config_entry, modbus_item)
        self.async_internal_will_remove_from_hass_port = self._config_entry.data[
            CONF_PORT
        ]
        # option list build from the status list of the ModbusItem
        self.options = []
        for index, item in enumerate(self._modbus_item._resultlist):
            self.options.append(item.text)

    async def async_select_option(self, option: str) -> None:
        # the synching is done by the ModbusObject of the entity
        await self.settranslateVal(option)
        self._attr_current_option = await self.translateVal
        self.async_write_ha_state()

    async def async_update(self) -> None:
        # the synching is done by the ModbusObject of the entity
        # await self.coordinator.async_request_refresh()
        self._attr_current_option = await self.translateVal

    @property
    def device_info(self) -> DeviceInfo:
        return MyEntity.my_device_info(self)
