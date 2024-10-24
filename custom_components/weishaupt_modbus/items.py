"""Item classes."""

from .const import TYPES


# An item of a status, e.g. error code and error text along with a precise description
# A class is intentionally defined here because the assignment via dictionaries would not work so elegantly in the end,
# especially when searching backwards. (At least I don't know how...)
class StatusItem:
    """Status item class."""

    _number = None
    _text = None
    _description = None

    def __init__(self, number, text, description=None) -> None:
        """Initialise StatusItem."""
        self._number = number
        self._text = text
        self._description = description

    @property
    def number(self):
        """Return number."""
        return self._number

    @number.setter
    def number(self, value) -> None:
        """Set number."""
        self._number = value

    @property
    def text(self):
        """Return text."""
        return self._text

    @text.setter
    def text(self, value) -> None:
        self._text = value

    @property
    def description(self):
        """Return description."""
        return self._description

    @description.setter
    def description(self, value) -> None:
        self._description = value


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
    _state = None

    def __init__(self, address, name, mformat, mtype, device, resultlist=None) -> None:
        """Initialise ModbusItem."""
        self._address = address
        self._name = name
        self._format = mformat
        self._type = mtype
        self._device = device
        self._resultlist = resultlist
        self._state = None

    @property
    def address(self):
        """Return address."""
        return self._address

    @property
    def state(self):
        """Return state."""
        return self._state

    @state.setter
    def state(self, val):
        self._state = val

    @property
    def name(self):
        """Return name."""
        return self._name

    @property
    def format(self):
        """Return format."""
        return self._format

    @property
    def type(self):
        """Return type."""
        return self._type

    @property
    def device(self):
        """Return device."""
        return self._device

    @property
    def resultlist(self):
        """Return resultlist."""
        return self._resultlist

    def getTextFromNumber(self, val):
        """Get errortext from corespnding number."""
        if self._resultlist is None:
            return None
        for index, item in enumerate(self._resultlist):
            if val == item.number:
                return item.text
        return "unbekannt <" + str(val) + ">"

    def getNumberFromText(self, val):
        """Get number of coresponding errortext."""
        if self._resultlist is None:
            return None
        for index, item in enumerate(self._resultlist):
            if val == item.text:
                return item.number
        return -1
