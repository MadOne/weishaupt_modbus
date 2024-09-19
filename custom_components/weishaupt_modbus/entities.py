from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.components.select import SelectEntity
from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfEnergy, UnitOfTemperature
from homeassistant.helpers.device_registry import DeviceInfo
from .const import CONST, FORMATS, TYPES
from .modbusobject import ModbusObject

def BuildEntityList(entries, host, port, modbusitems, type):
    # this builds a list of entities that can be used as parameter by async_setup_entry()
    # type of list is defined by the ModbusItem's type flag
    # so the app only holds one list of entities that is build from a list of ModbusItem 
    # stored in hpconst.py so far, will be provided by an external file in future
    for index, item in enumerate(modbusitems):
        if item.type == type:
           match type:
                # here the entities are created with the parameters provided by the ModbusItem object
                case TYPES.SENSOR:
                    entries.append(MySensorEntity(host, port, modbusitems[index]))
                case TYPES.SELECT:
                    entries.append(MySelectEntity(host, port, modbusitems[index]))
                case TYPES.NUMBER:
                    entries.append(MyNumberEntity(host, port, modbusitems[index]))

    return entries

class MyEntity():
    # The base class for entities that hold general parameters
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

    def calcTemperature(self,val):
        if val == -32768:
            return -1
        if val == -32767:
            return -2
        return val / 10

    @property
    def translateVal(self):
        # reads an translates a value from the modbua
        mbo = ModbusObject(self._host, self._port, self._modbus_item)
        val = mbo.value
        match self._modbus_item.format:
            case FORMATS.TEMPERATUR:
                return self.calcTemperature(val)
            case FORMATS.STATUS:
                return self._modbus_item.getTextFromNumber(val)
            case _:
                return val

    @translateVal.setter
    def translateVal(self,value):
        # translates and writes a value to the modbus
        mbo = ModbusObject(self._host, self._port, self._modbus_item)
        val = None
        match self._ModbusItem.format:
            # logically, this belongs to the ModbusItem, but doing it here
            # maybe adding a translate function in MyEntity?
            # currently it saves a lot of code lines ;-)
            case FORMATS.TEMPERATUR:
                val = value * 10
            case FORMATS.STATUS:
                val = self._ModbusItem.getNumberFromText(value)
            case _:
                val = value
        mbo.value = val
    
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
    _attr_device_class =  None
    _attr_state_class =  None

    def __init__(self, host, port, modbus_item) -> None:
        MyEntity.__init__(self, host, port, modbus_item)

        # to be cleaed up --> provide this info by the ModbusItem?
        if self._modbus_item._format == FORMATS.TEMPERATUR:
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_state_class = SensorStateClass.MEASUREMENT

        if self._modbus_item._format == FORMATS.PERCENTAGE:
            self._attr_native_unit_of_measurement = "%"


    async def async_update(self) -> None:
        # the synching is done by the ModbusObject of the entity
        self._attr_native_value = translateVal

    @property
    def device_info(self) -> DeviceInfo:
        return MyEntity.my_device_info(self)

class MyNumberEntity(NumberEntity, MyEntity):
    # class that represents a sensor entity derived from Sensorentity 
    # and decorated with general parameters from MyEntity
    _attr_native_unit_of_measurement = None
    _attr_device_class =  None
    _attr_state_class =  None

    def __init__(self, host, port, modbus_item) -> None:
        MyEntity.__init__(self, host, port, modbus_item)

        # to be cleaed up --> provide this info by the ModbusItem?
        if self._modbus_item._format == FORMATS.TEMPERATUR:
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_state_class = SensorStateClass.MEASUREMENT

        if self._modbus_item._format == FORMATS.PERCENTAGE:
            self._attr_native_unit_of_measurement = "%"


    async def async_update(self) -> None:
        # the synching is done by the ModbusObject of the entity
        self._attr_native_value = translateVal

    @property
    def device_info(self) -> DeviceInfo:
        return MyEntity.my_device_info(self)


class MySelectEntity(SelectEntity, MyEntity):
    # class that represents a sensor entity derived from Sensorentity 
    # and decorated with general parameters from MyEntity
    options = []
    _attr_current_option = "FEHLER"

    def __init__(self, host, port, modbus_item) -> None:
        MyEntity.__init__(self, host, port, modbus_item)
        self.async_internal_will_remove_from_hass_port = self._port
        # option list build from the status list of the ModbusItem
        self.options = []
        for index, item in enumerate(self._modbus_item._resultlist):
            self.options.append(item.text)

    async def async_select_option(self, option: str) -> None:
        # the synching is done by the ModbusObject of the entity
        self._attr_current_option = option
        translateVal = option
        self.async_write_ha_state()

    async def async_update(self) -> None:
        # the synching is done by the ModbusObject of the entity
        # await self.coordinator.async_request_refresh()
        self._attr_native_value = translateVal

    @property
    def device_info(self) -> DeviceInfo:
        return MyEntity.my_device_info(self)
