"""Item classes."""

from .const import TYPES, FormatConstants, TypeConstants, DeviceConstants


# An item of a status, e.g. error code and error text along with a precise description
# A class is intentionally defined here because the assignment via dictionaries would not work so elegantly in the end,
# especially when searching backwards. (At least I don't know how...)
class StatusItem:
    """Status item class."""

    _number = None
    _text = None
    _description = None
    _translation_key: str = ""

    def __init__(
        self,
        number: int,
        text: str,
        translation_key: str = None,
        description: str = None,
    ) -> None:
        """Initialise StatusItem."""
        self._number = number
        self._text = text
        self._description = description
        self._translation_key = translation_key

    @property
    def number(self) -> int:
        """Return number."""
        return self._number

    @number.setter
    def number(self, value: int) -> None:
        """Set number."""
        self._number = value

    @property
    def text(self) -> str:
        """Return text."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @property
    def description(self) -> str:
        """Return description."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def translation_key(self) -> str:
        """Return translation_key."""
        return self._translation_key

    @translation_key.setter
    def translation_key(self, val: str) -> None:
        """Set translation_key."""
        self._translation_key = val


class ModbusItem:
    """class Modbus item, consisting of address, name,
    format (temperature, status, ..),
    type (sensor, number, ..),
    device (System, Heatpump, ..) and
    optional result list from status items
    (number entities: status = limits?
    """

    _address = None
    _name = "empty"
    _format = None
    _type = TYPES.SENSOR
    _resultlist = None
    _device = None
    _state = None
    _is_invalid = False
    _translation_key: str = ""

    def __init__(
        self,
        address: int,
        name: str,
        mformat: FormatConstants,
        mtype: TypeConstants,
        device: DeviceConstants,
        translation_key: str = None,
        resultlist=None,
    ) -> None:
        """Initialise ModbusItem."""
        self._address = address
        self._name = name
        self._format = mformat
        self._type = mtype
        self._device = device
        self._resultlist = resultlist
        self._state = None
        self._is_invalid = False
        self._translation_key = translation_key

    @property
    def is_invalid(self) -> bool:
        """Return state."""
        return self._is_invalid

    @is_invalid.setter
    def is_invalid(self, val: bool):
        self._is_invalid = val

    @property
    def address(self) -> int:
        """Return address."""
        return self._address

    @address.setter
    def address(self, val: int):
        """Return address."""
        self._address = val

    @property
    def state(self):
        """Return the state of the item set by modbusobject."""
        return self._state

    @state.setter
    def state(self, val):
        """Set the state of the item from modbus."""
        self._state = val

    @property
    def name(self) -> str:
        """Return name."""
        return self._name

    @name.setter
    def name(self, val: str):
        """Return name."""
        self._name = val

    @property
    def format(self) -> FormatConstants:
        """Return format."""
        return self._format

    @property
    def type(self):
        """Return type."""
        return self._type

    @property
    def device(self) -> DeviceConstants:
        """Return device."""
        return self._device

    @device.setter
    def device(self, val: DeviceConstants):
        """Return device."""
        self._device = val

    @property
    def translation_key(self) -> str:
        """Return translation_key."""
        return self._translation_key

    @translation_key.setter
    def translation_key(self, val: str) -> None:
        """Set translation_key."""
        self._translation_key = val

    @property
    def resultlist(self):
        """Return resultlist."""
        return self._resultlist

    def get_text_from_number(self, val: int) -> str:
        """Get errortext from coresponding number."""
        if val is None:
            return None
        if self._resultlist is None:
            return None
        for _useless, item in enumerate(self._resultlist):
            if val == item.number:
                return item.text
        return "unbekannt <" + str(val) + ">"

    def get_number_from_text(self, val: str) -> int:
        """Get number of coresponding errortext."""
        if self._resultlist is None:
            return None
        for _useless, item in enumerate(self._resultlist):
            if val == item.text:
                return item.number
        return -1

    def get_translation_key_from_number(self, val: int) -> str:
        """Get errortext from coresponding number."""
        if val is None:
            return None
        if self._resultlist is None:
            return None
        for _useless, item in enumerate(self._resultlist):
            if val == item.number:
                return item.translation_key
        return "unbekannt <" + str(val) + ">"

    def get_number_from_translation_key(self, val: str) -> int:
        """Get number of coresponding errortext."""
        if val is None:
            return None
        if self._resultlist is None:
            return None
        for _useless, item in enumerate(self._resultlist):
            if val == item.translation_key:
                return item.number
        return -1
