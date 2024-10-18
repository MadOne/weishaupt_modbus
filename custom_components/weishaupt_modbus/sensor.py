"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, UnitOfEnergy, UnitOfTemperature
from homeassistant.core import HomeAssistant

# from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

# from time import gmtime, strftime
from . import wp
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    # config: ConfigType,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    myWp = wp.heat_pump(host, port)
    myWp.connect()
    myList = [
        Sys_Aussentemperatur1(host, port),
        Sys_Aussentemperatur2(host, port),
        Sys_Fehler(host, port),
        Sys_Warnung(host, port),
        Sys_Fehlerfrei(host, port),
        Sys_Betriebsanzeige(host, port),
        HK_RaumSollTemperatur(host, port),
        # HK_RaumTemperatur(host, port),
        # HK_RaumFeuchte(host, port),
        HK_VorlaufSollTemperatur(host, port),
        # HK_VorlaufTemperatur(host, port),
        sensor_measured_temp(host, port),
        sensor_target_temp(host, port),
        Energy_today(host, port),
        Energy_yesterday(host, port),
        Energy_month(host, port),
        Energy_year(host, port),
        HP_Betrieb(host, port),
        HP_Stoermeldung(host, port),
        HP_Leistungsanforderung(host, port),
        Hp_Vorlauftemperatur(host, port),
        Hp_Ruecklauftemperatur(host, port),
        WW_Konfiguration(host, port),
        # EnergySensor(myWp, "testname", "testdevice", myWp.Energy_total_year),
        # EnergySensor(myWp, "testname2", "testdevice2", myWp.Energy_total_year),
    ]
    if myWp.HK_Raumfeuchte is not None:
        myList.append(HK_RaumFeuchte(host, port))
    if myWp.HK_Raumtemperatur is not None:
        myList.append(HK_RaumTemperatur(host, port))
    if myWp.HK_Vorlauftemperatur is not None:
        myList.append(HK_VorlaufTemperatur(host, port))

    async_add_entities(
        myList,
        update_before_add=True,
    )


#####################
#   System          #
#####################
class Sys_Aussentemperatur1(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Aussentemperatur1"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        # whp = wp.heat_pump(self._host, self._port)
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Sys_Aussentemperatur1

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "System")},
            "name": "Wärmepumpe-System",
            # "sw_version": "Device_SW_Version",
            # "model": "Device_model",
            "manufacturer": "Weishaupt",
        }


class Sys_Aussentemperatur2(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Aussentemperatur2"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Sys_Aussentemperatur2

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "System")},
        }


class Sys_Fehler(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Fehler"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Sys_Fehler

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "System")},
        }


class Sys_Warnung(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    _attr_name = "Warnung"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        #
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Sys_Warnung

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "System")},
        }


class Sys_Fehlerfrei(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Fehlerfrei"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        #
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Sys_Fehlerfrei

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "System")},
        }


class Sys_Betriebsanzeige(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Betriebsanzeige"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        #
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Sys_Betriebsanzeige

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "System")},
        }


#####################
#   Heizkreis       #
#####################
class HK_RaumSollTemperatur(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Raumsolltemperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_Raumsolltemperatur

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
            "name": "Wärmepumpe-Heizkreis",
            # "sw_version": "Device_SW_Version",
            # "model": "Device_model",
            "manufacturer": "Weishaupt",
        }


class HK_RaumTemperatur(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Raumtemperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_Raumtemperatur

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_RaumFeuchte(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    _attr_name = "Raumfeuchte"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = "%"
    _attr_device_class = SensorDeviceClass.MOISTURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_Raumfeuchte

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_VorlaufSollTemperatur(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    _attr_name = "VorlaufSollTemperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_Vorlaufsolltemperatur

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_VorlaufTemperatur(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    _attr_name = "VorlaufTemperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_Vorlauftemperatur

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


#####################
#   Warmwasser      #
#####################


class sensor_measured_temp(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Ist Temperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.WW_Ist

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Warmwasser")},
            "name": "Wärmepumpe-Warmwasser",
            "manufacturer": "Weishaupt",
        }


class sensor_target_temp(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Soll Temperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.WW_Soll

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Warmwasser")},
        }


class WW_Konfiguration(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Konfiguration"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.WW_Konfiguration

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Warmwasser")},
        }

    #####################
    #   Heatpump        #
    #####################


class HP_Betrieb(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Betrieb"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Hp_Betrieb

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Wärmepumpe")},
            "name": "Wärmepumpe-Wärmepumpe",
            "manufacturer": "Weishaupt",
        }


class HP_Stoermeldung(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Störmeldung"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Hp_Stoermeldung

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Wärmepumpe")},
        }


class HP_Leistungsanforderung(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Leistungsanforderung"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_unit_of_measurement = "%"
    _attr_should_poll = True

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Hp_Leistungsanforderung

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Wärmepumpe")},
        }


class Hp_Vorlauftemperatur(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Vorlauftemperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Hp_Vorlauftemperatur

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Wärmepumpe")},
        }


class Hp_Ruecklauftemperatur(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Rücklauftemperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Hp_Ruecklauftemperatur

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Wärmepumpe")},
        }


#####################
#   2. WEZ          #
#####################

#####################
#   Eingänge        #
#####################


#####################
#   Statistik       #
#####################


class Energy_today(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Energie heute"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Energy_total_today

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Statistik")},
            "name": "Wärmepumpe-Statistik",
            "manufacturer": "Weishaupt",
        }


class Energy_yesterday(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Energie gestern"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Energy_total_yesterday

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Statistik")},
        }


class Energy_month(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Energie Monat"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Energy_total_month

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Statistik")},
        }


class Energy_year(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Energie Jahr"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.Energy_total_year

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Statistik")},
        }


class EnergySensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = ""
    _attr_unique_id = ""
    _attr_should_poll = True
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY

    def __init__(self, myWp, name, device, method) -> None:
        """Init."""
        self._myWp = myWp
        self._attr_name = name
        self._attr_unique_id = DOMAIN + self._attr_name
        self._device = device
        # self._method = method()

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        self._myWp.connect()
        self._attr_native_value = 21

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._device)},
        }
