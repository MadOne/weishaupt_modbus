from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.components.select import SelectEntity
from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfEnergy, UnitOfTemperature
from homeassistant.helpers.device_registry import DeviceInfo
from .const import CONST, FORMATS, TYPES
from .modbusobject import ModbusObject

def BuildEntityList(entries, host, port, modbusitems, type):
    for index, item in enumerate(modbusitems):
        if item.type == type:
           match type:
                case TYPES.SENSOR:
                    entries.append(MySensorEntity(host, port, modbusitems[index]))
                case TYPES.SELECT:
                    entries.append(MySelectEntity(host, port, modbusitems[index]))
                case TYPES.NUMBER:
                    entries.append(MyNumberEntity(host, port, modbusitems[index]))

    return entries

class MyEntity():
    _host = None
    _port = None
    _modbus_item = None
    _attr_name = ""
    _attr_unique_id = ""
    _attr_should_poll = True
    _dev_device = ""

    def __init__(self, host, port, modbus_item) -> None:
        self._host = host
        self._port = port
        self._modbus_item = modbus_item
        self._attr_name = self._modbus_item.name
        self._attr_unique_id = CONST.DOMAIN + self._attr_name
        self._dev_device = self._modbus_item.device

    def my_device_info(self) -> DeviceInfo:
        return {
                "identifiers": {(CONST.DOMAIN, self._dev_device)},
                "name": self._dev_device,
                "sw_version": "Device_SW_Version",
                "model": "Device_model",
                "manufacturer": "Weishaupt",
        }

class MySensorEntity(SensorEntity, MyEntity):
    _attr_native_unit_of_measurement = None
    _attr_device_class =  None
    _attr_state_class =  None

    def __init__(self, host, port, modbus_item) -> None:
        MyEntity.__init__(self, host, port, modbus_item)

        if self._modbus_item._format == FORMATS.TEMPERATUR:
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_state_class = SensorStateClass.MEASUREMENT

        if self._modbus_item._format == FORMATS.PERCENTAGE:
            self._attr_native_unit_of_measurement = "%"


    async def async_update(self) -> None:
        mbo = ModbusObject(self._host, self._port, self._modbus_item)
        self._attr_native_value = mbo.value

    @property
    def device_info(self) -> DeviceInfo:
        return MyEntity.my_device_info(self)

class MyNumberEntity(NumberEntity, MyEntity):
    _attr_native_unit_of_measurement = None
    _attr_device_class =  None
    _attr_state_class =  None

    def __init__(self, host, port, modbus_item) -> None:
        MyEntity.__init__(self, host, port, modbus_item)

        if self._modbus_item._format == FORMATS.TEMPERATUR:
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_state_class = SensorStateClass.MEASUREMENT

        if self._modbus_item._format == FORMATS.PERCENTAGE:
            self._attr_native_unit_of_measurement = "%"


    async def async_update(self) -> None:
        mbo = ModbusObject(self._host, self._port, self._modbus_item)
        self._attr_native_value = mbo.value

    @property
    def device_info(self) -> DeviceInfo:
        return MyEntity.my_device_info(self)


class MySelectEntity(SelectEntity, MyEntity):
    options = []
    _attr_current_option = "FEHLER"

    def __init__(self, host, port, modbus_item) -> None:
        MyEntity.__init__(self, host, port, modbus_item)
        self.async_internal_will_remove_from_hass_port = self._port
        self.options = []
        for index, item in enumerate(self._modbus_item._resultlist):
            self.options.append(item.text)

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        mbo = ModbusObject(self._host, self._port, self._modbus_item)
        mbo.value = option
        self.async_write_ha_state()

    async def async_update(self) -> None:
        # await self.coordinator.async_request_refresh()
        mbo = ModbusObject(self._host, self._port, self._modbus_item)
        self._attr_current_option = mbo.value

    @property
    def device_info(self) -> DeviceInfo:
        return MyEntity.my_device_info(self)
