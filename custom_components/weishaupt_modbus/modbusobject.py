"""Modbusobject.

A Modbus object that contains a Modbus item and communicates with the Modbus.
It contains a ModbusClient for setting and getting Modbus register values
"""

from pymodbus.client import AsyncModbusTcpClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import TYPES
from .items import ModbusItem

# import logging
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)


class ModbusAPI:
    """ModbusAPI class."""

    _ip = None
    _port = None
    _modbus_client = None

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Construct ModbusClient.

        :param config_entry: HASS config entry
        :type config_entry: ConfigEntry
        :param modbus_item: definition of modbus item
        :type modbus_item: ModbusItem
        """
        self._ip = config_entry.data[CONF_HOST]
        self._port = config_entry.data[CONF_PORT]
        self._modbus_client = None

    async def connect(self):
        """Open modbus connection."""
        try:
            self._modbus_client = AsyncModbusTcpClient(
                host=self._ip, port=self._port, name="Weishaupt_WBB"
            )
            await self._modbus_client.connect()

        except:
            return None
        return self._modbus_client.connected

    async def close(self):
        """Close modbus connection."""
        try:
            await self._modbus_client.close()
            # noqa: TRY300
        except:
            return None
        return self._modbus_client.connected

    def get_device(self):
        """Return modbus connection."""
        return self._modbus_client


class ModbusObject:
    """ModbusObject.

    A Modbus object that contains a Modbus item and communicates with the Modbus.
    It contains a ModbusClient for setting and getting Modbus register values
    """

    _modbus_item = None
    _data_format = None

    def __init__(self, modbus_api: ModbusAPI, modbus_item: ModbusItem) -> None:
        """Construct ModbusClient.

        :param config_entry: HASS config entry
        :type config_entry: ConfigEntry
        :param modbus_item: definition of modbus item
        :type modbus_item: ModbusItem
        """

        self._modbus_item = modbus_item
        self._modbus_client = modbus_api.get_device()

    @property
    async def value(self):
        """Returns the value from the modbus register."""
        match self._modbus_item.type:
            case TYPES.SENSOR | TYPES.SENSOR_CALC:
                # Sensor entities are read-only
                return (
                    await self._modbus_client.read_input_registers(
                        self._modbus_item.address, slave=1
                    )
                ).registers[0]
            case TYPES.SELECT | TYPES.NUMBER | TYPES.NUMBER_RO:
                return (
                    await self._modbus_client.read_holding_registers(
                        self._modbus_item.address, slave=1
                    )
                ).registers[0]
            case _:
                return None

    # @value.setter
    async def setvalue(self, value) -> None:
        """Set the value of the modbus register, does nothing when not R/W."""
        try:
            match self._modbus_item.type:
                case TYPES.SENSOR | TYPES.NUMBER_RO | TYPES.SENSOR_CALC:
                    # Sensor entities are read-only
                    return
                case _:
                    await self._modbus_client.write_register(
                        self._modbus_item.address, int(value), slave=1
                    )
        except:
            return None
