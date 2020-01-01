from connection import Connection
from measurement_data import MeasurementData


class Handler:

    def __init__(self):
        self.data = MeasurementData()
        self.connection = Connection(self.data)
        self.calls = {'new_measurement': self.read_data, 'cancel_measurement': self.cancel}

    def handle(self, key, param):
        return self.calls[key]()

    def read_data(self):
        Connection.kill = False
        self.connection.thread.start()

    def cancel(self):
        Connection.kill = True
        print(self.connection.thread)
