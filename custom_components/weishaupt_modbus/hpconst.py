"""Heatpump constants."""

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass

from .const import FORMATS, TYPES
from .items import ModbusItem, StatusItem


@dataclass(frozen=True)
class DeviceConstants:
    """Device constants."""

    SYS = "System"
    WP = "Wärmepumpe"
    WW = "Warmwasser"
    HZ = "Heizkreis"
    HZ2 = "Heizkreis2"
    HZ3 = "Heizkreis3"
    HZ4 = "Heizkreis4"
    HZ5 = "Heizkreis5"
    W2 = "2. Wärmeerzeuger"
    ST = "Statistik"


DEVICES = DeviceConstants()

##############################################################################################################################
# Listen mit Fehlermeldungen, Warnmeldungen und Statustexte
# Beschreibungstext ist ebenfalls möglich
# class StatusItem(): def __init__(self, number, text, description = None):
##############################################################################################################################

SYS_FEHLER = [
    StatusItem(65535, "kein Fehler"),
]

SYS_WARNUNG = [
    StatusItem(65535, "keine Warnung"),
    StatusItem(32, "Fehler Kältesatz (32)"),
]

SYS_FEHLERFREI = [
    StatusItem(0, "Fehler aktiv"),
    StatusItem(1, "Störungsfreier Betrieb"),
]

SYS_BETRIEBSANZEIGE = [
    StatusItem(0, "undefiniert"),
    StatusItem(1, "Relaistest"),
    StatusItem(2, "Notaus"),
    StatusItem(3, "Diagnose"),
    StatusItem(4, "Handbetrieb"),
    StatusItem(5, "Handbetrieb Heizen"),
    StatusItem(6, "Handbetrieb Kühlen"),
    StatusItem(7, "Manueller Abtaubetrieb"),
    StatusItem(8, "Abtauen"),
    StatusItem(9, "2. WEZ"),
    StatusItem(10, "EVU_SPERRE"),
    StatusItem(11, "SG Tarif"),
    StatusItem(12, "SG Maximal"),
    StatusItem(13, "Tarifladung"),
    StatusItem(14, "Erhöhter Betrieb"),
    StatusItem(15, "Standzeit"),
    StatusItem(16, "Standby"),
    StatusItem(17, "Spülen"),
    StatusItem(18, "Frostschutz"),
    StatusItem(19, "Heizbetrieb"),
    StatusItem(20, "Warmwasserbetrieb"),
    StatusItem(21, "Legionellenschutz"),
    StatusItem(22, "Umschaltung HZ KU"),
    StatusItem(23, "Kühlbetrieb"),
    StatusItem(24, "Passive Kühlung"),
    StatusItem(25, "Sommerbetrieb"),
    StatusItem(26, "Schwimmbadbetrieb"),
    StatusItem(27, "Urlaub"),
    StatusItem(28, "Estrichprogramm"),
    StatusItem(29, "Gesperrt"),
    StatusItem(30, "Sperre AT"),
    StatusItem(31, "Sperre Sommer"),
    StatusItem(32, "Sperre Winter"),
    StatusItem(33, "Einsatzgrenze"),
    StatusItem(34, "HK Sperre"),
    StatusItem(35, "Absenkbetrieb"),
    StatusItem(43, "Ölrückführung"),
]

SYS_BETRIEBSART = [
    StatusItem(0, "Automatik"),
    StatusItem(1, "Heizen"),
    StatusItem(2, "Kühlen"),
    StatusItem(3, "Sommer"),
    StatusItem(4, "Standby"),
    StatusItem(5, "2.WEZ"),
]

