import time

from winsound import Beep
import serial


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
            return serial.Serial('COM5', 9600, timeout=None, parity=serial.PARITY_NONE, rtscts=1)
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
        return self.data[index][1] + mlt*delta[1]

    def play(self, value):
        # values: 0 - 1023
        Beep(500 + value, 500)


if __name__ == "__main__":
    ppg = PipiGraph()
    # for i in [10, 30, 50, 70, 50, 30, 10]:
    #     ppg.play(i)
    while True:
        print(ppg.device.read(16))
        time.sleep(1)
