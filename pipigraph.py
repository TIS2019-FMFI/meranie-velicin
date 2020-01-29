import time
from winsound import Beep
import serial
import random


class PipiGraph:

    def __init__(self, values):
        self.device = self.create_connection()
        self.data = []
        for x in values:
            self.data.append((x[0], x[1][0]))
        self.min_time = self.data[0][0]
        self.max_time = self.data[-1][0]

    def create_connection(self):
        try:
            return serial.Serial('COM3', 9600, timeout=None, parity=serial.PARITY_NONE, rtscts=1)
        except serial.serialutil.SerialException:
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
                 self.data[index + 1][1] - self.data[index][1]]  # value
        mlt = (time_unit - self.data[index][0]) / delta[0]
        return round(self.data[index][1] + mlt*delta[1], 2)

    def read_values(self):
        """
        reads value from the device and plays tone according to the read value
        """
        while True:
            s = self.device.read_until(b'\n')
            s = (s.decode("utf-8")).split()
            value = int(s[0])
            tone = self.get_value(self.get_time(value))
            self.play(tone)
            time.sleep(0.5)

    def play(self, value):
        # values: 0 - 1023
        Beep(500 + int(value), 500)


if __name__ == "__main__":
    val = []
    for i in range(0, 40, 2):
        val.append((i, (random.randint(25, 100), 'C')))
    # print(val)
    ppg = PipiGraph(val)
    ppg.read_values()
    # for i in range(1024):
    #     x = ppg.get_time(i)
    #     print(i, ppg.get_value(x))
    # for i in [10, 30, 50, 70, 50, 30, 10]:
    #     ppg.play(i)
    # while True:
    #     print(ppg.device.read(16))
    #     time.sleep(1)
