from dataclasses import dataclass
from .const import TYPES, FORMATS
from .items import ModbusItem, StatusItem

@dataclass(frozen=True)
class DeviceConstants:
    SYS = "System"
    WP = "Wärmepumpe"
    WW = "Warmwasser"

DEVICES = DeviceConstants()

##############################################################################################################################
# Listen mit Fehlermeldungen, Warnmeldungen und Statustexte
# Beschreibungstext ist ebenfalls m�glich
# class StatusItem(): def __init__(self, number, text, description = None):
##############################################################################################################################

SYS_FEHLER = [
    StatusItem(65535,"kein Fehler"),
]

SYS_WARNUNG = [
    StatusItem(65535,"keine Warnung"),
    StatusItem(32,"Fehler Kältesatz (32)"),
]

SYS_FEHLERFREI = [
    StatusItem(0,"Fehler aktiv"),
    StatusItem(1,"Störungsfreier Betrieb"),
]

SYS_BETRIEBSANZEIGE = [
    StatusItem(0,"undefiniert"),
    StatusItem(1,"Relaistest"),
    StatusItem(2,"Notaus"),
    StatusItem(3,"Diagnose"),
    StatusItem(4,"Handbetrieb"),
    StatusItem(5,"Handbetrieb Heizen"),
    StatusItem(6,"Handbetrieb Kühlen"),
    StatusItem(7,"Manueller Abtaubetrieb"),
    StatusItem(8,"Abtauen"),
    StatusItem(9,"2. WEZ"),
    StatusItem(10,"EVU_SPERRE"),
    StatusItem(11,"SG Tarif"),
    StatusItem(12,"SG Maximal"),
    StatusItem(13,"Tarifladung"),
    StatusItem(14,"Erhöhter Betrieb"),
    StatusItem(15,"Standzeit"),
    StatusItem(16,"Standby"),
    StatusItem(17,"Spülen"),
    StatusItem(18,"Frostschutz"),
    StatusItem(19,"Heizbetrieb"),
    StatusItem(20,"Warmwasserbetrieb"),
    StatusItem(21,"Legionellenschutz"),
    StatusItem(22,"Umschaltung HZ KU"),
    StatusItem(23,"Kühlbetrieb"),
    StatusItem(24,"Passive Kühlung"),
    StatusItem(25,"Sommerbetrieb"),
    StatusItem(26,"Schwimmbadbetrieb"),
    StatusItem(27,"Urlaub"),
    StatusItem(28,"Estrichprogramm"),
    StatusItem(29,"Gesperrt"),
    StatusItem(30,"Sperre AT"),
    StatusItem(31,"Sperre Sommer"),
    StatusItem(32,"Sperre Winter"),
    StatusItem(33,"Einsatzgrenze"),
    StatusItem(34,"HK Sperre"),
    StatusItem(35,"Absenkbetrieb"),
    StatusItem(43,"Ölrückführung"),
]

SYS_BETRIEBSART = [
    StatusItem(0,"Automatik"),
    StatusItem(1,"Heizen"),
    StatusItem(2,"Kühlen"),
    StatusItem(3,"Sommer"),
    StatusItem(4,"Standby"),
    StatusItem(5,"2.WEZ"),
]

HP_BETRIEB = [
    StatusItem(0,"Undefiniert"),
    StatusItem(1,"Relaistest"),
    StatusItem(2,"Notaus"),
    StatusItem(3,"Diagnose"),
    StatusItem(4,"Handbetrieb"),
    StatusItem(5,"Handbetrieb Heizen"),
    StatusItem(6,"Handbetrieb Kühlen"),
    StatusItem(7,"Manueller Abtaubetrieb"),
    StatusItem(8,"Abtauen"),
    StatusItem(9,"WEZ2"),
    StatusItem(10,"EVU_SPERRE"),
    StatusItem(11,"SG Tarif"),
    StatusItem(12,"SG Maximal"),
    StatusItem(13,"Tarifladung"),
    StatusItem(14,"Erhöhter Betrieb"),
    StatusItem(15,"Standzeit"),
    StatusItem(16,"Standbybetrieb"),
    StatusItem(17,"Spülbetrieb"),
    StatusItem(18,"Frostschutz"),
    StatusItem(19,"Heizbetrieb"),
    StatusItem(20,"Warmwasserbetrieb"),
    StatusItem(21,"Legionellenschutz"),
    StatusItem(22,"Umschaltung HZ KU"),
    StatusItem(23,"Kühlbetrieb"),
    StatusItem(24,"Passive Kühlung"),
    StatusItem(25,"Sommerbetrieb"),
    StatusItem(26,"Schwimmbad"),
    StatusItem(27,"Urlaub"),
    StatusItem(28,"Estrich"),
    StatusItem(29,"Gesperrt"),
    StatusItem(30,"Sperre AT"),
    StatusItem(31,"Sperre Sommer"),
    StatusItem(32,"Sperre Winter"),
    StatusItem(33,"Einsatzgrenze"),
    StatusItem(34,"HK Sperre"),
    StatusItem(35,"Absenk"),
    StatusItem(43,"Ölrückführung"),
]

