import time

from winsound import Beep
import serial


class PipiGraph():

    def __init__(self):
        self.device = self.create_connection()

    def create_connection(self):
        try:
            return serial.Serial('COM4', 9600, timeout=None, parity=serial.PARITY_NONE, rtscts=1)
        except serial.serialutil.SerialException:
            return False

    def play(self, value):
        #values: 0 - 1023
        Beep(500 + value, 500)


if __name__ == "__main__":
    ppg = PipiGraph()
    for i in [10, 30, 50, 70, 50, 30, 10]:
        ppg.play(i)