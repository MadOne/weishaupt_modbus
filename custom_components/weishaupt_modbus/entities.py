"""Build entitiy List and Update Coordinator."""

import asyncio
from datetime import timedelta
import logging
import warnings

from pymodbus import ModbusException

from homeassistant.components.number import NumberEntity
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import (
    #    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_PORT
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

# from homeassistant.const import UnitOfEnergy, UnitOfTemperature
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import CONST, FORMATS, TYPES  # , DOMAIN
from .kennfeld import PowerMap
from .modbusobject import ModbusObject

_LOGGER = logging.getLogger(__name__)


def BuildEntityList(entries, config_entry, modbusitems, item_type, coordinator=None):
    """Build the entity list.

    Function builds a list of entities that can be used as parameter by async_setup_entry()
    type of list is defined by the ModbusItem's type flag
    so the app only holds one list of entities that is build from a list of ModbusItem
    stored in hpconst.py so far, will be provided by an external file in future
    """
    for index, item in enumerate(modbusitems):
        if item.type == item_type:
            match item_type:
                # here the entities are created with the parameters provided by the ModbusItem object
                case TYPES.SENSOR | TYPES.NUMBER_RO:
                    entries.append(
                        MySensorEntity(config_entry, modbusitems[index], coordinator)
                    )
                # case TYPES.SENSOR_CALC:
                #    entries.append(MyCalcSensorEntity(config_entry, modbusitems[index]))
                case TYPES.SELECT:
                    entries.append(MySelectEntity(config_entry, modbusitems[index]))
                case TYPES.NUMBER:
                    entries.append(MyNumberEntity(config_entry, modbusitems[index]))

    return entries


class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    data = []

    def __init__(self, hass, my_api, modbusitems):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="weishaupt-coordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=30),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True,
        )
        self._modbus_api = my_api
        self._device = None  #: MyDevice | None = None
        self._modbusitems = modbusitems

    async def _async_setup(self):
        """Set up the coordinator.

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        await self._modbus_api.connect()
        self._device = self._modbus_api.get_device()

    def calcTemperature(self, val: float, modbus_item):
        """Calculate Temperature with values from the heatpump."""
        divider = 1
        if modbus_item.resultlist is not None:
            divider = modbus_item.getNumberFromText("divider")

        if val is None:
            return None
        if val == -32768:
            return -1
        if val == -32767:
            return -2
        if val == 32768:
            return None
        return val / divider

    def calcPercentage(self, val: float, modbus_item):
        """Calculate Percentage with value from heatpump."""
        divider = 1
        if modbus_item.resultlist is not None:
            divider = modbus_item.getNumberFromText("divider")

        if val is None:
            return None
        if val == 65535:
            return None
        return val / divider

    # @property
    async def translateVal(self, modbus_item):
        """Read an translates a value from the modbus."""
        mbo = ModbusObject(self._modbus_api, modbus_item)
        if mbo is None:
            return None
        val = await mbo.value
        match modbus_item.format:
            case FORMATS.TEMPERATUR:
                return self.calcTemperature(val, modbus_item)
            case FORMATS.PERCENTAGE:
                return self.calcPercentage(val, modbus_item)
            case FORMATS.STATUS:
                return modbus_item.getTextFromNumber(val)
            case _:
                if val is None:
                    return val
                return val  # / self._divider

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        # try:
        # Note: asyncio.TimeoutError and aiohttp.ClientError are already
        # handled by the data update coordinator.
        async with asyncio.timeout(10):
            # Grab active context variables to limit data required to be fetched from API
            # Note: using context is not required if there is no need or ability to limit
            # data retrieved from API.
            # listening_idx = set(self.async_contexts())
            # return await self._modbus_api.fetch_data(listening_idx)
            try:
                await self._modbus_api.connect()
            except ModbusException:
                warnings.warn("connection to the heatpump failed")

            for index, item in enumerate(self._modbusitems):
                try:
                    match item.type:
                        # here the entities are created with the parameters provided by the ModbusItem object
                        case TYPES.SENSOR | TYPES.NUMBER_RO:
                            item.state = await self.translateVal(item)
                except:
                    warnings.warn("Item:" + str(item.name + " failed"))

            try:
                await self._modbus_api.close()
            except ModbusException:
                warnings.warn("Closing connection to heatpump failed")
        # except:  # noqa: E722 # ApiAuthError as err:
        #    return None
        # Raising ConfigEntryAuthFailed will cancel future updates
        # and start a config flow with SOURCE_REAUTH (async_step_reauth)
        # raise ConfigEntryAuthFailed from err
        # except ApiError as err:
        #    raise UpdateFailed(f"Error communicating with API: {err}")


class MyEntity:
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
    _attr_name = ""
    _attr_unique_id = ""
    _attr_should_poll = True
    _dev_device = ""

    def __init__(self, config_entry, modbus_item) -> None:
        """Initialize the entity."""
        self._config_entry = config_entry
        self._modbus_item = modbus_item
        self._attr_name = self._modbus_item.name
        self._attr_unique_id = CONST.PREFIX + self._modbus_item.name
        self._dev_device = self._modbus_item.device

        if self._modbus_item._format != FORMATS.STATUS:
            self._attr_native_unit_of_measurement = self._modbus_item._format

            if self._modbus_item._format == FORMATS.ENERGY:
                self._attr_state_class = SensorStateClass.TOTAL_INCREASING
            if self._modbus_item._format == FORMATS.TEMPERATUR:
                self._attr_state_class = SensorStateClass.MEASUREMENT
            if self._modbus_item._format == FORMATS.POWER:
                self._attr_state_class = SensorStateClass.MEASUREMENT

            if self._modbus_item.resultlist is not None:
                self._attr_native_min_value = self._modbus_item.getNumberFromText("min")
                self._attr_native_max_value = self._modbus_item.getNumberFromText("max")
                self._attr_native_step = self._modbus_item.getNumberFromText("step")
                self._divider = self._modbus_item.getNumberFromText("divider")
                self._attr_device_class = self._modbus_item.getTextFromNumber(-1)

    def calcTemperature(self, val: float):
        """Calcualte temperature."""
        if val is None:
            return None
        if val == -32768:
            return -1
        if val == -32767:
            return -2
        if val == 32768:
            return None
        return val / self._divider

    def calcPercentage(self, val: float):
        """Calculate percentage."""
        if val is None:
            return None
        if val == 65535:
            return None
        return val / self._divider

    @property
    async def translateVal(self):
        """Read an translate a value from the modbus."""
        #        mbo = ModbusObject(self._config_entry, self._modbus_item)
        mbo = None

        if mbo is None:
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
                if val is None:
                    return val
                return val / self._divider

    # @translateVal.setter
    async def settranslateVal(self, value):
        """Translate and write a value to the modbus."""
        #        mbo = ModbusObject(self._config_entry, self._modbus_item)
        mbo = None

        if mbo is None:
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
        """Build the device info with this helper."""
        return {
            "identifiers": {(CONST.DOMAIN, self._dev_device)},
            "name": self._dev_device,
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

    def __init__(self, config_entry, modbus_item, coordinator=None, idx=None) -> None:
        """Initialize sensor entitiy."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, modbus_item)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self._modbus_item.state
        self.async_write_ha_state()

    # async def async_update(self) -> None:
    #    # the synching is done by the ModbusObject of the entity
    #    self._attr_native_value = await self.translateVal

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)


