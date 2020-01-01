import time

from connection import Connection
from measurement_data import MeasurementData


class Handler:

    def __init__(self):
        self.data = MeasurementData()
        self.connection = Connection(self.data)
        self.calls = {'new_measurement': self.read_data, 'cancel_measurement': self.cancel}

    def handle(self, key, param):
        return self.calls[key](*param)

    def read_data(self):
        Connection.kill = False
        self.connection.thread.start()

    def cancel(self):
        Connection.kill = True
        print(self.data.values)


if __name__ == '__main__':
    h = Handler()
    h.handle('new_measurement', tuple())
    x = 0
    while x < 5:
        x += 1
        time.sleep(1)
    h.cancel()