HP_BETRIEB = [
    StatusItem(0, "Undefiniert"),
    StatusItem(1, "Relaistest"),
    StatusItem(2, "Notaus"),
    StatusItem(3, "Diagnose"),
    StatusItem(4, "Handbetrieb"),
    StatusItem(5, "Handbetrieb Heizen"),
    StatusItem(6, "Handbetrieb Kühlen"),
    StatusItem(7, "Manueller Abtaubetrieb"),
    StatusItem(8, "Abtauen"),
    StatusItem(9, "WEZ2"),
    StatusItem(10, "EVU_SPERRE"),
    StatusItem(11, "SG Tarif"),
    StatusItem(12, "SG Maximal"),
    StatusItem(13, "Tarifladung"),
    StatusItem(14, "Erhöhter Betrieb"),
    StatusItem(15, "Standzeit"),
    StatusItem(16, "Standbybetrieb"),
    StatusItem(17, "Spülbetrieb"),
    StatusItem(18, "Frostschutz"),
    StatusItem(19, "Heizbetrieb"),
    StatusItem(20, "Warmwasserbetrieb"),
    StatusItem(21, "Legionellenschutz"),
    StatusItem(22, "Umschaltung HZ KU"),
    StatusItem(23, "Kühlbetrieb"),
    StatusItem(24, "Passive Kühlung"),
    StatusItem(25, "Sommerbetrieb"),
    StatusItem(26, "Schwimmbad"),
    StatusItem(27, "Urlaub"),
    StatusItem(28, "Estrich"),
    StatusItem(29, "Gesperrt"),
    StatusItem(30, "Sperre AT"),
    StatusItem(31, "Sperre Sommer"),
    StatusItem(32, "Sperre Winter"),
    StatusItem(33, "Einsatzgrenze"),
    StatusItem(34, "HK Sperre"),
    StatusItem(35, "Absenk"),
    StatusItem(43, "Ölrückführung"),
]

HP_STOERMELDUNG = [
    StatusItem(0, "Störung"),
    StatusItem(1, "Störungsfrei"),
]

HP_RUHEMODUS = [
    StatusItem(0, "aus"),
    StatusItem(1, "80 %"),
    StatusItem(2, "60 %"),
    StatusItem(3, "40 %"),
]

HZ_KONFIGURATION = [
    StatusItem(0, "aus"),
    StatusItem(1, "Pumpenkreis"),
    StatusItem(2, "Mischkreis"),
    StatusItem(3, "Sollwert (Pumpe M1)"),
]

HZ_ANFORDERUNG = [
    StatusItem(0, "aus"),
    StatusItem(1, "witterungsgeführt"),
    StatusItem(2, "konstant"),
]

HZ_BETRIEBSART = [
    StatusItem(0, "Automatik"),
    StatusItem(1, "Komfort"),
    StatusItem(2, "Normal"),
    StatusItem(3, "Absenkbetrieb"),
    StatusItem(4, "Standby"),
]

HZ_PARTY_PAUSE = [
    StatusItem(1, "Pause 12.0h"),
    StatusItem(2, "Pause 11.5h"),
    StatusItem(3, "Pause 11.0h"),
    StatusItem(4, "Pause 10.5h"),
    StatusItem(5, "Pause 10.0h"),
    StatusItem(6, "Pause 9.5h"),
    StatusItem(7, "Pause 9.0h"),
    StatusItem(8, "Pause 8.5h"),
    StatusItem(9, "Pause 8.0h"),
    StatusItem(10, "Pause 7.5h"),
    StatusItem(11, "Pause 7.0h"),
    StatusItem(12, "Pause 6.5h"),
    StatusItem(13, "Pause 6.0h"),
    StatusItem(14, "Pause 5.5h"),
    StatusItem(15, "Pause 5.0h"),
    StatusItem(16, "Pause 4.5h"),
    StatusItem(17, "Pause 4.0h"),
    StatusItem(18, "Pause 3.5h"),
    StatusItem(19, "Pause 3.0h"),
    StatusItem(20, "Pause 2.5h"),
    StatusItem(21, "Pause 2.0h"),
    StatusItem(22, "Pause 1.5h"),
    StatusItem(23, "Pause 1.0h"),
    StatusItem(24, "Pause 0.5h"),
    StatusItem(25, "Automatik"),
    StatusItem(26, "Party 0.5h"),
    StatusItem(27, "Party 1.0h"),
    StatusItem(28, "Party 1.5h"),
    StatusItem(29, "Party 2.0h"),
    StatusItem(30, "Party 2.5h"),
    StatusItem(31, "Party 3.0h"),
    StatusItem(32, "Party 3.5h"),
    StatusItem(33, "Party 4.0h"),
    StatusItem(34, "Party 4.5h"),
    StatusItem(35, "Party 5.0h"),
    StatusItem(36, "Party 5.5h"),
    StatusItem(37, "Party 6.0h"),
    StatusItem(38, "Party 6.5h"),
    StatusItem(39, "Party 7.0h"),
    StatusItem(40, "Party 7.5h"),
    StatusItem(41, "Party 8.0h"),
    StatusItem(42, "Party 8.5h"),
    StatusItem(43, "Party 9.0h"),
    StatusItem(44, "Party 9.5h"),
    StatusItem(45, "Party 10.0h"),
    StatusItem(46, "Party 10.5h"),
    StatusItem(47, "Party 11.0h"),
    StatusItem(48, "Party 11.5h"),
    StatusItem(49, "Party 12.0h"),
]

