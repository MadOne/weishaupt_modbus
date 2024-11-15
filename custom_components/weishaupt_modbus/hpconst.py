"""Heatpump constants."""

import copy

from homeassistant.components.sensor import SensorDeviceClass

from .const import FORMATS, TYPES, DEVICES
from .items import ModbusItem, StatusItem


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

################################################################################
# Listen mit Fehlermeldungen, Warnmeldungen und Statustexte
# Beschreibungstext ist ebenfalls möglich
# class StatusItem(): def __init__(self, number, text, description = None):
################################################################################

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
MODBUS_SYS_ITEMS: list[ModbusItem] = [
    ModbusItem( address=30001, name="Aussentemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.SYS, resultlist=TEMPRANGE_STD, translation_key="aussentemp"),
    ModbusItem( address=30002, name="Luftansaugtemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.SYS, resultlist=TEMPRANGE_STD, translation_key="luftansautgemp"),
    ModbusItem( address=30003, name="Fehler", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.SYS, resultlist=SYS_FEHLER, translation_key="fehler"),
    ModbusItem( address=30004, name="Warnung", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.SYS, resultlist=SYS_FEHLER, translation_key="warnung"), # same codes as for warnings
    ModbusItem( address=30005, name="Fehlerfrei", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.SYS, resultlist=SYS_FEHLERFREI, translation_key="fehlerfrei"),
    ModbusItem( address=30006, name="Betriebsanzeige", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.SYS, resultlist=SYS_BETRIEBSANZEIGE, translation_key="betriebsanzeige"),
    ModbusItem( address=40001,  name="Systembetriebsart", mformat=FORMATS.STATUS, mtype=TYPES.SELECT, device=DEVICES.SYS, resultlist=SYS_BETRIEBSART, translation_key="systembetriebsart"),
] # noqa: E501

MODBUS_WP_ITEMS: list[ModbusItem] = [
    ModbusItem( address=33101, name="Betrieb", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.WP, resultlist=HP_BETRIEB, translation_key="wp_betrieb"),
    ModbusItem( address=33102, name="Störmeldung", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.WP, resultlist=HP_STOERMELDUNG, translation_key="wp_stoermeldung"),
    ModbusItem( address=33103, name="Leistungsanforderung", mformat=FORMATS.PERCENTAGE, mtype=TYPES.SENSOR, device=DEVICES.WP, translation_key="leistungsanforderung"),
    ModbusItem( address=33103, name="Wärmeleistung", mformat=FORMATS.POWER, mtype=TYPES.SENSOR_CALC, device=DEVICES.WP, resultlist=RANGE_CALCPOWER, translation_key="waermeleistung"),
    ModbusItem( address=33104, name="Vorlauftemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.WP, resultlist=TEMPRANGE_STD, translation_key="vl_temp"),
    ModbusItem( address=33105, name="Rücklauftemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR,  device=DEVICES.WP, resultlist=TEMPRANGE_STD, translation_key="rl_temp"),
    ModbusItem( address=33106, name="Verdampfungstemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.WP, resultlist=TEMPRANGE_STD, translation_key="verdampfungs_temp"),
    ModbusItem( address=33107, name="Verdichtersauggastemp", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.WP, resultlist=TEMPRANGE_STD, translation_key="verdichter_ansaug_gas_temp"),
    ModbusItem( address=33108, name="Weichentemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.WP, translation_key="weichen_temp"),
    ModbusItem( address=33109, name="Anforderung(Vorlauf regenerativ)", mformat=FORMATS.PERCENTAGE, mtype=TYPES.SENSOR, device=DEVICES.WP, translation_key="anforderung_vl_regenerativ"),
    ModbusItem( address=33110, name="Puffertemperatur?", mformat=FORMATS.UNKNOWN, mtype=TYPES.SENSOR, device=DEVICES.WP, translation_key="puffer_temp"),
    ModbusItem( address=33111, name="Vorlauftemperatur präzise(Summenvorlauf(B7))", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.WP, resultlist=TEMPRANGE_STD, translation_key="vl_praeziese_summenvorlauf_b7"),

    ModbusItem( address=43101, name="Konfiguration ", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.WP, resultlist=HP_KONFIGURATION, translation_key="wp_konf"),
    ModbusItem( address=43102, name="Ruhemodus", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.WP, resultlist=HP_RUHEMODUS, translation_key="ruhemodus"),
    ModbusItem( address=43103, name="Pumpe Einschaltart", mformat=FORMATS.NUMBER, mtype=TYPES.NUMBER_RO, device=DEVICES.WP, translation_key="pumpe_einschaltart"),
    ModbusItem( address=43104, name="Sollwert Pumpe Leistung Heizen", mformat=FORMATS.PERCENTAGE, mtype=TYPES.NUMBER_RO, device=DEVICES.WP, resultlist=RANGE_PERCENTAGE, translation_key="sollwert_pumpe_leistung_heizen"),
    ModbusItem( address=43105, name="Sollwert Pumpe Leistung Kühlen", mformat=FORMATS.PERCENTAGE, mtype=TYPES.NUMBER_RO, device=DEVICES.WP, resultlist=RANGE_PERCENTAGE, translation_key="sollwert_pumpe_leistung_kuehlen"),
    ModbusItem( address=43106, name="Sollwert Pumpe Leistung Warmwasser", mformat=FORMATS.PERCENTAGE, mtype=TYPES.NUMBER_RO, device=DEVICES.WP, resultlist=RANGE_PERCENTAGE, translation_key="sollwert_pumpe_leitung_ww"),
    ModbusItem( address=43107, name="Sollwert Pumpe Leistung Abtaubetrieb", mformat=FORMATS.PERCENTAGE, mtype=TYPES.NUMBER_RO, device=DEVICES.WP, resultlist=RANGE_PERCENTAGE, translation_key="sollwert_pumpe_leistung_abtau"),
    ModbusItem( address=43108, name="Sollwert Volumenstrom Heizen", mformat=FORMATS.VOLUMENSTROM, mtype=TYPES.NUMBER_RO, device=DEVICES.WP, resultlist=RANGE_FLOWRATE, translation_key="soll_volumenstrom_heizen"),
    ModbusItem( address=43109, name="Sollwert Volumenstrom Kühlen", mformat=FORMATS.VOLUMENSTROM, mtype=TYPES.NUMBER_RO,  device=DEVICES.WP, resultlist=RANGE_FLOWRATE, translation_key="soll_volumenstrom_kuehlen"),
    ModbusItem( address=43110, name="Sollwert Volumenstrom Warmwasser", mformat=FORMATS.VOLUMENSTROM, mtype=TYPES.NUMBER_RO, device=DEVICES.WP, resultlist=RANGE_FLOWRATE, translation_key="soll_volumenstrom_ww"),
] # noqa: E501

MODBUS_HZ_ITEMS = [
    ModbusItem( address=31101, name="Raumsolltemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.HZ, resultlist=TEMPRANGE_ROOM, translation_key="raum_soll_temp"),
    ModbusItem( address=31102, name="Raumtemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.HZ, resultlist=TEMPRANGE_ROOM, translation_key="raum_temp"),
    ModbusItem( address=31103, name="Raumfeuchte", mformat=FORMATS.PERCENTAGE, mtype=TYPES.SENSOR, device=DEVICES.HZ, translation_key="raum_feuchte"),
    ModbusItem( address=31104, name="Vorlaufsolltemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.HZ, resultlist=TEMPRANGE_STD, translation_key="vl_temp"),
    ModbusItem( address=31105, name="HZ_Vorlauftemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.HZ, resultlist=TEMPRANGE_STD, translation_key="hz_vl_temp"),
    ModbusItem( address=31106, name="Adr. 31106", mformat=FORMATS.UNKNOWN, mtype=TYPES.SENSOR, device=DEVICES.HZ, translation_key="adr31106"),
    ModbusItem( address=41101, name="HZ_Konfiguration", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.HZ, resultlist=HZ_KONFIGURATION, translation_key="hz_konf"),
    ModbusItem( address=41102, name="Anforderung Typ", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.HZ, resultlist=HZ_ANFORDERUNG, translation_key="anf_typ"),
    ModbusItem( address=41103, name="Betriebsart", mformat=FORMATS.STATUS, mtype=TYPES.SELECT, device=DEVICES.HZ, resultlist=HZ_BETRIEBSART, translation_key="hz_betriebsart"),
    ModbusItem( address=41104, name="Pause / Party", mformat=FORMATS.STATUS, mtype=TYPES.SELECT, device=DEVICES.HZ, resultlist=HZ_PARTY_PAUSE, translation_key="party_pause"),
    ModbusItem( address=41105, name="Raumsolltemperatur Komfort", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.HZ, resultlist=TEMPRANGE_ROOM, translation_key="raum_soll_temp_komf"),
    ModbusItem( address=41106, name="Raumsolltemperatur Normal", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.HZ, resultlist=TEMPRANGE_ROOM, translation_key="raum_soll_temp_normal"),
    ModbusItem( address=41107, name="Raumsolltemperatur Absenk", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.HZ, resultlist=TEMPRANGE_ROOM, translation_key="raum_soll_temp_absenk"),
    ModbusItem( address=41108, name="Heizkennlinie", mformat=FORMATS.KENNLINIE, mtype=TYPES.NUMBER, device=DEVICES.HZ, resultlist=RANGE_HZKENNLINIE, translation_key="heizkennlinie"),
    ModbusItem( address=41109, name="Sommer Winter Umschaltung", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.HZ, resultlist=TEMPRANGE_ROOM, translation_key="so_wi_umschalt"),
    ModbusItem( address=41110, name="Heizen Konstanttemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER_RO, device=DEVICES.HZ, resultlist=TEMPRANGE_ROOM, translation_key="heiz_konstanttemp"),
    ModbusItem( address=41111, name="Heizen Konstanttemp Absenk", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER_RO, device=DEVICES.HZ, resultlist=TEMPRANGE_ROOM, translation_key="heiz_konstanttemp_absenk"),
    ModbusItem( address=41112, name="Kühlen Konstanttemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER_RO, device=DEVICES.HZ, resultlist=TEMPRANGE_ROOM, translation_key="kuehl_konstanttemp"),
] # noqa: E501

# buils other Heizkreis Itemlists
MODBUS_HZ2_ITEMS: list = []
for index, item in enumerate(iterable=MODBUS_HZ_ITEMS):
    mbi = copy.deepcopy(x=item)
    mbi.address = item.address+100
    mbi.name = item.name + "2"
    mbi.translation_key = item.translation_key + "2"
    mbi.device = DEVICES.HZ2
    MODBUS_HZ2_ITEMS.append(mbi)  # noqa: PERF401

# buils other Heizkreis Itemlists
MODBUS_HZ3_ITEMS: list = []
for index, item in enumerate(iterable=MODBUS_HZ_ITEMS):
    mbi = copy.deepcopy(x=item)
    mbi.address = item.address+200
    mbi.name = item.name + "3"
    mbi.translation_key = item.translation_key + "3"
    mbi.device = DEVICES.HZ3
    MODBUS_HZ3_ITEMS.append(mbi)  # noqa: PERF401

# buils other Heizkreis Itemlists
MODBUS_HZ4_ITEMS: list = []
for index, item in enumerate(iterable=MODBUS_HZ_ITEMS):
    mbi = copy.deepcopy(x=item)
    mbi.address = item.address+300
    mbi.name = item.name + "4"
    mbi.translation_key = item.translation_key + "4"
    mbi.device = DEVICES.HZ4
    MODBUS_HZ4_ITEMS.append(mbi)  # noqa: PERF401

# buils other Heizkreis Itemlists
MODBUS_HZ5_ITEMS: list = []
for index, item in enumerate(iterable=MODBUS_HZ_ITEMS):
    mbi: ModbusItem = copy.deepcopy(x=item)
    mbi.address = item.address+400
    mbi.name = item.name + "5"
    mbi.translation_key = item.translation_key + "5"
    mbi.device = DEVICES.HZ5
    MODBUS_HZ5_ITEMS.append(mbi)  # noqa: PERF401

MODBUS_WW_ITEMS: list[ModbusItem] = [
    ModbusItem( address=32101, name="Warmwassersolltemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.WW, resultlist=TEMPRANGE_WATER, translation_key="ww_soll_temp"),
    ModbusItem( address=32102, name="Warmwassertemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.SENSOR, device=DEVICES.WW, resultlist=TEMPRANGE_WATER, translation_key="ww_temp"),
    ModbusItem( address=42101, name="WW_Konfiguration", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.WW, resultlist=WW_KONFIGURATION, translation_key="ww_konf"),
    ModbusItem( address=42102, name="Warmwasser Push", mformat=FORMATS.STATUS, mtype=TYPES.SELECT, device=DEVICES.WW, resultlist=WW_PUSH, translation_key="ww_push"),
    ModbusItem( address=42103, name="Warmwasser Normal", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.WW, resultlist=TEMPRANGE_WATER, translation_key="ww_normal"),
    ModbusItem( address=42104, name="Warmwasser Absenk", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.WW, resultlist=TEMPRANGE_WATER, translation_key="ww_absenk"),
    ModbusItem( address=42105, name="SG Ready Anhebung", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.WW, resultlist=TEMPRANGE_SGREADY, translation_key="sgr_anhebung"),
] # noqa: E501

MODBUS_W2_ITEMS: list[ModbusItem] = [
    ModbusItem( address=34101, name="Status 2. WEZ", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.W2, resultlist=W2_STATUS, translation_key="status_2_wez"),
    ModbusItem( address=34102, name="Schaltspiele E-Heizung 1", mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.W2, translation_key="schaltsp_e1"),
    ModbusItem( address=34103, name="Betriebsstunden E1", mformat=FORMATS.TIME_H, mtype=TYPES.SENSOR, device=DEVICES.W2, translation_key="betriebss_e1"),
    ModbusItem( address=34104, name="Status E-Heizung 1", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.W2, resultlist=W2_STATUS, translation_key="status_e1"),
    ModbusItem( address=34105, name="Status E-Heizung 2", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.W2, resultlist=W2_STATUS, translation_key="status_e2"),
    ModbusItem( address=34106, name="Schaltspiele E-Heizung 2", mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.W2, translation_key="schaltsp_e2"),
    ModbusItem( address=34107, name="Betriebsstunden E2", mformat=FORMATS.TIME_H, mtype=TYPES.SENSOR, device=DEVICES.W2, translation_key="betriebss_e2"),
    ModbusItem( address=44101, name="W2_Konfiguration", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.W2, resultlist=W2_KONFIG, translation_key="w2_konf"),
    ModbusItem( address=44102, name="Grenztemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.W2, resultlist=TEMPRANGE_BIVALENZ, translation_key="grenztemp"),
    ModbusItem( address=44103, name="Bivalenztemperatur", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.W2, resultlist=TEMPRANGE_BIVALENZ, translation_key="bivalenztemp"),
    ModbusItem( address=44104, name="Bivalenztemperatur WW", mformat=FORMATS.TEMPERATUR, mtype=TYPES.NUMBER, device=DEVICES.W2, resultlist=TEMPRANGE_BIVALENZ, translation_key="bivalenztemp_ww"),
] # noqa: E501

MODBUS_ST_ITEMS: list[ModbusItem] = [
    ModbusItem( address=36101, name="Gesamt Energie heute", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ges_energie_heute"),
    ModbusItem( address=36102, name="Gesamt Energie gestern", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ges_energie_gestern"),
    ModbusItem( address=36103, name="Gesamt Energie Monat", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ges_energie_monat"),
    ModbusItem( address=36104, name="Gesamt Energie Jahr", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ges_energie_jahr"),
    ModbusItem( address=36201, name="Heizen Energie heute", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="heiz_energie_heute"),
    ModbusItem( address=36202, name="Heizen Energie gestern", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="heiz_energie_getern"),
    ModbusItem( address=36203, name="Heizen Energie Monat", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="heiz_energie_monat"),
    ModbusItem( address=36204, name="Heizen Energie Jahr", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="heiz_energie_jahr"),
    ModbusItem( address=36301, name="Warmwasser Energie heute", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ww_energie_heute"),
    ModbusItem( address=36302, name="Warmwasser Energie gestern", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ww_energie_gestern"),
    ModbusItem( address=36303, name="Warmwasser Energie Monat", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ww_energie_monat"),
    ModbusItem( address=36304, name="Warmwasser Energie Jahr", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ww_energie_jahr"),
    ModbusItem( address=36401, name="Kühlen Energie heute", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="kuehl_energie_heute"),
    ModbusItem( address=36402, name="Kühlen Energie gestern", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="kuehl_energie_gestern"),
    ModbusItem( address=36403, name="Kühlen Energie Monat", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="kuehl_energie_monat"),
    ModbusItem( address=36404, name="Kühlen Energie Jahr", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="kuehl_energie_jahr"),
    ModbusItem( address=36501, name="Abtauen Energie heute", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="abtau_energie_heute"),
    ModbusItem( address=36502, name="Abtauen Energie gestern", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY,translation_key="abtau_energie_gester"),
    ModbusItem( address=36503, name="Abtauen Energie Monat", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="abtau_energie_monat"),
    ModbusItem( address=36504, name="Abtauen Energie Jahr", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="abtau_energie_jahr"),
    ModbusItem( address=36601, name="Gesamt Energie II heute", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ges_energie_2_heute"),
    ModbusItem( address=36602, name="Gesamt Energie II gestern", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ges_energie_2_gestern"),
    ModbusItem( address=36603, name="Gesamt Energie II Monat", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ges_energie_2_monat"),
    ModbusItem( address=36604, name="Gesamt Energie II Jahr", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="ges_energie_2_Jahr"),
    ModbusItem( address=36701, name="Elektr. Energie heute", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="el_energie_heute"),
    ModbusItem( address=36702, name="Elektr. Energie gestern", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="el_energie_gestern"),
    ModbusItem( address=36703, name="Elektr. Energie Monat", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="el_energie_monat"),
    ModbusItem( address=36704, name="Elektr. Energie Jahr", mformat=FORMATS.ENERGY, mtype=TYPES.SENSOR, device=DEVICES.ST, resultlist=RANGE_ENERGY, translation_key="el_energie_jahr"),
    ModbusItem( address=36801, name="Adr. 36801", mformat=FORMATS.UNKNOWN, mtype=TYPES.SENSOR, device=DEVICES.ST, translation_key="adr36801"),
] # noqa: E501


MODBUS_IO_ITEMS: list[ModbusItem] = [
    ModbusItem( address=35101, name="SG-Ready 1", mformat=FORMATS.UNKNOWN, mtype=TYPES.SENSOR, device=DEVICES.IO, translation_key="sgr1"),
    ModbusItem( address=35102, name="SG-Ready 2", mformat=FORMATS.UNKNOWN, mtype=TYPES.SENSOR, device=DEVICES.IO, translation_key="sgr2"),
    ModbusItem( address=35103, name="Ausgang H1.2", mformat=FORMATS.UNKNOWN, mtype=TYPES.SENSOR, device=DEVICES.IO, translation_key="ausg_h12"),
    ModbusItem( address=35104, name="Ausgang H1.3", mformat=FORMATS.UNKNOWN, mtype=TYPES.SENSOR, device=DEVICES.IO, translation_key="ausg_h13"),
    ModbusItem( address=35105, name="Ausgang H1.4", mformat=FORMATS.UNKNOWN, mtype=TYPES.SENSOR, device=DEVICES.IO, translation_key="ausg_h14"),
    ModbusItem( address=35106, name="Ausgang H1.5", mformat=FORMATS.UNKNOWN, mtype=TYPES.SENSOR, device=DEVICES.IO, translation_key="ausg_h15"),
    ModbusItem( address=35107, name="Eingang DE1", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.IO, resultlist=W2_STATUS, translation_key="eing_de1"),
    ModbusItem( address=35108, name="Eingang DE2", mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.IO, resultlist=W2_STATUS, translation_key="eing_de2"),

    ModbusItem( address=45101, name="Konf. Eingang SGR1", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.IO, resultlist=IO_KONFIG_IN, translation_key="konf_eing_sgr1"),
    ModbusItem( address=45102, name="Konf. Eingang SGR2", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.IO, resultlist=IO_KONFIG_IN, translation_key="konf_eing_sgr2"),
    ModbusItem( address=45103, name="Konf. Ausgang H1.2", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.IO, resultlist=IO_KONFIG, translation_key="konf_ausg_h12"),
    ModbusItem( address=45104, name="Konf. Ausgang  H1.3", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.IO, resultlist=IO_KONFIG, translation_key="konf_ausg_h13"),
    ModbusItem( address=45105, name="Konf. Ausgang  H1.4", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.IO, resultlist=IO_KONFIG, translation_key="konf_ausg_h14"),
    ModbusItem( address=45106, name="Konf. Ausgang  H1.5", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.IO, resultlist=IO_KONFIG, translation_key="konf_ausg_h15"),
    ModbusItem( address=45107, name="Konf. Eingang DE1", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.IO, resultlist=IO_KONFIG_IN, translation_key="konf_eing_de1"),
    ModbusItem( address=45108, name="Konf. Eingang DE2", mformat=FORMATS.STATUS, mtype=TYPES.NUMBER_RO, device=DEVICES.IO, resultlist=IO_KONFIG_IN, translation_key="konf_eing_de2"),
] # noqa: E501

DEVICELISTS: list = [
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
