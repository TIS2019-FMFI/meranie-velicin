scale = {
    '00': '', '40': 'm', '20': 'k', '10': 'M', '80': '\u03BC',
    '04': 'DIODE', '02': 'DUTY Hz'}

all_units = {
    '20': 'Ohm',  # odpor
    '40': 'A',  # prud
    '80': 'V',  # napatie
    '01': 'F',  # teplota F
    '02': 'C',  # teplota C
    '08': 'Hz',  # frekvencia
    '10': 'hFE'  # tranzistor (current gain)
}


class Parser:
    # https://github.com/drahoslavzan/ProsKit-MT1820-Probe/blob/master/proskit.cc

    def __init__(self):
        self.value = None
        self.units = None

    def parse(self, bytestream):
        """
        podla toho ako to bude posielit ak takto:
        s = ser.read(14) a posleme "s" treba pridat tento riadok
        #bytestream = str(bytestream)
        """
        self.value = \
            int(bytestream[1:2]) * 1000 + \
            int(bytestream[2:3]) * 100 + \
            int(bytestream[3:4]) * 10 + \
            int(bytestream[4:5])
        dic = {0: 1, 1: 1000, 2: 100, 4: 10}
        if str(bytestream[0]) == '-':
            self.value *= -1
        self.value /= dic.get(int(bytestream[6:7]))
        self.units = scale.get((bytestream[9:10].hex()), '')
        if self.units in ['m', 'k', 'M', '\u03BC']:
            # m-milli, k-kilo, M-mega, \u03BC-micro
            dic2 = {'m': 0.001, 'k': 1000, 'M': 1000000, '\u03BC': 0.000001}
            self.value *= dic2.get(self.units)
            self.value = f'{self.value:.5f}'.rstrip('0').rstrip('.')  # format without "e", max. 5 decimal places
            self.units = ""
        self.units += all_units.get((bytestream[10:11].hex()), '')
        # print("parser", self.value, self.units)
        return self.value, self.units
