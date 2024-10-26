"""Modbusobject.

A Modbus object that contains a Modbus item and communicates with the Modbus.
It contains a ModbusClient for setting and getting Modbus register values
"""
# import warnings

import warnings

from pymodbus import ModbusException, ExceptionResponse
from pymodbus.client import AsyncModbusTcpClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import TYPES
from .items import ModbusItem

import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.WARNING)


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
            # warnings.warn("Connection to heatpump succeeded")

        except ModbusException:
            warnings.warn("Connection to heatpump failed")
            return None
        return self._modbus_client.connected

    def close(self):
        """Close modbus connection."""
        try:
            # await self._modbus_client.close()
            self._modbus_client.close()
        except ModbusException:
            warnings.warn("Closing connection to heatpump failed")
            return False
        return True

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
        # await self._modbus_client.connect()

    @property
    async def value(self):
        """Returns the value from the modbus register."""
        if self._modbus_client is None:
            return None
        if not self._modbus_client.connected:
            mbr = await self._modbus_client.connect()
            warnings.warn(
                "Reconnect failed"
                + self._modbus_client.comm_params.host
                + ":"
                + str(self._modbus_client.comm_params.port)
            )

        val = None
        if self._modbus_item._is_invalid:
            warnings.warn(
                "Item " + self._modbus_item.name + " skipped because of invalid address"
            )
        else:
            match self._modbus_item.type:
                case TYPES.SENSOR | TYPES.SENSOR_CALC:
                    # Sensor entities are read-only
                    try:
                        mbr = await self._modbus_client.read_input_registers(
                            self._modbus_item.address, slave=1
                        )
                        if len(mbr.registers) > 0:
                            val = mbr.registers[0]
                    except ModbusException as exc:
                        print(
                            f"Received ModbusException({exc}) from library in {{{self._modbus_item.name}}}"
                        )
                        # exception: ModbusException = exc
                        # if exception.string == "([Connection] Client is not connected)":
                        #    self._modbus_item._is_invalid = True
                        # print(
                        #    "Flagged "
                        #    + self._modbus_item.name
                        #    + " as invalid (Connection) but connected is:"
                        #    + str(self._modbus_client.connected)
                        # )
                        return None
                    if mbr.isError():
                        print(f"Received Modbus library error({mbr})")
                        myexception_code: ExceptionResponse = mbr
                        print(myexception_code.exception_code)
                        if mbr.exception_code == 2:
                            self._modbus_item._is_invalid = True

                            # print(myexception_code.
                            print(
                                "Flagged "
                                + self._modbus_item.name
                                + " as invalid(IllegalAddress)"
                            )
                        return None
                    if isinstance(mbr, ExceptionResponse):
                        print(f"Received Modbus library exception ({mbr})")
                        return None
                        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message

                case TYPES.SELECT | TYPES.NUMBER | TYPES.NUMBER_RO:
                    try:
                        mbr = await self._modbus_client.read_holding_registers(
                            self._modbus_item.address, slave=1
                        )
                        if len(mbr.registers) > 0:
                            val = mbr.registers[0]
                    except ModbusException as exc:
                        print(
                            f"Received ModbusException({exc}) from library in {{{self._modbus_item.name}}}"
                        )
                        exception: ModbusException = exc
                        if exception.string == "([Connection] Client is not connected)":
                            self._modbus_item._is_invalid = True
                        print(
                            "Flagged "
                            + self._modbus_item.name
                            + " as invalid (Connection)"
                        )
                        return None
                    if mbr.isError():
                        print(f"Received Modbus library error({mbr})")
                        myexception_code: ExceptionResponse = mbr
                        print(myexception_code.exception_code)
                        if mbr.exception_code == 2:
                            self._modbus_item._is_invalid = True

                            # print(myexception_code.
                            print(
                                "Flagged "
                                + self._modbus_item.name
                                + " as invalid(IllegalAddress)"
                            )
                        return None
                    if isinstance(mbr, ExceptionResponse):
                        print(f"Received Modbus library exception ({mbr})")
                        return None
                        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
                case _:
                    val = None
        return val

    # @value.setter
    async def setvalue(self, value) -> None:
        """Set the value of the modbus register, does nothing when not R/W."""
        if self._modbus_client is None:
            return None
        try:
            match self._modbus_item.type:
                case TYPES.SENSOR | TYPES.NUMBER_RO | TYPES.SENSOR_CALC:
                    # Sensor entities are read-only
                    return
                case _:
                    await self._modbus_client.write_register(
                        self._modbus_item.address, int(value), slave=1
                    )
        except ModbusException:
            warnings.warn(
                "Writing "
                + str(value)
                + " to "
                + str(self._modbus_item.name)
                + " ("
                + str(self._modbus_item.address + ")" + " failed")
            )
            return None
