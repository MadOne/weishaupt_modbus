"""The Update Coordinator for the ModbusItems."""

import logging
import asyncio
import warnings

from pymodbus import ModbusException

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
from homeassistant.config_entries import ConfigEntry

from .const import (
    CONST,
    FORMATS,
    TYPES,
    CONF_HK2,
    CONF_HK3,
    CONF_HK4,
    CONF_HK5,
)
from .hpconst import DEVICES, TEMPRANGE_STD
from .items import ModbusItem
from .modbusobject import ModbusObject, ModbusAPI

logging.basicConfig()
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.WARNING)


class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(
        self,
        hass,
        my_api: ModbusAPI,
        modbusitems: ModbusItem,
        p_config_entry: ConfigEntry,
    ):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="weishaupt-coordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=CONST.SCAN_INTERVAL,
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True,
        )
        self._modbus_api = my_api
        self._device = None  #: MyDevice | None = None
        self._modbusitems = modbusitems
        self._number_of_items = len(modbusitems)
        self._config_entry = p_config_entry

    async def get_value(self, modbus_item: ModbusItem):
        """Read a value from the modbus."""
        mbo = ModbusObject(self._modbus_api, modbus_item)
        if mbo is None:
            modbus_item.state = None
        modbus_item.state = await mbo.value
        return modbus_item.state

    async def get_value_a(self, modbus_item: ModbusItem):
        """Read a value from the modbus."""
        mbo = ModbusObject(self._modbus_api, modbus_item)
        if mbo is None:
            return None
        return await mbo.value

    async def check_configured(self, modbus_item: ModbusItem) -> bool:
        """function checks if item is configured"""
        if self._config_entry.data[CONF_HK2] is False:
            if modbus_item.device is DEVICES.HZ2:
                return False

        if self._config_entry.data[CONF_HK3] is False:
            if modbus_item.device is DEVICES.HZ3:
                return False

        if self._config_entry.data[CONF_HK4] is False:
            if modbus_item.device is DEVICES.HZ4:
                return False

        if self._config_entry.data[CONF_HK5] is False:
            if modbus_item.device is DEVICES.HZ5:
                return False
        return True

    async def _async_setup(self):
        """Set up the coordinator.

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        await self.fetch_data()

    async def fetch_data(self, idx=None):
        """Fetch all values from the modbus."""
        # if idx is not None:
        if idx is None:
            # first run: Update all entitiies
            to_update = tuple(range(len(self._modbusitems)))
        elif len(idx) == 0:
            # idx exists but is not yet filled up: Update all entitiys.
            to_update = tuple(range(len(self._modbusitems)))
        else:
            # idx exists and is filled up: Update only entitys requested by the coordinator.
            to_update = idx

        # await self._modbus_api.connect()
        for index in to_update:
            item = self._modbusitems[index]
            # At setup the coordinator has to be called before buildentitylist. Therefore check if we should add HZ2,3,4,5...
            if await self.check_configured(item) is True:
                match item.type:
                    # here the entities are created with the parameters provided
                    # by the ModbusItem object
                    case TYPES.SENSOR | TYPES.NUMBER_RO | TYPES.NUMBER | TYPES.SELECT:
                        await self.get_value(item)
                    case TYPES.SENSOR_CALC:
                        r1 = await self.get_value_a(item)
                        item_x = ModbusItem(
                            item.get_number_from_text("x"),
                            "x",
                            FORMATS.TEMPERATUR,
                            TYPES.SENSOR_CALC,
                            DEVICES.SYS,
                            TEMPRANGE_STD,
                        )
                        r2 = await self.get_value(item_x)
                        if r2 is None:
                            # use Aussentemperatur if Luftansaugtemperatur not available
                            item_x = ModbusItem(
                                item.get_number_from_text("x2"),
                                "x2",
                                FORMATS.TEMPERATUR,
                                TYPES.SENSOR_CALC,
                                DEVICES.SYS,
                                TEMPRANGE_STD,
                            )
                            r2 = await self.get_value(item_x)
                        item_y = ModbusItem(
                            item.get_number_from_text("y"),
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
        # Note: asyncio.TimeoutError and aiohttp.ClientError are already
        # handled by the data update coordinator.
        async with asyncio.timeout(10):
            # Grab active context variables to limit data required to be fetched from API
            # Note: using context is not required if there is no need or ability to limit
            # data retrieved from API.
            try:
                listening_idx = set(self.async_contexts())
                return await self.fetch_data(listening_idx)
            except ModbusException:
                warnings.warn("connection to the heatpump failed")
