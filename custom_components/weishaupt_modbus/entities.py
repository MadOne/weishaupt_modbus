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
from .hpconst import DEVICES, TEMPRANGE_STD
from .items import ModbusItem
from .kennfeld import PowerMap
from .modbusobject import ModbusObject

logging.basicConfig()
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.WARNING)


async def check_available(modbus_item, config_entry) -> bool:
    _modbus_api = config_entry.runtime_data
    mbo = ModbusObject(_modbus_api, modbus_item)
    _useless = await mbo.value
    if modbus_item.is_invalid is False:
        return True
    return False


async def BuildEntityList(entries, config_entry, modbusitems, item_type, coordinator):
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
                    # here the entities are created with the parameters provided by the ModbusItem object
                    case TYPES.SENSOR | TYPES.NUMBER_RO:
                        entries.append(
                            MySensorEntity(
                                config_entry, modbusitems[index], coordinator, index
                            )
                        )
                    case TYPES.SENSOR_CALC:
                        entries.append(
                            MyCalcSensorEntity(
                                config_entry, modbusitems[index], coordinator, index
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


class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

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
        self._number_of_items = len(modbusitems)

    async def get_value(self, modbus_item):
        """Read a value from the modbus."""
        mbo = ModbusObject(self._modbus_api, modbus_item)
        if mbo is None:
            modbus_item.state = None
        modbus_item.state = await mbo.value
        return modbus_item.state

    async def get_value_a(self, modbus_item):
        """Read a value from the modbus."""
        mbo = ModbusObject(self._modbus_api, modbus_item)
        if mbo is None:
            return None
        return await mbo.value

    async def _async_setup(self):
        """Set up the coordinator.

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        # await self._modbus_api.connect()
        #    self._device = self._modbus_api.get_device()
        await self.fetch_data()

    async def fetch_data(self, idx=None):
        """Fetch all values from the modbus."""
        # if idx is not None:
        if idx is None:
            # first run: Update all entitiys
            toUpdate = tuple(range(len(self._modbusitems)))
        elif len(idx) == 0:
            # idx exists but is not yet filled up: Update all entitiys.
            toUpdate = tuple(range(len(self._modbusitems)))
        else:
            # idx exists and is filled up: Update only entitys requested by the coordinator.
            toUpdate = idx

        # await self._modbus_api.connect()
        for index in toUpdate:
            item = self._modbusitems[index]
            match item.type:
                # here the entities are created with the parameters provided by the ModbusItem object
                case TYPES.SENSOR | TYPES.NUMBER_RO | TYPES.NUMBER | TYPES.SELECT:
                    await self.get_value(item)
                case TYPES.SENSOR_CALC:
                    r1 = await self.get_value_a(item)
                    item_x = ModbusItem(
                        item.getNumberFromText("x"),
                        "x",
                        FORMATS.TEMPERATUR,
                        TYPES.SENSOR_CALC,
                        DEVICES.SYS,
                        TEMPRANGE_STD,
                    )
                    r2 = await self.get_value(item_x)
                    item_y = ModbusItem(
                        item.getNumberFromText("y"),
                        "y",
                        FORMATS.TEMPERATUR,
                        TYPES.SENSOR_CALC,
                        DEVICES.WP,
                        TEMPRANGE_STD,
                    )
                    r3 = await self.get_value(item_y)

                    item.state = [r1, r2, r3]

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
                listening_idx = set(self.async_contexts())
                return await self.fetch_data(listening_idx)
            except ModbusException:
                warnings.warn("connection to the heatpump failed")

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
    _modbus_api = None

    def __init__(self, config_entry, modbus_item, modbus_api) -> None:
        """Initialize the entity."""
        self._config_entry = config_entry
        self._modbus_item = modbus_item
        self._attr_name = self._modbus_item.name
        self._attr_unique_id = CONST.PREFIX + self._modbus_item.name
        self._dev_device = self._modbus_item.device
        self._modbus_api = modbus_api

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

    def calc_temperature(self, val: float):
        """Calcualte temperature."""

        # match val:
        #    case None:
        #        return None
        #    case -32768:
        #        # No Sensor installed
        #        return -1
        #    case -32767:
        #        # Sensor broken
        #        return -2
        #    case 32768:
        #        # Dont know. Whats this?
        #        return None
        #    case range(-500, 5000):
        #        # Valid Temperatur range
        #        return int(val) / self._divider
        #    case _:
        #        return None
        # print(str(val))
        if val is None:
            return None
        if val == 32768:
            # No Sensor installed
            self._modbus_item.is_invalid = True
            # print(self._modbus_item.name + "Sensor not installed")
            return -1
        if val == 32767:
            # Sensor broken
            self._modbus_item.is_invalid = True
            # print(self._modbus_item.name + "Sensor broken")

        if val == 32768:
            # Dont know. Whats this?
            return None
        if val in range(-500, 5000):
            return int(val) / self._divider

    def calc_percentage(self, val: float):
        """Calculate percentage."""
        if val is None:
            return None
        if val == 65535:
            return None
        return int(val) / self._divider

    def translate_val(self, val):
        """Translate modbus value into sensful format."""
        if val is None:
            return val
        match self._modbus_item.format:
            case FORMATS.TEMPERATUR:
                return self.calc_temperature(val)
            case FORMATS.PERCENTAGE:
                return self.calc_percentage(val)
            case FORMATS.STATUS:
                return self._modbus_item.getTextFromNumber(val)
            case _:
                return int(val) / self._divider

    def retranslate_val(self, value):
        """Re-translate modbus value into sensful format."""
        val = None
        match self._modbus_item.format:
            # logically, this belongs to the ModbusItem, but doing it here
            case FORMATS.STATUS:
                val = self._modbus_item.getNumberFromText(value)
            case _:
                val = value * self._divider
        return val

    async def set_translate_val(self, value):
        """Translate and writes a value to the modbus."""
        val = self.retranslate_val(value)

        await self._modbus_api.connect()
        mbo = ModbusObject(self._modbus_api, self._modbus_item)
        await mbo.setvalue(val)
        # self._modbus_api.close()

    def my_device_info(self) -> DeviceInfo:
        """Build the device info."""
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
        super().__init__(coordinator, context=idx)
        self.idx = idx
        MyEntity.__init__(self, config_entry, modbus_item, coordinator._modbus_api)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.translate_val(self._modbus_item.state)
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
    """

    # calculates output from map
    my_map = PowerMap()

    def __init__(self, config_entry, modbus_item, coordinator, idx) -> None:
        MySensorEntity.__init__(self, config_entry, modbus_item, coordinator, idx)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.translate_val(self._modbus_item.state)
        self.async_write_ha_state()

    # async def async_update(self) -> None:
    #    # the synching is done by the ModbusObject of the entity
    #    self._attr_native_value = self.translate_val(0)

    def calc_power(self, val, x, y):
        """Calculate heating power from power map."""
        if val is None:
            return val
        return (val / 100) * self.my_map.map(x, y)

    def translate_val(self, val):
        """Translate a value from the modbus."""
        if val is None:
            return None
        val_0 = self.calc_percentage(val[0])
        val_x = self.calc_temperature(val[1]) / 10
        val_y = self.calc_temperature(val[2]) / 10

        match self._modbus_item.format:
            case FORMATS.POWER:
                return self.calc_power(val_0, val_x, val_y)
            case _:
                if val_0 is None:
                    return None
                return val_0 / self._divider

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

    def __init__(self, config_entry, modbus_item, coordinator=None, idx=None) -> None:
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, modbus_item, coordinator._modbus_api)

        if self._modbus_item.resultlist is not None:
            self._attr_native_min_value = self._modbus_item.getNumberFromText("min")
            self._attr_native_max_value = self._modbus_item.getNumberFromText("max")
            self._attr_native_step = self._modbus_item.getNumberFromText("step")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.translate_val(self._modbus_item.state)
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        await self.set_translate_val(value)
        # await self.coordinator.async_request_refresh()
        self._modbus_item.state = int(self.retranslate_val(value))
        self._attr_native_value = self.translate_val(self._modbus_item.state)
        self.async_write_ha_state()

    # async def async_update(self) -> None:
    #    # the synching is done by the ModbusObject of the entity
    #    self._attr_native_value = self.translate_val(self._modbus_item.state)

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

    def __init__(self, config_entry, modbus_item, coordinator, idx=None) -> None:
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, modbus_item, coordinator._modbus_api)
        self.async_internal_will_remove_from_hass_port = self._config_entry.data[
            CONF_PORT
        ]
        # option list build from the status list of the ModbusItem
        self.options = []
        for index, item in enumerate(self._modbus_item._resultlist):
            self.options.append(item.text)

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

    # async def async_update(self) -> None:
    #    # the synching is done by the ModbusObject of the entity
    #    await self.coordinator.async_request_refresh()
    #    self._attr_current_option = self.translate_val(self._modbus_item.state)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)
