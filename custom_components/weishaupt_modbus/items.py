from .const import TYPES

# An item of a status, e.g. error code and error text along with a precise description
# A class is intentionally defined here because the assignment via dictionaries would not work so elegantly in the end, 
# especially when searching backwards. (At least I don't know how...)
class StatusItem():
    _number = -1
    _text = ""
    _description = ""

    def __init__(self, number, text, description = None):
        self._number = number
        self._text = text
        self._description = description

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value) -> None:
        self._number = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value) -> None:
        self._text = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value) -> None:
        self._description = value

# A Modbus item, consisting of address, name, 
#                              format (temperature, status, ..),
#                              type (sensor, number, ..),
#                              device (System, Heatpump, ..) and
#                              optional result list from status items
#                              (number entities: status = limits?
class ModbusItem():
    _address = None
    _name = "empty"
    _format = None
    _type = TYPES.SENSOR
    _resultlist = None
    _device = None

    def __init__(self, address, name, format, type, device, resultlist = None):
        self._address = address
        self._name = name
        self._format = format
        self._type = type
        self._device = device
        self._resultlist = resultlist
        
    @property
    def address(self):
        return self._address
    @property
    def name(self):
        return self._name

    @property
    def format(self):
        return self._format

    @property
    def type(self):
        return self._type

    @property
    def device(self):
        return self._device

    @property
    def resultlist(self):
        return self._resultlist

    def getTextFromNumber(self, val):
        if self._resultlist == None:
            return None
        for index, item in enumerate(self._resultlist):
            if val == item.number:
                return item.text
        return "unbekannt <" + str(val) + ">"

    def getNumberFromText(self, val):
        if self._resultlist == None:
            return None
        for index, item in enumerate(self._resultlist):
            if val == item.text:
                return item.number
        return -1