class MyCalcSensorEntity(MySensorEntity):
    """class that represents a sensor entity.

    Derived from Sensorentity
    and decorated with general parameters from MyEntity
    calculates output from map
    """

    my_map = PowerMap()

    def __init__(self, config_entry, modbus_item) -> None:
        """Initialize Sensor Entity."""
        MySensorEntity.__init__(self, config_entry, modbus_item)

    async def async_update(self) -> None:
        """Sync by the ModbusObject of the entity."""
        self._attr_native_value = await self.translateVal

    def calcPower(self, val, x, y):
        """Calculate power."""
        if val is None:
            return val
        return (val / 100) * self.my_map.map(x, y)

    @property
    async def translateVal(self):
        """Not sure."""
        # reads an translates a value from the modbus
        #        mbo = ModbusObject(self._config_entry, self._modbus_item)
        #        val = self.calcPercentage(await mbo.value)

        #        mb_x = ModbusItem(
        #            self._modbus_item.getNumberFromText("x"),
        #            "x",
        #            FORMATS.TEMPERATUR,
        #            TYPES.SENSOR_CALC,
        #            DEVICES.SYS,
        #            TEMPRANGE_STD,
        #        )
        #        mbo_x = ModbusObject(self._config_entry, mb_x)
        #        if mbo_x is None:
        #            return None
        #        t_temp = await mbo_x.value
        #        val_x = self.calcTemperature(t_temp) / 10
        #        mb_y = ModbusItem(
        #            self._modbus_item.getNumberFromText("y"),
        #            "y",
        #            FORMATS.TEMPERATUR,
        #            TYPES.SENSOR_CALC,
        #            DEVICES.WP,
        #            TEMPRANGE_STD,
        #        )
        #        mbo_y = ModbusObject(self._config_entry, mb_y)
        #        if mbo_y is None:
        #            return None
        #        t_temp = await mbo_y.value
        #        val_y = self.calcTemperature(t_temp) / 10
        return None

    #        match self._modbus_item.format:
    #            case FORMATS.POWER:
    #                return self.calcPower(val, val_x, val_y)
    #            case _:
    #                return val / self._divider

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MySensorEntity.my_device_info(self)


class MyNumberEntity(NumberEntity, MyEntity):
    """Class that represents a sensor entity.

    derived from Sensorentity
    and decorated with general parameters from MyEntity
    """

    _attr_native_unit_of_measurement = None
    _attr_device_class = None
    _attr_state_class = None
    _attr_native_min_value = 10
    _attr_native_max_value = 60

    def __init__(self, config_entry, modbus_item) -> None:
        """Initialize the number entity."""
        MyEntity.__init__(self, config_entry, modbus_item)

        if self._modbus_item.resultlist is not None:
            self._attr_native_min_value = self._modbus_item.getNumberFromText("min")
            self._attr_native_max_value = self._modbus_item.getNumberFromText("max")
            self._attr_native_step = self._modbus_item.getNumberFromText("step")

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        await self.settranslateVal(value)
        self._attr_native_value = await self.translateVal
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Sync by the ModbusObject of the entity."""
        self._attr_native_value = await self.translateVal

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)


class MySelectEntity(SelectEntity, MyEntity):
    """class that represents a select entity.

    Derived from SelectEntity
    and decorated with general parameters from MyEntity
    """

    options = []
    _attr_current_option = "FEHLER"

    def __init__(self, config_entry, modbus_item) -> None:
        """Initialize select entity."""
        MyEntity.__init__(self, config_entry, modbus_item)
        self.async_internal_will_remove_from_hass_port = self._config_entry.data[
            CONF_PORT
        ]
        # option list build from the status list of the ModbusItem
        self.options = []
        for index, item in enumerate(self._modbus_item._resultlist):
            self.options.append(item.text)

    async def async_select_option(self, option: str) -> None:
        """Sync is done by the ModbusObject of the entity."""
        await self.settranslateVal(option)
        self._attr_current_option = await self.translateVal
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Sync is done by the ModbusObject of the entity."""
        # await self.coordinator.async_request_refresh()
        self._attr_current_option = await self.translateVal

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)
