"""Modbusobject.

A Modbus object that contains a Modbus item and communicates with the Modbus.
It contains a ModbusClient for setting and getting Modbus register values
"""
# import warnings

import asyncio
import logging
import warnings

from pymodbus import ExceptionResponse, ModbusException
from pymodbus.client import AsyncModbusTcpClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import TYPES, FORMATS
from .items import ModbusItem

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
            for i in range(3):
                await self._modbus_client.connect()
                if self._modbus_client.connected:
                    return self._modbus_client.connected
                else:
                    await asyncio.sleep(1)
            warnings.warn("Connection to heatpump succeeded")

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
        warnings.warn("Connection to heatpump closed")
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

    def check_valid(self, val):
        match self._modbus_item.format:
            case FORMATS.TEMPERATUR:
                self.check_temperature(val)
                return
            case FORMATS.PERCENTAGE:
                self.check_percentage(val)
                return
            case FORMATS.STATUS:
                self.check_status(val)
                return
            case _:
                self._modbus_item.is_invalid = False

    def check_temperature(self, val):
        match val:
            case -32768:
                # No Sensor installed, remove it from the list
                self._modbus_item.is_invalid = True
            case 32768:
                # Dont know. Whats this?
                # print("Sensor not installed: " + self._modbus_item.name)
                self._modbus_item.is_invalid = True
            case _:
                # print("Sensor OK " + self._modbus_item.name + " " + str(val))
                self._modbus_item.is_invalid = False

    def check_percentage(self, val):
        if val == 65535:
            self._modbus_item.is_invalid = True
        self._modbus_item.is_invalid = False

    def check_status(self, val):
        self._modbus_item.is_invalid = False

    @property
    async def value(self):
        """Returns the value from the modbus register."""
        if self._modbus_client is None:
            return None

        val = None
        if not self._modbus_item.is_invalid:
            try:
                match self._modbus_item.type:
                    case TYPES.SENSOR | TYPES.SENSOR_CALC:
                        # Sensor entities are read-only

                        mbr = await self._modbus_client.read_input_registers(
                            self._modbus_item.address, slave=1
                        )
                        if len(mbr.registers) > 0:
                            self.check_valid(val)
                            val = mbr.registers[0]
                    case TYPES.SELECT | TYPES.NUMBER | TYPES.NUMBER_RO:
                        mbr = await self._modbus_client.read_holding_registers(
                            self._modbus_item.address, slave=1
                        )
                        if len(mbr.registers) > 0:
                            self.check_valid(val)
                            val = mbr.registers[0]
                    case _:
                        val = None
                        warnings.warn(
                            "Unknown Sensor type: "
                            + str(self._modbus_item.type)
                            + "in "
                            + str(self._modbus_item.name)
                        )
            except ModbusException as exc:
                warnings.warn(
                    "Received ModbusException: "
                    + exc
                    + "in item: "
                    + self._modbus_item.name
                )
                return None
            if mbr.isError():
                myexception_code: ExceptionResponse = mbr
                if myexception_code.exception_code == 2:
                    self._modbus_item.is_invalid = True
                else:
                    warnings.warn(
                        "Received Modbus library error: "
                        + str(mbr)
                        + "in item: "
                        + self._modbus_item.name
                    )
                return None
            if isinstance(mbr, ExceptionResponse):
                warnings.warn(
                    "Received ModbusException: "
                    + str(mbr)
                    + " from library in item: "
                    + self._modbus_item.name
                )
                return None
                # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message

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
