from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT
from pymodbus.client import AsyncModbusTcpClient
from .const import FORMATS, TYPES

# import logging
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)


# A Modbus object that contains a Modbus item and communicates with the Modbus
# it contains a ModbusClient for setting and getting Modbus register values
class ModbusObject:
    _ModbusItem = None
    _DataFormat = None

    _ip = None
    _port = None
    _ModbusClient = None

    def __init__(self, config_entry, modbus_item):
        self._ModbusItem = modbus_item

        self._ip = config_entry.data[CONF_HOST]
        self._port = config_entry.data[CONF_PORT]
        self._ModbusClient = None

    async def connect(self):
        try:
            self._ModbusClient = AsyncModbusTcpClient(host=self._ip, port=self._port)
            await self._ModbusClient.connect()
            return self._ModbusClient.connected  # noqa: TRY300
        except:  # noqa: E722
            return None

    @property
    async def value(self):
        try:
            await self.connect()
            match self._ModbusItem.type:
                case TYPES.SENSOR | TYPES.SENSOR_CALC:
                    # Sensor entities are read-only
                    return (
                        await self._ModbusClient.read_input_registers(
                            self._ModbusItem.address, slave=1
                        )
                    ).registers[0]
                case TYPES.SELECT | TYPES.NUMBER | TYPES.NUMBER_RO:
                    return (
                        await self._ModbusClient.read_holding_registers(
                            self._ModbusItem.address, slave=1
                        )
                    ).registers[0]
        except:  # noqa: E722
            return None

    # @value.setter
    async def setvalue(self, value) -> None:
        try:
            match self._ModbusItem.type:
                case TYPES.SENSOR | TYPES.NUMBER_RO | TYPES.SENSOR_CALC:
                    # Sensor entities are read-only
                    return
                case _:
                    await self.connect()
                    await self._ModbusClient.write_register(
                        self._ModbusItem.address, int(value), slave=1
                    )
        except:  # noqua: E722
            return None