WW_KONFIGURATION = [
    StatusItem(0, "aus"),
    StatusItem(1, "Umlenkventil"),
    StatusItem(2, "Pumpe"),
]

HP_KONFIGURATION = [
    StatusItem(0, "Ncht konfiguriert"),
    StatusItem(1, "Heizen verfügbar"),
    StatusItem(2, "Heizen, Kühlen verfügbar"),
    StatusItem(3, "Heizen, Kühlen, Warmwasser verfügbar"),
    StatusItem(4, "Heizen, Warmwasser verfügbar"),
]

WW_PUSH = [
    StatusItem(0, "AUS"),
]
# Fill WW_PUSH with values for every 5 Minutes
for i in range(5, 240, 5):
    WW_PUSH.append(StatusItem(i, str(i) + "Minuten"))  # noqa: PERF401

W2_STATUS = [
    StatusItem(0, "aus"),
    StatusItem(1, "ein"),
]

W2_KONFIG = [
    StatusItem(0, "0"),
    StatusItem(1, "1"),
]

#####################################################
# Description of physical units via the status list #
#####################################################

RANGE_PERCENTAGE = [
    StatusItem(0, "min"),
    StatusItem(100, "max"),
    StatusItem(1, "step"),
    StatusItem(1, "divider"),
]

TEMPRANGE_ROOM = [
    StatusItem(16, "min"),
    StatusItem(30, "max"),
    StatusItem(0.5, "step"),
    StatusItem(10, "divider"),
    StatusItem(-1, SensorDeviceClass.TEMPERATURE),
]

TEMPRANGE_WATER = [
    StatusItem(30, "min"),
    StatusItem(60, "max"),
    StatusItem(0.5, "step"),
    StatusItem(10, "divider"),
    StatusItem(-1, SensorDeviceClass.TEMPERATURE),
]

TEMPRANGE_SGREADY = [
    StatusItem(0, "min"),
    StatusItem(10, "max"),
    StatusItem(0.5, "step"),
    StatusItem(10, "divider"),
    StatusItem(-1, SensorDeviceClass.TEMPERATURE),
]

TEMPRANGE_BIVALENZ = [
    StatusItem(-20, "min"),
    StatusItem(10, "max"),
    StatusItem(0.5, "step"),
    StatusItem(10, "divider"),
    StatusItem(-1, SensorDeviceClass.TEMPERATURE),
]

TEMPRANGE_STD = [
    StatusItem(-60, "min"),
    StatusItem(100, "max"),
    StatusItem(0.5, "step"),
    StatusItem(10, "divider"),
    StatusItem(-1, SensorDeviceClass.TEMPERATURE),
]


RANGE_HZKENNLINIE = [
    StatusItem(0, "min"),
    StatusItem(3, "max"),
    StatusItem(0.05, "step"),
    StatusItem(100, "divider"),
]

TIMERANGE_WWPUSH = [
    StatusItem(0, "min"),
    StatusItem(240, "max"),
    StatusItem(5, "step"),
    StatusItem(1, "divider"),
]

RANGE_FLOWRATE = [
    StatusItem(0, "min"),
    StatusItem(3, "max"),
    StatusItem(0.1, "step"),
    StatusItem(100, "divider"),
]

RANGE_ENERGY = [
    StatusItem(-1, SensorDeviceClass.ENERGY),
    StatusItem(1, "divider"),
]

