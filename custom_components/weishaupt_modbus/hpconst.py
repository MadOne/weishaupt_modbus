"""Heatpump constants."""

import copy
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
    UK = "Unknown"
    IO = "Eingänge/Ausgänge"


DEVICES = DeviceConstants()


@dataclass(frozen=True)
class DeviceLists:
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
    UK = "Unknown"
    IO = "Eingänge/Ausgänge"


reverse_device_list = {
    "System": "SYS",
    "Wärmepumpe": "WP",
    "Warmwasser": "WW",
    "Heizkreis": "HZ",
    "Heizkreis2": "HZ2",
    "Heizkreis3": "HZ3",
    "Heizkreis4": "HZ4",
    "Heizkreis5": "HZ5",
    "2. Wärmeerzeuger": "W2",
    "Statistik": "ST",
    "Unbekannt": "UK",
    "Eingänge/Ausgänge": "IO",
}

##############################################################################################################################
# Listen mit Fehlermeldungen, Warnmeldungen und Statustexte
# Beschreibungstext ist ebenfalls möglich
# class StatusItem(): def __init__(self, number, text, description = None):
##############################################################################################################################

# fmt: off
SYS_FEHLER = [
    StatusItem(65535,'kein Fehler'),
    StatusItem(1,'Kältemittelfühler Expansionsventil Eintritt (T1)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(2,'Luftansaugfühler (T2)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(3,'Wärmetauscherfühler AG Austritt (T3)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(4,'Verdichtersauggasfühler (T4)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(5,'EVI-Sauggasfühler (T5)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(6,'Kältemittelfühler IG Austritt (T6)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(7,'Ölsumpffühler (T7)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(8,'Expansionsventil EVI', 'Leitung prüfen, ggf. austauschen. Ggf. defektes Expansionsventil austauschen.'),
    StatusItem(9,'Niederdrucksensor (P1)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(10,'Hochdrucksensor (P2)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(11,'Mitteldrucksensor (P3)', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(12,'Expansionsventil Kühlen defekt', 'Leitung prüfen, ggf. austauschen. Expansionsventil austauschen.'),
    StatusItem(13,'keine Kommunikation zum Inverter', 'Lastspannung am Verdichter und Inverter prüfen. & Verbindungsleitung Steuerplatine Kältesatz zu Inverter prüfen. & Ggf. defekte Steuerplatine Kältesatz austauschen.'),
    StatusItem(14,'keine Kommunikation zum Außengerät', 'Verbindungsleitung zum Außengerät prüfen.'),
    StatusItem(15,'Hochdruckschalter hat ausgelöst', 'Drücke im Kältekreis kontrollieren. Volumenstrom prüfen. & Verdrahtung prüfen. & Sicherstellen, dass die Einsatzgrenzen der Wärmepumpe eingehalten werden. & Kältekreis prüfen.'),
    StatusItem(16,'Inverter gesperrt, da in den letzten 10 Stunden 10 Fehler aufgetreten sind', 'Spannungsversorgung mindestens 10 Minuten unterbrechen. Bei wiederholtem Auftreten Weishaupt-Kundendienst benachrichtigen.'),
    StatusItem(17,'EEPROM Speicher-Fehler', 'Spannungsversorgung mindestens 10 Minuten unterbrechen.'),
    StatusItem(18,'keine Modbus-Kommunikation zwischen Regler EC und Steuerplatine Kältesatz', 'Modbus-Verbindung prüfen.'),
    StatusItem(19,'durch Inverter-Alarm Wärmepumpe abgeschaltet', 'Bei wiederholtem Auftreten Weishaupt-Kundendienst benachrichtigen.'),
    StatusItem(20,'Verdichter passt nicht zur Konfiguration', 'Verdichtertyp prüfen. & Spannungsversorgung mindestens 10 Minuten unterbrechen.'),
    StatusItem(21,'Niederdruck-Störung', 'Verdampfer auf Eisfreiheit prüfen. Funktion Ventilator prüfen. & Niederdrucksensor (P1) prüfen. Kältekreis prüfen.'),
    StatusItem(22,'zu geringe Überhitzung', 'Wenn der Fehler wiederholt auftritt: Überhitzung prüfen. & Verdichtersauggasfühler (T4) prüfen. Niederdrucksensor (P1) prüfen. & Antrieb Expansionsventil prüfen. Kältekreis prüfen.'),
    StatusItem(23,'zu hohe Überhitzung', 'Wenn der Fehler wiederholt auftritt: Überhitzung prüfen. & Verdichtersauggasfühler (T4) prüfen. Niederdrucksensor (P1) prüfen. & Antrieb Expansionsventil prüfen. Kältekreis prüfen.'),
    StatusItem(24,'EVI zu hohe Überhitzung', 'Wenn der Fehler wiederholt auftritt: Kältekreis prüfen. & Lecksuche durchführen.'),
    StatusItem(25,'Kältemittelmenge zu niedrig', 'Wenn der Fehler wiederholt auftritt: Kältekreis prüfen. & Lecksuche durchführen.'),
    StatusItem(26,'Hochdruck-Störung', 'Wärmeabnahme prüfen. & Hohe Warmwasser-Solltemperaturen vermeiden. & Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Einstellung Überströmventil prüfen.'),
    StatusItem(27,'Kondensationstemperatur zu niedrig', 'Der erwartete Betriebszustand wird bei hoher Außentemperatur und geringer Vorlauftemperatur nicht erreichen. & Anlage mit 2. Wärmeerzeuger hochheizen.'),
    StatusItem(28,'Kondensationstemperatur zu hoch', 'Wärmeabnahme prüfen. Einstellung Überströmventil prüfen. Heizwasser-Volumenstrom prüfen.'),
    StatusItem(29,'Verdampfungstemperatur zu niedrig', 'Verdampfer auf Eisfreiheit prüfen. Funktion Ventilator prüfen. & Kältekreis prüfen.'),
    StatusItem(30,'Verdampfungstemperatur zu hoch', 'Die Einsatzgrenze der Wärmepumpe wurde überschritten. & Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird.'),
    StatusItem(32,'Wärmepumpe nicht kompatibel', 'Spannungsversorgung Verdichter prüfen. Spannungsversorgung von den Klemmen zum Kältesatz prüfen. & Weishaupt-Kundendienst benachrichtigen.'),
    StatusItem(33,'Regler EC hat keine Verbindung zum Erweiterungsmodul EM-HK', 'Verbindungsleitung zwischen Regler und Erweiterungsmodul prüfen.'),
    StatusItem(40,'Volumenstrom zu gering', 'Mindestvolumenstrom beachten [Kap. 3.4.6]. Volumenstrom prüfen, ggf. erhöhen. & Leitung Volumenstromsensor (B10) prüfen. Volumenstromsensor (B10) prüfen, ggf. austauschen.'),
    StatusItem(41,'Spreizung LWT/Rücklauf negativ / Vierwegeventil schaltet nach dem Abtauen nicht zurück; nach 3 Warnungen verriegelt die Anlage)', 'Volumenstrom anpassen. Pumpenleistung reduzieren. Vierwegeventil prüfen. & Ggf. Funktion deaktivieren.'),
    StatusItem(43,'Ventilator blockiert', 'Verdampfer auf Eisfreiheit prüfen. Funktion Ventilator prüfen.'),
    StatusItem(44,'Drehzahl Ventilator zu niedrig', 'Verdampfer auf Eisfreiheit prüfen. Funktion Ventilator prüfen.'),
    StatusItem(47,'Kommunikation Regler EC zu Steuerplatine Kältesatz fehlerhaft', 'Leitung prüfen, ggf. austauschen.'),
    StatusItem(50,'Außenfühler (B1) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(51,'Außenfühler (B1) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(52,'Weichenfühler (B2) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(53,'Weichenfühler (B2) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(54,'Warmwasserfühler (B3) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(55,'Warmwasserfühler (B3) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(56,'Vorlauffühler Verflüssiger (B4) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(57,'Vorlauffühler Verflüssiger (B4) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(58,'Vorlauffühler (B7) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(59,'Vorlauffühler (B7) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(60,'Rücklauffühler (B9) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(61,'Rücklauffühler (B9) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(64,'Pufferfühler (B11) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(65,'Pufferfühler (B11) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(66,'Mischerfühler regenerativ (B2.1) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(67,'Mischerfühler regenerativ (B2.1) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(70,'Vorlauffühler Zweiter Heizkreis (B6.2) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(71,'Vorlauffühler Zweiter Heizkreis (B6.2) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(72,'Fühler (T1.2) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(73,'Fühler (T1.2) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(74,'Fühler (T2.2) unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(75,'Fühler (T2.2) kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(90,'Analogeingang AE1 unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(91,'Analogeingang AE1 kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(92,'Analogeingang AE2 unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(93,'Analogeingang AE2 kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(94,'Analogeingang AE3 unterbrochen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(95,'Analogeingang AE3 kurzgeschlossen', 'Fühler und Leitung prüfen, ggf. austauschen.'),
    StatusItem(101,'Wärmepumpe wird außerhalb der Einsatzgrenzen betrieben', 'Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird, siehe W 26 bis W 30.'),
    StatusItem(102,'maximale Abtauzeit überschritten', 'Bei exponiertem Aufstellungsort kann starker Wind zu dieser Warnung führen. Nach der Abtauung Verdampfer auf Eisfreiheit prüfen.'),
    StatusItem(103,'Kommunikation Kältekreis fehlerhaft', 'Spannungsversorgung mindestens 10 Minuten unterbrechen. Bei wiederholtem Auftreten Weishaupt-Kundendienst benachrichtigen.'),
    StatusItem(104,'Druckgastemperatur zu hoch', 'Wärmeabnahme prüfen. Kältekreis prüfen.'),
    StatusItem(105,'Stromaufnahme vom Inverter zu hoch', 'Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Verdichteranschluss am Inverter prüfen.'),
    StatusItem(106,'Stromaufnahme zu hoch', 'Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Spannungsversorgung prüfen (Netzspannung zu gering). & Drosselspulen in der 400 V Zuleitung zum Inverter prüfen.'),
    StatusItem(107,'Gleichspannung am Inverter zu hoch', 'Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Spannungsversorgung prüfen.'),
    StatusItem(108,'Gleichspannung am Inverter zu niedrig', 'Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Spannungsversorgung prüfen.'),
    StatusItem(109,'Wärmepumpe wird außerhalb vom zulässigen Spannungsbereich betrieben', 'Spannungsversorgung prüfen.'),
    StatusItem(110,'Wärmepumpe wird außerhalb vom zulässigen Spannungsbereich betrieben', 'Spannungsversorgung prüfen.'),
    StatusItem(111,'Hochdruckschalter hat ausgelöst', 'Wärmeabnahme prüfen. & Einstellung vom Überströmventil prüfen. Stellung der Kugelhähne am Innenund Außengerät prüfen. & Drücke im Kältekreis kontrollieren. Volumenstrom kontrollieren. & Verdrahtung prüfen. & Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Kältekreis prüfen.'),
    StatusItem(112,'Inverter ist überhitzt', 'Sicherstellen, dass: die Montagebedingungen für das Innengerät eingehalten werden & die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird & Weishaupt-Kundendienst benachrichtigen (Version der Steuerplatine Kältesatz RCC Modbus prüfen).'),
    StatusItem(113,'Inverter ist überhitzt', 'Sicherstellen, dass: die Montagebedingungen für das Innengerät eingehalten werden & die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird & Weishaupt-Kundendienst benachrichtigen (Version der Steuerplatine Kältesatz RCC Modbus prüfen).'),
    StatusItem(114,'Stellung vom Verdichtermotor kann nicht bestimmt werden', 'Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Verdichteranschluss am Inverter prüfen.'),
    StatusItem(117,'Gleichspannung am Inverter zu niedrig', 'Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Spannungsversorgung prüfen.'),
    StatusItem(118,'Strom zwischen Inverter und Verdichter ist zu hoch', 'Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Verdichteranschluss am Inverter prüfen. Verdichter-Wicklungswiderstände messen.'),
    StatusItem(119,'Stromaufnahme vom Verdichter zu hoch Zeitüberschreitung', 'Sicherstellen, dass die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird. & Verdichteranschluss am Inverter prüfen. Verdichter-Wicklungswiderstände messen.'),
    StatusItem(120,'Invertertemperatur zu hoch', 'Sicherstellen, dass: die Montagebedingungen für das Innengerät eingehalten werden & die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird'),
    StatusItem(121,'Spannung am Inverter zu gering', 'Spannung nach den Drosselspulen messen.'),
    StatusItem(122,'Modbus-Konfigurationsfehler', 'Spannungsversorgung mindestens 10 Minuten unterbrechen.'),
    StatusItem(123,'keine Modbus-Verbindung', 'Modbus-Verbindung (Leitung und Stecker) zwischen Inverter und Steuerplatine Kältesatz prüfen. & Spannungsversorgung mindestens 10 Minuten unterbrechen.'),
    StatusItem(124,'Druckgastemperatur zu hoch', 'Wärmeabnahme prüfen. Kältekreis prüfen.'),
    StatusItem(127,'Invertertemperatur zu hoch', 'Sicherstellen, dass: die Montagebedingungen für das Innengerät eingehalten werden & die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird'),
    StatusItem(128,'Inverter ist überhitzt', 'Sicherstellen, dass: die Montagebedingungen für das Innengerät eingehalten werden & die Wärmepumpe innerhalb der Einsatzgrenzen betrieben wird & Weishaupt-Kundendienst benachrichtigen (Version der Steuerplatine Kältesatz RCC Modbus prüfen).'),
    StatusItem(129,'Modbus-Kommunikation fehlerhaft', 'Modbus-Verbindung zwischen Inverter und Steuerplatine Kältesatz prüfen (Leitung und Stecker). & Spannungsversorgung mindestens 10 Minuten unterbrechen.'),
    StatusItem(130,'Modbus-Kommunikation fehlerhaft', 'Modbus-Verbindung zwischen Inverter und Steuerplatine Kältesatz prüfen (Leitung und Stecker). & Spannungsversorgung mindestens 10 Minuten unterbrechen.'),
    StatusItem(133,'Elektronikfehler', 'Spannungsversorgung mindestens 10 Minuten unterbrechen.'),
    StatusItem(135,'Hochdruckschalter defekt', 'Hochdruckschalter-Anschluss prüfen.'),
    StatusItem(136,'Verdichter passt nicht zur Konfiguration', 'Verdichtertyp prüfen. & Spannungsversorgung mindestens 10 Minuten unterbrechen.'),
    StatusItem(137,'Hochdruckschalter passt nicht zur Konfiguration', 'Hochdruckschalter prüfen. Spannungsversorgung mindestens 10 Minuten unterbrechen.'),
    StatusItem(140,'Druckgastemperatur zu niedrig', 'Druckgasfühler (DT) und Leitung prüfen, ggf. austauschen.'),
    StatusItem(143,'Invertertemperatur zu niedrig', 'Kühlung am Inverter prüfen. Gerät neu starten.'),
    StatusItem(144,'Drosselspulentemperatur zu niedrig', 'Sicherstellen, dass die Montagebedingungen für das Innengerät eingehalten werden.'),
    StatusItem(150,"Verdichter Stromsensor Phase U Fehler"),
    StatusItem(151,"Verdichter Stromsensor Phase V Fehler"),
    StatusItem(152,"Verdichter Stromsensor Phase W Fehler Spannungsversorgung von Eingangsklemme"),
    StatusItem(153,"Stromsensor Fehler"),
    StatusItem(154,"Inverter Temperatursensor Fehler"),
    StatusItem(155,"Temperatursensor Fehler"),
    StatusItem(156,"Druckgasfühler (DT)"),
    StatusItem(157,"keine Kommunikation zur Steuerplatine Kältesatz"),
    StatusItem(158,"EEPROM-Speicher-Fehler"),
    StatusItem(159,"Stromaufnahme zu hoch"),
    StatusItem(160,"Wärmepumpe wird außerhalb vom zulässigen Spannungsbereich betrieben"),
    StatusItem(161,"Wärmepumpe wird außerhalb vom zulässigen Spannungsbereich betriebe"),
    StatusItem(162,"Gleichspannung am Inverter zu hoch"),
    StatusItem(163,"Gleichspannung am Inverter zu niedrig"),
    StatusItem(164,"Hochdruckschalter hat ausgelöst"),
    StatusItem(165,"Phase zwischen Eingang und Verdichter unterbrochen"),
    StatusItem(166,"Inverter überhitzt"),
    StatusItem(167,"Inverter überhitzt"),
    StatusItem(168,"Konfigurationsfehler Verdichter"),
    StatusItem(169,"Stromaufnahme vom Verdichter zu hoch"),
    StatusItem(170,"Verdichter Phase U Überspannung"),
    StatusItem(171,"Verdichter Phase V Überspannung"),
    StatusItem(172,"Verdichter Phase W Überspannung"),
    StatusItem(173,"Phasenausfall am Verdichter"),
    StatusItem(174,"Verdichter blockiert"),
    StatusItem(175,"Verdichter startet nicht"),
    StatusItem(176,"Unregelmäßige Spannungsversorgung vom Inverter"),
    StatusItem(177,"Verdichter überlastet"),
    StatusItem(178,"Temperatur am Druckgasfühler (DT) zu hoch"),
    StatusItem(179,"Temperatur am Inverter"),
    StatusItem(180,"Verdichter blockiert"),
    StatusItem(181,"Verdichter blockiert"),
    StatusItem(182,"Stromaufnahme zu hoch"),
    StatusItem(183,"Stromaufnahme zu hoch"),
    StatusItem(184,"Spannung zu hoch"),
]  # noqa: E501

# fmt: on

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
    StatusItem(36, "Vorlauf regenerativ"),
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
    StatusItem(1, "Heizen"),
    StatusItem(2, "Heizen, Kühlen"),
    StatusItem(3, "Heizen, Kühlen, Warmwasser"),
    StatusItem(4, "Heizen, Warmwasser"),
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


IO_KONFIG = [
    StatusItem(0, "0"),
    StatusItem(1, "1"),
    StatusItem(2, "2"),
    StatusItem(3, "3"),
    StatusItem(4, "4"),
    StatusItem(5, "5"),
    StatusItem(6, "6"),
    StatusItem(7, "7"),
    StatusItem(65535, "65535"),
]

IO_KONFIG_IN = [
    StatusItem(
        0,
        "SG Ready",
        "Siehe Smart-Grid-Funktion [Kap. 6.7.7.2]. Funktion kann nur in SGR1 gewählt werden und wird automatisch auf SGR2 übertragen, in SGR2 sind dann die anderen Funktionen gesperrt.",
    ),
    StatusItem(
        1,
        "EVU-Sperre:",
        "Heiz- und Kühlbetrieb und Warmwasserladung gesperrt, Frostschutz ist sichergestellt.",
    ),
    StatusItem(
        2,
        "Erhöhter Betrieb",
        "Zu der Vorlaufsolltemperatur im Heizbetrieb und der Warmwasser-Solltemperatur wird die eingestellte ",
    ),
    StatusItem(
        3,
        "HK-Sperre",
        "Heiz- und Kühlbetrieb gesperrt, Frostschutz ist sichergestellt, Warmwasserladung weiterhin betriebsbereit. ",
    ),
    StatusItem(
        4,
        "Umschaltung Hz/Kü:",
        "Wärmeanforderungen werden ignoriert, nur Kühlanforderungen wirken auf die Wärmepumpe. Die Funktion Umschaltung Hz/Kü hat Vorrang vor Erhöhter Betrieb.",
    ),
    StatusItem(5, "Ruhemodus", "Manueller Ruhemodus, externer Kontakt [Kap. 6.7.5.2]."),
    StatusItem(6, "Not-Aus:", "Wärmepumpe, Elektroheizung und Pumpe aus."),
    StatusItem(7, "System Standby:", "Standby"),
    StatusItem(8, "Erzeugersperre HZ:", "Heizkreis durch Wärmepumpe gesperrt."),
    StatusItem(9, "Erzeugersperre WW:", "Warmwasserladung durch Wärmepumpe gesperrt."),
    StatusItem(
        10,
        "Erzeugersperre HZ und WW:",
        "Heizkreis und Warmwasserladung durch Wärmepumpe gesperrt",
    ),
    StatusItem(11, "Warmwasser Standby:", "Warmwasserladung Standby."),
    StatusItem(12, "Warmwasser Absenk:", "Warmwasserladung im Absenkbetrieb."),
    StatusItem(13, "Warmwasser Normal:", "Warmwasserladung im Normalbetrieb."),
    StatusItem(
        14,
        "Warmwasser PUSH:",
        "Vom Zeitprogramm abweichender Warmwasserbedarf. Der Trinkwasserspeicher wird auf Normaltemperatur aufgeheizt und gehalten.",
    ),
    StatusItem(15, "Taupunktwächter", "Kühlbetrieb für Heizkreise gesperrt."),
    StatusItem(16, "Heizkreis … Standby:", "Heizkreis im Standby."),
    StatusItem(17, "Heizkreis … Absenk:", "Heizkreis im Absenkbetrieb"),
    StatusItem(18, "Heizkreis … Normal:", "Heizkreis im Normalbetrieb."),
    StatusItem(19, "Heizkreis … Komfort:", "Heizkreis im Komfortbetrieb"),
    StatusItem(20, "2.WEZ", "2. Wärmeerzeuger über Eingang aktivieren."),
    StatusItem(
        21,
        "Sperre Verdichter:",
        "Externe Vorgabe zur Sperre vom Verdichter.ng für Digitaleingang DE",
    ),
    StatusItem(65535, "AUS", "Keine Funktion, wird nicht angesteuert."),
]

IO_KONFIG_OUT = [
    StatusItem(0, "AUS", "Keine Funktion, wird nicht angesteuert."),
    StatusItem(
        1,
        "Zirkulationspumpe",
        "Ausgang wird periodisch während dem Warmwasserprogramm angesteuert.",
    ),
    StatusItem(
        2,
        "ext. Heizkreispumpe",
        "Ausgang wird im Heizbetrieb der Wärmepumpe angesteuert.",
    ),
    StatusItem(3, "Schaltuhr", "Ausgang wird nach Zeitprogramm angesteuert."),
    StatusItem(
        4, "Störmeldung", "Ausgang wird im Fehlerfall der Wärmepumpe angesteuert."
    ),
    StatusItem(
        5, "Kühlbetrieb", "Ausgang wird im Kühlbetrieb der Wärmepumpe angesteuert."
    ),
    StatusItem(
        6,
        "Verdichterbetrieb",
        "Ausgang wird bei Verdichterbetrieb der Wärmepumpe angesteuert.",
    ),
    StatusItem(
        7, "Warmwasserbetrieb", "Ausgang wird bei Warmwasserladung angesteuert."
    ),
    StatusItem(
        8,
        "Dauerspannung",
        "Ausgang wird bei eingeschaltetem Innengerät angesteuert.",
    ),
    StatusItem(
        9,
        "Betriebsweitermeldung",
        "Ausgang wird bei Verdichterbetrieb angesteuert.",
    ),
    StatusItem(
        10,
        "Hz- WW-Betrieb",
        "Ausgang wird im Heizbetrieb oder bei Warmwasserladung angesteuert.",
    ),
    StatusItem(
        11,
        "Düsenringheizung",
        "Ausgang wird bei zusätzlicher Heizung am Düsenring im Außengerät angesteuert.",
    ),
    StatusItem(
        12,
        "Kondensatwannenheizung",
        "Ausgang wird bei zusätzlicher Heizung in der Kondensatwanne im Außengerät angesteuert",
    ),
    StatusItem(
        13,
        "Pumpe HK1",
        "Ausgang wird bei Pumpenbetrieb für einen direkten Heizkreis angesteuert.",
    ),
    StatusItem(
        14,
        "Umlenkventil Heizen",
        "Ausgang wird angesteuert, wenn das Dreiwegeventil auf Heizbetrieb steht.",
    ),
    StatusItem(
        15,
        "Umlenkventil Warmwasser",
        "Ausgang wird angesteuert, wenn das Dreiwegeventil auf Warmwasserladung steht.",
    ),
    StatusItem(
        65535,
        "Umlenkventil Kühlen",
        "Ausgang wird angesteuert, wenn das Dreiwegeventil auf Kühlbetrieb steht.",
    ),
    StatusItem(65535, "65535", "Keine Funktion, wird nicht angesteuert."),
]

IO_KONFIG_SGR = [
    StatusItem(0, "0"),
    StatusItem(1, "1"),
    StatusItem(2, "2"),
    StatusItem(3, "3"),
    StatusItem(4, "4"),
    StatusItem(5, "5"),
    StatusItem(6, "6"),
    StatusItem(7, "7"),
    StatusItem(65535, "65535"),
]

IO_STATUS = [
    StatusItem(0, "aus"),
    StatusItem(1, "ein"),
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
    ModbusItem( 30004, "Warnung", FORMATS.STATUS, TYPES.SENSOR, DEVICES.SYS, SYS_FEHLER), # same codes as for warnings
    ModbusItem( 30005, "Fehlerfrei", FORMATS.STATUS, TYPES.SENSOR, DEVICES.SYS, SYS_FEHLERFREI),
    ModbusItem( 30006, "Betriebsanzeige", FORMATS.STATUS, TYPES.SENSOR, DEVICES.SYS, SYS_BETRIEBSANZEIGE),
    ModbusItem( 40001,  "Systembetriebsart", FORMATS.STATUS, TYPES.SELECT, DEVICES.SYS, SYS_BETRIEBSART),
] # noqa: E501

MODBUS_WP_ITEMS = [
    ModbusItem( 33101, "Betrieb", FORMATS.STATUS, TYPES.SENSOR, DEVICES.WP, HP_BETRIEB),
    ModbusItem( 33102, "Störmeldung", FORMATS.STATUS, TYPES.SENSOR, DEVICES.WP, HP_STOERMELDUNG),
    ModbusItem( 33103, "Leistungsanforderung", FORMATS.PERCENTAGE, TYPES.SENSOR, DEVICES.WP),
    ModbusItem( 33103, "Wärmeleistung", FORMATS.POWER, TYPES.SENSOR_CALC, DEVICES.WP, RANGE_CALCPOWER),
    ModbusItem( 33104, "Vorlauftemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WP, TEMPRANGE_STD),
    ModbusItem( 33105, "Rücklauftemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR,  DEVICES.WP, TEMPRANGE_STD),
    ModbusItem( 33106, "Verdampfungstemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WP, TEMPRANGE_STD),
    ModbusItem( 33107, "Verdichtersauggastemp", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WP, TEMPRANGE_STD),
    ModbusItem( 33108, "Weichentemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WP),
    ModbusItem( 33109, "Anforderung", FORMATS.PERCENTAGE, TYPES.SENSOR, DEVICES.WP),
    ModbusItem( 33110, "Adr. 33110", FORMATS.UNKNOWN, TYPES.SENSOR, DEVICES.WP),
    ModbusItem( 33111, "Vorlauftemperatur präzise", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WP, TEMPRANGE_STD),

    ModbusItem( 43101, "Konfiguration ", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.WP, HP_KONFIGURATION),
    ModbusItem( 43102, "Ruhemodus", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.WP, HP_RUHEMODUS),
    ModbusItem( 43103, "Pumpe Einschaltart", FORMATS.NUMBER, TYPES.NUMBER_RO, DEVICES.WP ),
    ModbusItem( 43104, "Sollwert Pumpe Leistung Heizen", FORMATS.PERCENTAGE, TYPES.NUMBER_RO, DEVICES.WP, RANGE_PERCENTAGE),
    ModbusItem( 43105, "Sollwert Pumpe Leistung Kühlen", FORMATS.PERCENTAGE, TYPES.NUMBER_RO, DEVICES.WP, RANGE_PERCENTAGE),
    ModbusItem( 43106, "Sollwert Pumpe Leistung Warmwasser", FORMATS.PERCENTAGE, TYPES.NUMBER_RO, DEVICES.WP, RANGE_PERCENTAGE),
    ModbusItem( 43107, "Sollwert Pumpe Leistung Abtaubetrieb", FORMATS.PERCENTAGE, TYPES.NUMBER_RO, DEVICES.WP, RANGE_PERCENTAGE),
    ModbusItem( 43108, "Sollwert Volumenstrom Heizen", FORMATS.VOLUMENSTROM, TYPES.NUMBER_RO, DEVICES.WP, RANGE_FLOWRATE),
    ModbusItem( 43109, "Sollwert Volumenstrom Kühlen", FORMATS.VOLUMENSTROM, TYPES.NUMBER_RO,  DEVICES.WP, RANGE_FLOWRATE),
    ModbusItem( 43110, "Sollwert Volumenstrom Warmwasser", FORMATS.VOLUMENSTROM, TYPES.NUMBER_RO, DEVICES.WP, RANGE_FLOWRATE),
] # noqa: E501

MODBUS_HZ_ITEMS = [
    ModbusItem( 31101, "Raumsolltemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 31102, "Raumtemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ, TEMPRANGE_ROOM),
    ModbusItem( 31103, "Raumfeuchte", FORMATS.PERCENTAGE, TYPES.SENSOR, DEVICES.HZ),
    ModbusItem( 31104, "Vorlaufsolltemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ, TEMPRANGE_STD),
    ModbusItem( 31105, "HZ_Vorlauftemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.HZ, TEMPRANGE_STD),
    ModbusItem( 31106, "Adr. 31106", FORMATS.UNKNOWN, TYPES.SENSOR, DEVICES.HZ),
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
] # noqa: E501

# buils other Heizkreis Itemlists
MODBUS_HZ2_ITEMS = []
for index, item in enumerate(MODBUS_HZ_ITEMS):
    mbi = copy.deepcopy(item)
    mbi.address = item.address+100
    mbi.name = item.name + "2"
    mbi.device = DEVICES.HZ2
    MODBUS_HZ2_ITEMS.append(mbi)  # noqa: PERF401

# buils other Heizkreis Itemlists
MODBUS_HZ3_ITEMS = []
for index, item in enumerate(MODBUS_HZ_ITEMS):
    mbi = copy.deepcopy(item)
    mbi.address = item.address+200
    mbi.name = item.name + "3"
    mbi.device = DEVICES.HZ3
    MODBUS_HZ3_ITEMS.append(mbi)  # noqa: PERF401

# buils other Heizkreis Itemlists
MODBUS_HZ4_ITEMS = []
for index, item in enumerate(MODBUS_HZ_ITEMS):
    mbi = copy.deepcopy(item)
    mbi.address = item.address+300
    mbi.name = item.name + "4"
    mbi.device = DEVICES.HZ4
    MODBUS_HZ4_ITEMS.append(mbi)  # noqa: PERF401

# buils other Heizkreis Itemlists
MODBUS_HZ5_ITEMS = []
for index, item in enumerate(MODBUS_HZ_ITEMS):
    mbi = copy.deepcopy(item)
    mbi.address = item.address+400
    mbi.name = item.name + "5"
    mbi.device = DEVICES.HZ5
    MODBUS_HZ5_ITEMS.append(mbi)  # noqa: PERF401

MODBUS_WW_ITEMS = [
    ModbusItem( 32101, "Warmwassersolltemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WW, TEMPRANGE_WATER),
    ModbusItem( 32102, "Warmwassertemperatur", FORMATS.TEMPERATUR, TYPES.SENSOR, DEVICES.WW, TEMPRANGE_WATER),
    ModbusItem( 42101, "WW_Konfiguration", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.WW, WW_KONFIGURATION),
    ModbusItem( 42102, "Warmwasser Push", FORMATS.STATUS, TYPES.SELECT, DEVICES.WW, WW_PUSH),
    ModbusItem( 42103, "Warmwasser Normal", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.WW, TEMPRANGE_WATER),
    ModbusItem( 42104, "Warmwasser Absenk", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.WW, TEMPRANGE_WATER),
    ModbusItem( 42105, "SG Ready Anhebung", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.WW, TEMPRANGE_SGREADY),
] # noqa: E501

MODBUS_W2_ITEMS = [
    ModbusItem( 34101, "Status 2. WEZ", FORMATS.STATUS, TYPES.SENSOR, DEVICES.W2, W2_STATUS),
    ModbusItem( 34102, "Schaltspiele E-Heizung 1", FORMATS.NUMBER, TYPES.SENSOR, DEVICES.W2),
    ModbusItem( 34103, "Betriebsstunden E1", FORMATS.TIME_H, TYPES.SENSOR, DEVICES.W2),
    ModbusItem( 34104, "Status E-Heizung 1", FORMATS.STATUS, TYPES.SENSOR, DEVICES.W2, W2_STATUS),
    ModbusItem( 34105, "Status E-Heizung 2", FORMATS.STATUS, TYPES.SENSOR, DEVICES.W2, W2_STATUS),
    ModbusItem( 34106, "Schaltspiele E-Heizung 2", FORMATS.NUMBER, TYPES.SENSOR, DEVICES.W2),
    ModbusItem( 34107, "Betriebsstunden E2", FORMATS.TIME_H, TYPES.SENSOR, DEVICES.W2),
    ModbusItem( 44101, "W2_Konfiguration", FORMATS.STATUS, TYPES.SENSOR, DEVICES.W2, W2_KONFIG),
    ModbusItem( 44102, "Grenztemperatur", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.W2, TEMPRANGE_BIVALENZ),
    ModbusItem( 44103, "Bivalenztemperatur", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.W2, TEMPRANGE_BIVALENZ),
    ModbusItem( 44104, "Bivalenztemperatur WW", FORMATS.TEMPERATUR, TYPES.NUMBER, DEVICES.W2, TEMPRANGE_BIVALENZ),
] # noqa: E501

MODBUS_ST_ITEMS = [
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
    ModbusItem( 36801, "Adr. 36801", FORMATS.UNKNOWN, TYPES.SENSOR, DEVICES.ST),
] # noqa: E501


MODBUS_IO_ITEMS = [
    ModbusItem( 35101, "SG-Ready 1", FORMATS.UNKNOWN, TYPES.SENSOR, DEVICES.IO),
    ModbusItem( 35102, "SG-Ready 2", FORMATS.UNKNOWN, TYPES.SENSOR, DEVICES.IO),
    ModbusItem( 35103, "Ausgang H1.2", FORMATS.UNKNOWN, TYPES.SENSOR, DEVICES.IO),
    ModbusItem( 35104, "Ausgang H1.3", FORMATS.UNKNOWN, TYPES.SENSOR, DEVICES.IO),
    ModbusItem( 35105, "Ausgang H1.4", FORMATS.UNKNOWN, TYPES.SENSOR, DEVICES.IO),
    ModbusItem( 35106, "Ausgang H1.5", FORMATS.UNKNOWN, TYPES.SENSOR, DEVICES.IO),
    ModbusItem( 35107, "Eingang DE1", FORMATS.STATUS, TYPES.SENSOR, DEVICES.IO, W2_STATUS),
    ModbusItem( 35108, "Eingang DE2", FORMATS.STATUS, TYPES.SENSOR, DEVICES.IO, W2_STATUS),

    ModbusItem( 45101, "Konf. Eingang SGR1", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.IO, resultlist=IO_KONFIG_IN),
    ModbusItem( 45102, "Konf. Eingang SGR2", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.IO, resultlist=IO_KONFIG_IN),
    ModbusItem( 45103, "Konf. Ausgang H1.2", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.IO, resultlist=IO_KONFIG),
    ModbusItem( 45104, "Konf. Ausgang  H1.3", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.IO, resultlist=IO_KONFIG),
    ModbusItem( 45105, "Konf. Ausgang  H1.4", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.IO, resultlist=IO_KONFIG),
    ModbusItem( 45106, "Konf. Ausgang  H1.5", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.IO, resultlist=IO_KONFIG),
    ModbusItem( 45107, "Konf. Eingang DE1", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.IO, resultlist=IO_KONFIG_IN),
    ModbusItem( 45108, "Konf. Eingang DE2", FORMATS.STATUS, TYPES.NUMBER_RO, DEVICES.IO, resultlist=IO_KONFIG_IN),
] # noqa: E501

DEVICELISTS = [
    MODBUS_SYS_ITEMS,
    MODBUS_WP_ITEMS,
    MODBUS_WW_ITEMS,
    MODBUS_HZ_ITEMS,
    MODBUS_HZ2_ITEMS,
    MODBUS_HZ3_ITEMS,
    MODBUS_HZ4_ITEMS,
    MODBUS_HZ5_ITEMS,
    MODBUS_W2_ITEMS,
    MODBUS_ST_ITEMS,
    MODBUS_IO_ITEMS
]

# fmt: on
