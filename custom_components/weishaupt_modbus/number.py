"""Number platform for wemportal component."""

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType

from . import wp
from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the wemportal component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
) -> None:
    """Set up Numbers."""
    hass.data.setdefault(DOMAIN, {})
    # hub = hass.data[DOMAIN][config_entry.entry_id]
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    # port = config_entry.data.get[CONF_PORT]
    # host = "10.10.1.225"
    # port = "502"
    async_add_entities(
        [
            WW_Normal(host, port),
            WW_Absenk(host, port),
            HK_Party(host, port),
            HK_Pause(host, port),
            HK_Raum_Soll_Komfort(host, port),
            HK_Raum_Soll_Normal(host, port),
            HK_Raum_Soll_Absenk(host, port),
            HK_Heizkennlinie(host, port),
            HK_SommerWinterUmschaltung(host, port),
            HK_Heizen_Konstanttemperatur(host, port),
            HK_Heizen_Konstanttemperatur_Absenk(host, port),
            HK_Kuehlen_Konstanttemperatur(host, port),
        ],
        update_before_add=True,
    )


class WW_Normal(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "WW Normal"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 40
    _attr_native_max_value = 60
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Normal
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.WW_Normal = int(value)

        self._attr_native_value = whp.WW_Normal
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.WW_Normal

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Warmwasser")},
        }


class WW_Absenk(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "WW Absenk"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 30
    _attr_native_max_value = 40
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.WW_Absenk = int(value)

        self._attr_native_value = whp.WW_Absenk
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.WW_Absenk

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Warmwasser")},
        }


class HK_Party(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Party"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 0
    _attr_native_max_value = 12
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = UnitOfTime.HOURS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # party_pause = whp.HK_Pause_Party
        # if party_pause > 25:
        #    self._attr_native_value = (party_pause - 25) * 0.5
        # else:
        #    self._attr_native_value = 0

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_Pause_Party = int(25 + (value / 0.5))
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        party_pause = whp.HK_Pause_Party
        if party_pause > 25:
            self._attr_native_value = (party_pause - 25) * 0.5
        else:
            self._attr_native_value = 0

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_Pause(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Pause"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 0
    _attr_native_max_value = 12
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = UnitOfTime.HOURS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # party_pause = whp.HK_Pause_Party
        # if party_pause < 25:
        #    self._attr_native_value = (25 - party_pause) * 0.5
        # else:
        #    self._attr_native_value = 0

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_Pause_Party = int(25 - (value / 0.5))
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        party_pause = whp.HK_Pause_Party
        if party_pause < 25:
            self._attr_native_value = (25 - party_pause) * 0.5
        else:
            self._attr_native_value = 0

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_Raum_Soll_Komfort(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Raumsollwert Komfort"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 20
    _attr_native_max_value = 30
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_RaumSoll_Komfort = int(value)
        self._attr_native_value = whp.HK_RaumSoll_Komfort
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_RaumSoll_Komfort

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_Raum_Soll_Normal(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Raumsollwert Normal"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 15
    _attr_native_max_value = 25
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_RaumSoll_Normal = int(value)
        self._attr_native_value = whp.HK_RaumSoll_Normal
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_RaumSoll_Normal

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_Raum_Soll_Absenk(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Raumsollwert Absenk"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 10
    _attr_native_max_value = 20
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_RaumSoll_Absenk = int(value)
        self._attr_native_value = whp.HK_RaumSoll_Absenk
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_RaumSoll_Absenk

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_Heizkennlinie(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Heizkennlinie"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 0
    _attr_native_max_value = 1.5
    _attr_native_step = 0.05
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_Heizkennlinie = value
        self._attr_native_value = whp.HK_Heizkennlinie
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_Heizkennlinie

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_SommerWinterUmschaltung(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Sommer Winter Umschaltung"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 3
    _attr_native_max_value = 30
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_SommerWinterUmschaltung = value
        self._attr_native_value = whp.HK_SommerWinterUmschaltung
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_SommerWinterUmschaltung

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_Heizen_Konstanttemperatur(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Heizen Konstanttemperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 20
    _attr_native_max_value = 45
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_HeizenKonstanttemperatur = int(value)
        self._attr_native_value = whp.HK_HeizenKonstanttemperatur
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_HeizenKonstanttemperatur

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_Heizen_Konstanttemperatur_Absenk(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Heizen Konstanttemperatur Absenk"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 20
    _attr_native_max_value = 30
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_HeizenKonstanttemperaturAbsenk = int(value)
        self._attr_native_value = whp.HK_HeizenKonstanttemperaturAbsenk
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_HeizenKonstanttemperaturAbsenk

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }


class HK_Kuehlen_Konstanttemperatur(NumberEntity):
    """Representation of a WEM Portal number."""

    _attr_name = "Kühlen Konstanttemperatur"
    _attr_unique_id = DOMAIN + _attr_name
    _attr_native_value = 0
    _attr_should_poll = True
    _attr_native_min_value = 15
    _attr_native_max_value = 25
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, host, port) -> None:
        """Init."""
        self._host = host
        self._port = port
        # whp = wp.heat_pump(host, port)
        # whp.connect()
        # self._attr_native_value = whp.WW_Absenk
        # self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        whp.HK_KuehlenKonstanttemperatur = int(value)
        self._attr_native_value = whp.HK_KuehlenKonstanttemperatur
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update Entity Only used by the generic entity update service."""
        whp = wp.heat_pump(self._host, self._port)
        whp.connect()
        self._attr_native_value = whp.HK_KuehlenKonstanttemperatur

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, "Heizkreis")},
        }