RANGE_CALCPOWER = [
    StatusItem(-1, SensorDeviceClass.POWER),
    StatusItem(1, "divider"),
    StatusItem(30002, "x"),
    StatusItem(33104, "y"),
]

# pylint: disable=line-too-long

##############################################################################################################################
# Modbus Register List:                                                                                                      #
# https://docs.google.com/spreadsheets/d/1EZ3QgyB41xaXo4B5CfZe0Pi8KPwzIGzK/edit?gid=1730751621#gid=1730751621                #
##############################################################################################################################

# fmt: off
MODBUS_SYS_ITEMS = [
    ModbusItem( 30001, "Aussentemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.SYS, TEMPRANGE_STD),
    ModbusItem( 30002, "Luftansaugtemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.SYS, TEMPRANGE_STD),
    ModbusItem( 30003, "Fehler", FORMATS.STATUS, TYPES.SENSOR, DEVICES.SYS, SYS_FEHLER),
    ModbusItem( 30004, "Warnung", FORMATS.STATUS, TYPES.SENSOR, DEVICES.SYS, SYS_WARNUNG),
    ModbusItem( 30005, "Fehlerfrei", FORMATS.STATUS, TYPES.SENSOR, DEVICES.SYS, SYS_FEHLERFREI),
    ModbusItem( 30006, "Betriebsanzeige", FORMATS.STATUS, TYPES.SENSOR, DEVICES.SYS, SYS_BETRIEBSANZEIGE),
    ModbusItem( 40001,  "Systembetriebsart", FORMATS.STATUS, TYPES.SELECT, DEVICES.SYS, SYS_BETRIEBSART),
    ModbusItem( 33101, "Betrieb", FORMATS.STATUS, TYPES.SENSOR, DEVICES.WP, HP_BETRIEB),
    ModbusItem( 33102, "Störmeldung", FORMATS.STATUS, TYPES.SENSOR, DEVICES.WP, HP_STOERMELDUNG),
    ModbusItem( 33103, "Leistungsanforderung", FORMATS.PERCENTAGE, TYPES.SENSOR, DEVICES.WP),
    ModbusItem( 33103, "Wärmeleistung", FORMATS.POWER, TYPES.SENSOR_CALC, DEVICES.WP, RANGE_CALCPOWER),
    ModbusItem( 33104, "Vorlauftemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WP, TEMPRANGE_STD),
    ModbusItem( 33105, "Rücklauftemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR,  DEVICES.WP, TEMPRANGE_STD),
    ModbusItem( 43101, "Konfiguration ", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.WP, HP_KONFIGURATION),
    ModbusItem( 43102, "Ruhemodus", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.WP, HP_RUHEMODUS),
    ModbusItem( 43103, "Pumpe Einschaltart", FORMATS.NUMBER, TYPES.NUMBER_RO, DEVICES.WP ),
    ModbusItem( 43104, "Pumpe Leistung Heizen", FORMATS.PERCENTAGE, TYPES.NUMBER_RO, DEVICES.WP, RANGE_PERCENTAGE),
    ModbusItem( 43105, "Pumpe Leistung Kühlen", FORMATS.PERCENTAGE, TYPES.NUMBER_RO, DEVICES.WP, RANGE_PERCENTAGE),
    ModbusItem( 43106, "Pumpe Leistung Warmwasser", FORMATS.PERCENTAGE, TYPES.NUMBER_RO, DEVICES.WP, RANGE_PERCENTAGE),
    ModbusItem( 43107, "Pumpe Leistung Abtaubetrieb", FORMATS.PERCENTAGE, TYPES.NUMBER_RO, DEVICES.WP, RANGE_PERCENTAGE),
    ModbusItem( 43108, "Volumenstrom Heizen", FORMATS.VOLUMENSTROM, TYPES.NUMBER_RO, DEVICES.WP, RANGE_FLOWRATE),
    ModbusItem( 43109, "Volumenstrom Kühlen", FORMATS.VOLUMENSTROM, TYPES.NUMBER_RO,  DEVICES.WP, RANGE_FLOWRATE),
    ModbusItem( 43110, "Volumenstrom Warmwasser", FORMATS.VOLUMENSTROM, TYPES.NUMBER_RO, DEVICES.WP, RANGE_FLOWRATE),

    ModbusItem( 31101, "Raumsolltemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 31102, "Raumtemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 31103, "Raumfeuchte", FORMATS.PERCENTAGE, TYPES.SENSOR, DEVICES.HZ),
    ModbusItem( 31104, "Vorlaufsolltemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ, TEMPRANGE_STD),
    ModbusItem( 31105, "HZ_Vorlauftemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ, TEMPRANGE_STD),
    ModbusItem( 41101, "HZ_Konfiguration", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.HZ, HZ_KONFIGURATION),
    ModbusItem( 41102, "Anforderung Typ", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.HZ, HZ_ANFORDERUNG),
    ModbusItem( 41103, "Betriebsart", FORMATS.STATUS, TYPES.SELECT, DEVICES.HZ, HZ_BETRIEBSART),
    ModbusItem( 41104, "Pause / Party", FORMATS.STATUS, TYPES.SELECT, DEVICES.HZ, HZ_PARTY_PAUSE),
    ModbusItem( 41105, "Raumsolltemperatur Komfort", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 41106, "Raumsolltemperatur Normal", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 41107, "Raumsolltemperatur Absenk", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 41108, "Heizkennlinie", FORMATS.KENNLINIE, TYPES.NUMBER, DEVICES.HZ, RANGE_HZKENNLINIE),
    ModbusItem( 41109, "Sommer Winter Umschaltung", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 41110, "Heizen Konstanttemperatur", FORMATS.TEMPERATUR, TYPES.NUMBER_RO, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 41111, "Heizen Konstanttemp Absenk", FORMATS.TEMPERATUR, TYPES.NUMBER_RO, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 41112, "Kühlen Konstanttemperatur", FORMATS.TEMPERATUR, TYPES.NUMBER_RO, DEVICES.HZ, TEMPRANGE_ROOM),

    ModbusItem( 31201, "Raumsolltemperatur2", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ2, TEMPRANGE_ROOM),
    ModbusItem( 31202, "Raumtemperatur2", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ2, TEMPRANGE_ROOM),
    ModbusItem( 31203, "Raumfeuchte2", FORMATS.PERCENTAGE, TYPES.SENSOR, DEVICES.HZ2),
    ModbusItem( 31204, "Vorlaufsolltemperatur2", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ2, TEMPRANGE_STD),
    ModbusItem( 31205, "HZ_Vorlauftemperatur2", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ2, TEMPRANGE_STD),
    ModbusItem( 41201, "HZ_Konfiguration2", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.HZ2, HZ_KONFIGURATION),
    ModbusItem( 41202, "Anforderung Typ2", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.HZ2, HZ_ANFORDERUNG),
    ModbusItem( 41203, "Betriebsart2", FORMATS.STATUS, TYPES.SELECT, DEVICES.HZ2, HZ_BETRIEBSART),
    ModbusItem( 41204, "Pause / Party 2", FORMATS.STATUS, TYPES.SELECT, DEVICES.HZ2, HZ_PARTY_PAUSE),
    ModbusItem( 41205, "Raumsolltemperatur Komfort2", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.HZ2, TEMPRANGE_ROOM),
    ModbusItem( 41206, "Raumsolltemperatur Normal2", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.HZ2, TEMPRANGE_ROOM),
    ModbusItem( 41207, "Raumsolltemperatur Absenk2", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.HZ2, TEMPRANGE_ROOM),
    ModbusItem( 41208, "Heizkennlinie2", FORMATS.KENNLINIE, TYPES.NUMBER, DEVICES.HZ2, RANGE_HZKENNLINIE),
    ModbusItem( 41209, "Sommer Winter Umschaltung2", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.HZ2, TEMPRANGE_ROOM),
    ModbusItem( 41210, "Heizen Konstanttemperatur2", FORMATS.TEMPERATUR, TYPES.NUMBER_RO, DEVICES.HZ2, TEMPRANGE_ROOM),
    ModbusItem( 41211, "Heizen Konstanttemp Absenk2", FORMATS.TEMPERATUR, TYPES.NUMBER_RO, DEVICES.HZ2, TEMPRANGE_ROOM),
    ModbusItem( 41212, "Kühlen Konstanttemperatur2", FORMATS.TEMPERATUR, TYPES.NUMBER_RO, DEVICES.HZ2, TEMPRANGE_ROOM),

    ModbusItem( 32101, "Warmwassersolltemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WW, TEMPRANGE_WATER),
    ModbusItem( 32102, "Warmwassertemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WW, TEMPRANGE_WATER),
    ModbusItem( 42101, "WW_Konfiguration", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.WW, WW_KONFIGURATION),
    ModbusItem( 42102, "Warmwasser Push", FORMATS.STATUS, TYPES.SELECT, DEVICES.WW, WW_PUSH),
    ModbusItem( 42103, "Warmwasser Normal", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.WW, TEMPRANGE_WATER),
    ModbusItem( 42104, "Warmwasser Absenk", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.WW, TEMPRANGE_WATER),
    ModbusItem( 42105, "SG Ready Anhebung", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.WW, TEMPRANGE_SGREADY),

    ModbusItem( 34101, "Status 2. WEZ", FORMATS.STATUS, TYPES.SENSOR, DEVICES.W2, W2_STATUS),
    ModbusItem( 34102, "Schaltspiele E-Heizung 1", FORMATS.NUMBER, TYPES.SENSOR, DEVICES.W2),
    ModbusItem( 34103, "Schaltspiele E-Heizung 2", FORMATS.NUMBER, TYPES.SENSOR, DEVICES.W2),
    ModbusItem( 34104, "Status E-Heizung 1", FORMATS.STATUS, TYPES.SENSOR, DEVICES.W2, W2_STATUS),
    ModbusItem( 34105, "Status E-Heizung 2", FORMATS.STATUS, TYPES.SENSOR, DEVICES.W2, W2_STATUS),
    ModbusItem( 34106, "Betriebsstunden E1", FORMATS.TIME_H, TYPES.SENSOR, DEVICES.W2),
    ModbusItem( 34107, "Betriebsstunden E2", FORMATS.TIME_H, TYPES.SENSOR, DEVICES.W2),
    ModbusItem( 44101, "W2_Konfiguration", FORMATS.STATUS, TYPES.SENSOR, DEVICES.W2, W2_KONFIG),
    ModbusItem( 44102, "Grenztemperatur", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.W2, TEMPRANGE_BIVALENZ),
    ModbusItem( 44103, "Bivalenztemperatur", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.W2, TEMPRANGE_BIVALENZ),
    ModbusItem( 44104, "Bivalenztemperatur WW", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.W2, TEMPRANGE_BIVALENZ),

    ModbusItem( 36101, "Gesamt Energie heute", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36102, "Gesamt Energie gestern", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36103, "Gesamt Energie Monat", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36104, "Gesamt Energie Jahr", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36201, "Heizen Energie heute", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36202, "Heizen Energie gestern", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36203, "Heizen Energie Monat", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36204, "Heizen Energie Jahr", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36301, "Warmwasser Energie heute", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36302, "Warmwasser Energie gestern", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36303, "Warmwasser Energie Monat", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36304, "Warmwasser Energie Jahr", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36401, "Kühlen Energie heute", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36402, "Kühlen Energie gestern", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36403, "Kühlen Energie Monat", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36404, "Kühlen Energie Jahr", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36501, "Abtauen Energie heute", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36502, "Abtauen Energie gestern", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36503, "Abtauen Energie Monat", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36504, "Abtauen Energie Jahr", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36601, "Gesamt Energie II heute", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36602, "Gesamt Energie II gestern", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36603, "Gesamt Energie II Monat", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36604, "Gesamt Energie II Jahr", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36701, "Elektr. Energie heute", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36702, "Elektr. Energie gestern", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36703, "Elektr. Energie Monat", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
    ModbusItem( 36704, "Elektr. Energie Jahr", FORMATS.ENERGY, TYPES.SENSOR, DEVICES.ST, RANGE_ENERGY),
] # noqa: E501
# fmt: on
