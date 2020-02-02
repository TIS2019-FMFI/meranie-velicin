import time
from winsound import Beep
import serial.tools.list_ports
from messagebox import AlertBox
import random


class PipiGraph:

    def __init__(self, values):
        self.port = None
        self.device = self.create_connection()
        self.data = values
        self.min_time = self.data[0][0]
        self.max_time = self.data[-1][0]
        self.mem = dict()
        self.alert = AlertBox()

    def create_connection(self):
        if self.port is not None:
            self.port.close()
        ports = serial.tools.list_ports.comports()
        for device in ports:
            if hex(device.vid) == '0x1a86' and hex(device.pid) == '0x7523':
                try:
                    self.port = serial.Serial(device.device, 9600, timeout=None, parity=serial.PARITY_NONE, rtscts=1)
                    return True
                except serial.serialutil.SerialException:
                    return False
        return False

    def get_time(self, value):
        """
        value from device: 0 - 1023
        """
        return self.min_time + ((self.max_time - self.min_time) * (value / 1023.001))

    def get_value(self, time_unit):
        index = 0
        for i in range(len(self.data)):
            if self.data[i][0] > time_unit:
                break
            index = i
        delta = [self.data[index + 1][0] - self.data[index][0],  # time
                 self.data[index + 1][1][0] - self.data[index][1][0]]  # value
        mlt = (time_unit - self.data[index][0]) / delta[0]
        return round(self.data[index][1][0] + mlt*delta[1], 2)

    def read_values(self):
        """
        reads value from the device and plays tone according to the read value
        """
        while True:
            if self.port is None:
                # self.alert.show('Zariadenie nie je pripojené!')
                return
            s = self.port.read_until(b'\n')
            s = (s.decode("utf-8")).split()
            value = int(s[0])
            if self.mem.get(value) is None:
                tone = self.get_value(self.get_time(value))
                self.mem[value] = tone
            else:
                tone = self.mem[value]
            self.play(tone)
            time.sleep(0.5)

    @staticmethod
    def play(value):
        # values: 0 - 1023
        Beep(500 + int(value), 500)


if __name__ == "__main__":
    val = []
    for i in range(0, 40, 2):
        val.append((i, (random.randint(25, 100), 'C')))
    ppg = PipiGraph(val)
    ppg.read_values()