HP_STOERMELDUNG = [
    StatusItem(0,"Störung"),
    StatusItem(1,"Störungsfrei"),
]

HP_RUHEMODUS = [
    StatusItem(0,"aus"),
    StatusItem(1,"80 %"),
    StatusItem(2,"60 %"),
    StatusItem(3,"40 %"),
]

##############################################################################################################################
# Modbus Register List:                                                                                                      #
# https://docs.google.com/spreadsheets/d/1EZ3QgyB41xaXo4B5CfZe0Pi8KPwzIGzK/edit?gid=1730751621#gid=1730751621                #
##############################################################################################################################

MODBUS_SYS_ITEMS = [
    ModbusItem(30001,"Aussentemperatur 1",FORMATS.TEMPERATUR,TYPES.SENSOR,DEVICES.SYS),
    ModbusItem(30002,"Aussentemperatur 2",FORMATS.TEMPERATUR,TYPES.SENSOR,DEVICES.SYS),
    ModbusItem(30003,"Fehler",FORMATS.STATUS,TYPES.SENSOR,DEVICES.SYS, SYS_FEHLER),
    ModbusItem(30004,"Warnung",FORMATS.STATUS,TYPES.SENSOR,DEVICES.SYS, SYS_WARNUNG),
    ModbusItem(30005,"Fehlerfrei",FORMATS.STATUS,TYPES.SENSOR,DEVICES.SYS, SYS_FEHLERFREI),
    ModbusItem(30006,"Betriebsanzeige",FORMATS.STATUS,TYPES.SENSOR,DEVICES.SYS, SYS_BETRIEBSANZEIGE),
    ModbusItem(40001,"Systembetriebsart",FORMATS.STATUS,TYPES.SELECT,DEVICES.SYS, SYS_BETRIEBSART),

    ModbusItem(33101,"Betrieb",FORMATS.STATUS,TYPES.SENSOR,DEVICES.WP, HP_BETRIEB),
    ModbusItem(33102,"Störmeldung",FORMATS.STATUS,TYPES.SENSOR,DEVICES.WP, HP_STOERMELDUNG),
    ModbusItem(33103,"Leistungsanforderung",FORMATS.PERCENTAGE,TYPES.SENSOR,DEVICES.WP),
    ModbusItem(33104,"Vorlauftemperatur",FORMATS.TEMPERATUR,TYPES.SENSOR,DEVICES.WP),
    ModbusItem(33105,"Rücklauftemperatur",FORMATS.TEMPERATUR,TYPES.SENSOR,DEVICES.WP),
    ModbusItem(43101,"Konfiguration ",FORMATS.NUMBER,TYPES.NUMBER,DEVICES.WP),
    ModbusItem(43102,"Ruhemodus",FORMATS.STATUS,TYPES.SELECT,DEVICES.WP,HP_RUHEMODUS),
    ModbusItem(43103,"Pumpe Einschaltart",FORMATS.NUMBER,TYPES.NUMBER,DEVICES.WP),
    #ModbusItem(43104,"Pumpe Leistung Heizen",
    #ModbusItem(43105,"Pumpe Leistung Kühlen",
    #ModbusItem(43106,"Pumpe Leistung Warmwasser",
    #ModbusItem(43107,"Pumpe Leistung Abtaubetrieb",
    #ModbusItem(43108,"Volumenstrom Heizen",
    #ModbusItem(43109,"Volumenstrom Kühlen",
    #ModbusItem(43110,"Volumenstrom Warmwasser",
] 