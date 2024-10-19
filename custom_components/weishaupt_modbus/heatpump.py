import warnings

from pymodbus.client import ModbusTcpClient as ModbusClient

from homeassistant.const import CONF_HOST, CONF_PORT

from .const import TYPES
from .hpconst import MODBUS_SYS_ITEMS


class HeatPump:
    _ip = None
    _port = None
    _ModbusClient = None

    def __init__(self, config_entry):
        self._ip = config_entry.data[CONF_HOST]
        self._port = config_entry.data[CONF_PORT]
        self._ModbusClient = None

    def connect(self):
        # try:
        self._ModbusClient = ModbusClient(host=self._ip, port=self._port)
        return self._ModbusClient.connected  # noqa: TRY300

    # except:  # noqa: E722
    # return None

    def getValue(self, ModbusItem):
        try:
            if not self._ModbusClient.connected:
                self.connect()
            match ModbusItem.type:
                case TYPES.SENSOR | TYPES.SENSOR_CALC:
                    # Sensor entities are read-only
                    ModbusItem._value = self._ModbusClient.read_input_registers(
                        ModbusItem.address, slave=1
                    ).registers[0]
                case TYPES.SELECT | TYPES.NUMBER | TYPES.NUMBER_RO:
                    ModbusItem._value = self._ModbusClient.read_holding_registers(
                        ModbusItem.address, slave=1
                    ).registers[0]

        except:  # noqa: E722
            warnings.warn("Getting value of " & ModbusItem.name & " failed")
            return None

    def setValue(self, ModbusItem, value) -> None:
        try:
            match ModbusItem.type:
                case TYPES.SENSOR | TYPES.NUMBER_RO | TYPES.SENSOR_CALC:
                    # Sensor entities are read-only
                    return
                case _:
                    self.connect()
                    self._ModbusClient.write_register(
                        ModbusItem.address, int(value), slave=1
                    )
        except:  # noqua: E722
            return None

    def poll(self):
        for item in MODBUS_SYS_ITEMS:
            # warnings.warn(str(item.address))
            self.getValue(item)
            warnings.warn(str(item._value))
