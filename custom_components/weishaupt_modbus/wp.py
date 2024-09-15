"""Platform for sensor integration."""

from pymodbus.client import ModbusTcpClient as ModbusClient

# import logging

# hp_ip = "10.10.1.225"
# hp_port = 502

# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)
APPID_offset = 100


class heat_pump:
    """Test."""

    def __init__(self, hp_ip, hp_port) -> None:
        """Test."""
        self._ip = hp_ip
        self._port = hp_port
        self.WWP = None

    def connect(self):
        """Test."""
        try:
            self.WWP = ModbusClient(host=self._ip, port=self._port)
            return self.WWP.connected  # noqa: TRY300
        except:  # noqa: E722
            return None

    ##############################################################################################################################
    # Modbus Register List:                                                                                                      #
    # https://docs.google.com/spreadsheets/d/1EZ3QgyB41xaXo4B5CfZe0Pi8KPwzIGzK/edit?gid=1730751621#gid=1730751621                #
    ##############################################################################################################################

    #####################
    #   System          #
    #####################
    @property
    def Sys_Aussentemperatur1(self):
        """Outer Temperature1 - external sensor."""
        try:
            return self.WWP.read_input_registers(30001, slave=1).registers[0] / 10
        except:  # noqa: E722
            return None

    @property
    def Sys_Aussentemperatur2(self):
        """Outer Temperature2 - air inlet temperature."""
        try:
            return self.WWP.read_input_registers(30002, slave=1).registers[0] / 10
        except:  # noqa: E722
            return None

    @property
    def Sys_Fehler(self):
        """Error."""
        try:
            val = self.WWP.read_input_registers(30003, slave=1).registers[0]
            if val == 65535:
                return "kein Fehler"
            return "Fehler: " + val
        except:  # noqa: E722
            return None

    @property
    def Sys_Warnung(self):
        """Warning."""
        try:
            val = self.WWP.read_input_registers(30004, slave=1).registers[0]
            if val == 65535:
                return "keine Warnung"
            return "Warnung: " + val
        except:  # noqa: E722
            return None

    @property
    def Sys_Fehlerfrei(self):
        """Error free."""
        try:
            val = self.WWP.read_input_registers(30005, slave=1).registers[0]
            if val == 0:
                return "Fehler aktiv"
            else:  # noqa: RET505
                return "Störungsfreier Betrieb"
        except:  # noqa: E722
            return None

    @property
    def Sys_Betriebsanzeige(self):  # noqa: C901
        """Energy used today."""
        try:
            val = self.WWP.read_input_registers(30006, slave=1).registers[0]
            match val:
                case 0:
                    return "Undefiniert"
                case 1:
                    return "Relaistest"
                case 2:
                    return "Notaus"
                case 3:
                    return "Diagnose"
                case 4:
                    return "Handbetrieb"
                case 5:
                    return "Handbetrieb Heizen"
                case 6:
                    return "Handbetrieb Kühlen"
                case 7:
                    return "Manueller Abtaubetrieb"
                case 8:
                    return "Abtauen"
                case 9:
                    return "WEZ2"
                case 10:
                    return "EVU_SPERRE"
                case 11:
                    return "SG Tarif"
                case 12:
                    return "SG Maximal"
                case 13:
                    return "Tarifladung"
                case 14:
                    return "Erhöhter Betrieb"
                case 15:
                    return "Standzeit"
                case 16:
                    return "Standbybetrieb"
                case 17:
                    return "Spülbetrieb"
                case 18:
                    return "Frostschutz"
                case 19:
                    return "Heizbetrieb"
                case 20:
                    return "Warmwasserbetrieb"
                case 21:
                    return "Legionellenschutz"
                case 22:
                    return "Umschaltung HZ KU"
                case 23:
                    return "Kühlbetrieb"
                case 24:
                    return "Passive Kühlung"
                case 25:
                    return "Sommerbetrieb"
                case 26:
                    return "Schwimmbad"
                case 27:
                    return "Urlaub"
                case 28:
                    return "Estrich"
                case 29:
                    return "Gesperrt"
                case 30:
                    return "Sperre AT"
                case 31:
                    return "Sperre Sommer"
                case 32:
                    return "Sperre Winter"
                case 33:
                    return "Einsatzgrenze"
                case 34:
                    return "HK Sperre"
                case 35:
                    return "Absenk"
                case 43:
                    return "Ölrückführung"
                case _:
                    return "undefiniert (" + val + ")"                    
        except:  # noqa: E722
            return None

    @property
    def Sys_Betriebsart(self):
        """Energy used today."""
        val = self.WWP.read_holding_registers(40001, slave=1).registers[0]
        match val:
            case 0:
                return "AUTOMATIK"
            case 1:
                return "HEIZEN"
            case 2:
                return "KÜHLEN"
            case 3:
                return "SOMMER"
            case 4:
                return "STANDBY"
            case 5:
                return "2.WEZ"

    @Sys_Betriebsart.setter
    def Sys_Betriebsart(self, value):
        match value:
            case "AUTOMATIK":
                return_value = 0
            case "HEIZEN":
                return_value = 1
            case "KÜHLEN":
                return_value = 2
            case "SOMMER":
                return_value = 3
            case "STANDBY":
                return_value = 4
            case "2.WEZ":
                return_value = 5

        self.WWP.write_register(40001, return_value, slave=1)

    #####################
    #   Heizkreis       #
    #####################
    @property
    def HK_Raumsolltemperatur(self):
        """Raumsolltemperatur."""
        return self.WWP.read_input_registers(31101, slave=1).registers[0] / 10

    @property
    def HK_Raumtemperatur(self):
        """Raumtemperatur."""
        val = self.WWP.read_input_registers(31102, slave=1).registers[0]
        if val == 32768:
            return None
        return val / 10

    @property
    def HK_Raumfeuchte(self):
        """Raumtemperatur."""
        val = self.WWP.read_input_registers(31103, slave=1).registers[0]
        if val == 65535:
            return None
        return val

    @property
    def HK_Vorlaufsolltemperatur(self):
        """HK_Vorlaufsolltemperatur."""
        val = self.WWP.read_input_registers(31104, slave=1).registers[0]
        if val == -32768:
            return -1
        if val == -32767:
            return -2
        return val / 10
        

    @property
    def HK_Vorlauftemperatur(self):
        """HK_Vorlauftemperatur."""
        val = self.WWP.read_input_registers(31105, slave=1).registers[0]
        if val == 32768:
            # Heatpump Vorlauf, wenn HK keinen Vorlaufsensor hat #
            val = self.WWP.read_input_registers(33104, slave=1).registers[0]  
            if val == 32768:
                return None
        return val / 10

    @property
    def HK_Konfiguration(self):
        """Energy used today."""
        val = self.WWP.read_holding_registers(41101, slave=1).registers[0]
        match val:
            case 0:
                return "AUS"
            case 1:
                return "PUMPENKREIS"
            case 2:
                return "MISCHKREIS"
            case 3:
                return "SOLLWERT (PUMPE M1)"

    @property
    def HK_AnforderungTyp(self):
        """Energy used today."""
        val = self.WWP.read_holding_registers(41102, slave=1).registers[0]
        match val:
            case 0:
                return "AUS"
            case 1:
                return "WITTERUNGSGEFÜHRT"
            case 2:
                return "KONSTANT"

    @HK_AnforderungTyp.setter
    # This one is read only?
    def HK_AnforderungTyp(self, value):
        match value:
            case "AUS":
                return_value = 0
            case "WITTERUNGSGEFÜHRT":
                return_value = 1
            case "KONSTANT":
                return_value = 2
        self.WWP.write_register(41102, return_value, slave=1)

    @property
    def HK_Betriebsart(self):
        """Energy used today."""
        val = self.WWP.read_holding_registers(41103, slave=1).registers[0]

        match val:
            case 0:
                return "AUTOMATIK"
            case 1:
                return "KOMFORT"
            case 2:
                return "NORMAL"
            case 3:
                return "ABSENKBETRIEB"
            case 5:
                return "STANDBY"

    @property
    def HK_Pause_Party(self):
        """Energy used today."""

        val = self.WWP.read_holding_registers(41104, slave=1).registers[0]
        match val:
            case 1:
                return "Pause 12.0h"
            case 2:
                return "Pause 11.5h"
            case 3:
                return "Pause 11.0h"
            case 4:
                return "Pause 10.5h"
            case 5:
                return "Pause 10.0h"
            case 6:
                return "Pause 9.5h"
            case 7:
                return "Pause 9.0h"
            case 8:
                return "Pause 8.5h"
            case 9:
                return "Pause 8.0h"
            case 10:
                return "Pause 7.5h"
            case 11:
                return "Pause 7.0h"
            case 12:
                return "Pause 6.5h"
            case 13:
                return "Pause 6.0h"
            case 14:
                return "Pause 5.5h"
            case 15:
                return "Pause 5.0h"
            case 16:
                return "Pause 4.5h"
            case 17:
                return "Pause 4.0h"
            case 18:
                return "Pause 3.5h"
            case 19:
                return "Pause 3.0h"
            case 20:
                return "Pause 2.5h"
            case 21:
                return "Pause 2.0h"
            case 22:
                return "Pause 1.5h"
            case 23:
                return "Pause 1.0h"
            case 24:
                return "Pause 0.5h"
            case 25:
                return "Automatik"
            case 26:
                return "Party 0.5h"
            case 27:
                return "Party 1.0h"
            case 28:
                return "Party 1.5h"
            case 29:
                return "Party 2.0h"
            case 30:
                return "Party 2.5h"
            case 31:
                return "Party 3.0h"
            case 32:
                return "Party 3.5h"
            case 33:
                return "Party 4.0h"
            case 34:
                return "Party 4.5h"
            case 35:
                return "Party 5.0h"
            case 36:
                return "Party 5.5h"
            case 37:
                return "Party 6.0h"
            case 38:
                return "Party 6.5h"
            case 39:
                return "Party 7.0h"
            case 40:
                return "Party 7.5h"
            case 41:
                return "Party 8.0h"
            case 42:
                return "Party 8.5h"
            case 43:
                return "Party 9.0h"
            case 44:
                return "Party 9.5h"
            case 45:
                return "Party 10.0h"
            case 46:
                return "Party 10.5h"
            case 47:
                return "Party 11.0h"
            case 48:
                return "Party 11.5h"
            case 49:
                return "Party 12.0h"

        
        # return self.WWP.read_holding_registers(41104, slave=1).registers[0]
        # val = self.WWP.read_holding_registers(41104, slave=1).registers[0]
        # if val == 25:
        #    return "Automatik"
        # if val < 25:
        #    time = (25 - val) * 0.5
        #    return "Pausenzeit " + time + "h"
        # if val > 25:
        #    time = (val - 25) * 0.5
        #    return "Partyzeit " + val * 0.5 + "h"

    @HK_Pause_Party.setter
    def HK_Pause_Party(self, val):
        # party_pause = val.split(" ")[0]
        # time = val.split(" ")[1]
        # time_value = time[:-1]
        # if party_pause == "Automatik":
        #    return_value = 25
        # if party_pause == "Pausenzeit":
        #    return_value = 25 - (time_value * 0.5)

        # if val == "Partyzeit":
        #    return_value = 25 + (time_value * 0.5)

        # self.WWP.write_register(41104, return_value, slave=1)
        match val:
            case "Pause 12.0h":
                return_value = 1
            case "Pause 11.5h":
                return_value = 2
            case "Pause 11.0h":
                return_value = 3
            case "Pause 10.5h":
                return_value = 4
            case "Pause 10.0h":
                return_value = 5
            case "Pause 9.5h":
                return_value = 6
            case "Pause 9.0h":
                return_value = 7
            case "Pause 8.5h":
                return_value = 8
            case "Pause 8.0h":
                return_value = 9
            case "Pause 7.5h":
                return_value = 10
            case "Pause 7.0h":
                return_value = 11
            case "Pause 6.5h":
                return_value = 12
            case "Pause 6.0h":
                return_value = 13
            case "Pause 5.5h":
                return_value = 14
            case "Pause 5.0h":
                return_value = 15
            case "Pause 4.5h":
                return_value = 16
            case "Pause 4.0h":
                return_value = 17
            case "Pause 3.5h":
                return_value = 18
            case "Pause 3.0h":
                return_value = 19
            case "Pause 2.5h":
                return_value = 20
            case "Pause 2.0h":
                return_value = 21
            case "Pause 1.5h":
                return_value = 22
            case "Pause 1.0h":
                return_value = 23
            case "Pause 0.5h":
                return_value = 24
            case "Automatik":
                return_value = 25
            case "Party 0.5h":
                return_value = 26
            case "Party 1.0h":
                return_value = 27
            case "Party 1.5h":
                return_value = 28
            case "Party 2.0h":
                return_value = 29
            case "Party 2.5h":
                return_value = 30
            case "Party 3.0h":
                return_value = 31
            case "Party 3.5h":
                return_value = 32
            case "Party 4.0h":
                return_value = 33
            case "Party 4.5h":
                return_value = 34
            case "Party 5.0h":
                return_value = 35
            case "Party 5.5h":
                return_value = 36
            case "Party 6.0h":
                return_value = 37
            case "Party 6.5h":
                return_value = 38
            case "Party 7.0h":
                return_value = 39
            case "Party 7.5h":
                return_value = 40
            case "Party 8.0h":
                return_value = 41
            case "Party 8.5h":
                return_value = 42
            case "Party 9.0h":
                return_value = 43
            case "Party 9.5h":
                return_value = 44
            case "Party 10.0h":
                return_value = 45
            case "Party 10.5h":
                return_value = 46
            case "Party 11.0h":
                return_value = 47
            case "Party 11.5h":
                return_value = 48
            case "Party 12.0h":
                return_value = 49
        
        self.WWP.write_register(41104, return_value, slave=1)

    @property
    def HK_RaumSoll_Komfort(self):
        """Test."""
        return self.WWP.read_holding_registers(41105, slave=1).registers[0] / 10

    @HK_RaumSoll_Komfort.setter
    def HK_RaumSoll_Komfort(self, value):
        self.WWP.write_register(41105, value * 10, slave=1)

    @property
    def HK_RaumSoll_Normal(self):
        """Test."""
        return self.WWP.read_holding_registers(41106, slave=1).registers[0] / 10

    @HK_RaumSoll_Normal.setter
    def HK_RaumSoll_Normal(self, value):
        self.WWP.write_register(41106, value * 10, slave=1)

    @property
    def HK_RaumSoll_Absenk(self):
        """Test."""
        return self.WWP.read_holding_registers(41107, slave=1).registers[0] / 10

    @HK_RaumSoll_Absenk.setter
    def HK_RaumSoll_Absenk(self, value):
        self.WWP.write_register(41107, value * 10, slave=1)

    @property
    def HK_Heizkennlinie(self):
        """Test."""
        return self.WWP.read_holding_registers(41108, slave=1).registers[0] / 100

    @HK_Heizkennlinie.setter
    def HK_Heizkennlinie(self, value):
        self.WWP.write_register(41108, int(value * 100), slave=1)

    @property
    def HK_SommerWinterUmschaltung(self):
        """Test."""
        return self.WWP.read_holding_registers(41109, slave=1).registers[0] / 10

    @HK_SommerWinterUmschaltung.setter
    def HK_SommerWinterUmschaltung(self, value):
        self.WWP.write_register(41109, int(value * 10), slave=1)

    #####################
    #   Warm Water      #
    #####################
    @property
    def WW_Soll(self):
        """Temperature of warm-water."""
        return self.WWP.read_input_registers(32101, slave=1).registers[0] / 10

    @property
    def WW_Ist(self):
        """Temperature of warm-water."""
        return self.WWP.read_input_registers(32102, slave=1).registers[0] / 10

    @property
    def WW_Konfiguration(self):
        """WW_Konfiguration."""
        val = self.WWP.read_holding_registers(42101, slave=1).registers[0]

        match val:
            case 0:
                return "AUS"
            case 1:
                return "Umlenkventil"
            case 8:
                return "Pumpe"

    @property
    def WW_Push(self):
        """WW Push."""
        return self.WWP.read_holding_registers(42102, slave=1).registers[0]

    @WW_Push.setter
    def WW_Push(self, value):
        self.WWP.write_register(42102, value, slave=1)

    @property
    def WW_Normal(self):
        """Test."""
        return self.WWP.read_holding_registers(42103, slave=1).registers[0] / 10

    @WW_Normal.setter
    def WW_Normal(self, value):
        self.WWP.write_register(42103, value * 10, slave=1)

    @property
    def WW_Absenk(self):
        """Test."""
        return self.WWP.read_holding_registers(42104, slave=1).registers[0] / 10

    @WW_Absenk.setter
    def WW_Absenk(self, value):
        self.WWP.write_register(42104, value * 10, slave=1)

    @property
    def WW_SGReady(self):
        """Test."""
        return self.WWP.read_holding_registers(42105, slave=1).registers[0]

    @WW_SGReady.setter
    # readonly?
    def WW_SGReady(self, value):
        self.WWP.write_register(42105, value)

    #####################
    #   Heatpump        #
    #####################
    @property
    def Hp_Betrieb(self):  # noqa: C901
        """Energy used today."""
        val = self.WWP.read_input_registers(33101, slave=1).registers[0]
        match val:
            case 0:
                return "Undefiniert"
            case 1:
                return "Relaistest"
            case 2:
                return "Notaus"
            case 3:
                return "Diagnose"
            case 4:
                return "Handbetrieb"
            case 5:
                return "Handbetrieb Heizen"
            case 6:
                return "Handbetrieb Kühlen"
            case 7:
                return "Manueller Abtaubetrieb"
            case 8:
                return "Abtauen"
            case 9:
                return "WEZ2"
            case 10:
                return "EVU_SPERRE"
            case 11:
                return "SG Tarif"
            case 12:
                return "SG Maximal"
            case 13:
                return "Tarifladung"
            case 14:
                return "Erhöhter Betrieb"
            case 15:
                return "Standzeit"
            case 16:
                return "Standbybetrieb"
            case 17:
                return "Spülbetrieb"
            case 18:
                return "Frostschutz"
            case 19:
                return "Heizbetrieb"
            case 20:
                return "Warmwasserbetrieb"
            case 21:
                return "Legionellenschutz"
            case 22:
                return "Umschaltung HZ KU"
            case 23:
                return "Kühlbetrieb"
            case 24:
                return "Passive Kühlung"
            case 25:
                return "Sommerbetrieb"
            case 26:
                return "Schwimmbad"
            case 27:
                return "Urlaub"
            case 28:
                return "Estrich"
            case 29:
                return "Gesperrt"
            case 30:
                return "Sperre AT"
            case 31:
                return "Sperre Sommer"
            case 32:
                return "Sperre Winter"
            case 33:
                return "Einsatzgrenze"
            case 34:
                return "HK Sperre"
            case 35:
                return "Absenk"
            case 43:
                return "Ölrückführung"
            case _:
                return "undefiniert (" + val + ")"
                

    @property
    def Hp_Stoermeldung(self):
        """Energy used today."""
        val = self.WWP.read_input_registers(33102, slave=1).registers[0]
        match val:
            case 0:
                return "Störung"
            case 1:
                return "Störungsfrei"

    @property
    def Hp_Leistungsanforderung(self):
        """Energy used today."""
        return self.WWP.read_input_registers(33103, slave=1).registers[0]

    @property
    def Hp_Vorlauftemperatur(self):
        """Energy used today."""
        return self.WWP.read_input_registers(33104, slave=1).registers[0] / 10

    @property
    def Hp_Ruecklauftemperatur(self):
        """Energy used today."""
        return self.WWP.read_input_registers(33105, slave=1).registers[0] / 10

    #####################
    #   Statistics      #
    #####################
    @property
    def Energy_total_today(self):
        """Total energy used today."""
        return self.WWP.read_input_registers(36101, slave=1).registers[0]

    @property
    def Energy_total_yesterday(self):
        """Total energy used yesterday."""
        return self.WWP.read_input_registers(36102, slave=1).registers[0]

    @property
    def Energy_total_month(self):
        """Total energy used month."""
        return self.WWP.read_input_registers(36103, slave=1).registers[0]

    @property
    def Energy_total_year(self):
        """Total energy used year."""
        return self.WWP.read_input_registers(36104, slave=1).registers[0]

    @property
    def Heating_total_today(self):
        """Energy used for heating today."""
        return self.WWP.read_input_registers(36201, slave=1).registers[0]

    @property
    def Heating_total_yesterday(self):
        """Energy used for heating yesterday."""
        return self.WWP.read_input_registers(36202, slave=1).registers[0]

    @property
    def Heating_total_month(self):
        """Energy used for heating month."""
        return self.WWP.read_input_registers(36203, slave=1).registers[0]

    @property
    def Heating_total_year(self):
        """Energy used for heating year."""
        return self.WWP.read_input_registers(36204, slave=1).registers[0]

    @property
    def Water_total_today(self):
        """Energy used for heating water today."""
        return self.WWP.read_input_registers(36301, slave=1).registers[0]

    @property
    def Water_total_yesterday(self):
        """Energy used for heating water yesterday."""
        return self.WWP.read_input_registers(36302, slave=1).registers[0]

    @property
    def Water_total_month(self):
        """Energy used for heating water month."""
        return self.WWP.read_input_registers(36303, slave=1).registers[0]

    @property
    def Water_total_year(self):
        """Energy used for heating water year."""
        return self.WWP.read_input_registers(36304, slave=1).registers[0]

    @property
    def Cooling_total_today(self):
        """Energy used for cooling today."""
        return self.WWP.read_input_registers(36401, slave=1).registers[0]

    @property
    def Cooling_total_yesterday(self):
        """Energy used for cooling yesterday."""
        return self.WWP.read_input_registers(36402, slave=1).registers[0]

    @property
    def Cooling_total_month(self):
        """Energy used for cooling month."""
        return self.WWP.read_input_registers(36403, slave=1).registers[0]

    @property
    def Cooling_total_year(self):
        """Energy used for cooling year."""
        return self.WWP.read_input_registers(36404, slave=1).registers[0]


# whp = heat_pump(hp_ip, hp_port)
# whp.connect()
# print(whp.WW_Soll)
# whp.WW_Soll = 44
# print(whp.WW_Soll)
# whp.WW_Soll = 45
# print(whp.WW_Soll)

# print(whp.WW_Ist)
