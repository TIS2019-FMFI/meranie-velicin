import threading

from connection import Connection
from measurement_data import *
from measurement import Measurement
from after_measurement import AfterMeasurement
from new_measurement import NewMeasurement
from draw_graph import DrawGraph


class Handler:

    end = False

    def __init__(self):
        self.thread = threading.Thread(target=self.manager)

        self.measurement_window = None
        self.data = MeasurementData()
        self.connection = Connection(self.data)
        self.calls = {'new_measurement': self.new_measurement, 'cancel_measurement': self.cancel,
                      'start_threads': self.start_threads, 'after_window': self.after_window,
                      'new_measurement_window': self.new_measurement_window, 'save': self.save,
                      'show_graph': self.graph_window, 'export': self.export, 'load': self.load}

    def handle(self, key, param):
        return self.calls[key](*param)

    def new_measurement_window(self):
        nm = NewMeasurement(self)
        nm.Show()
        self.data.file_name = nm.get_file_name()

    def after_window(self):
        Handler.end = True
        pm = AfterMeasurement(self)
        pm.Show()

    @staticmethod
    def graph_window():
        nm = DrawGraph()
        nm.Show()

    def start_threads(self):
        self.measurement_window = Measurement(self, self.data)
        self.measurement_window.Show()
        self.thread.start()
        Handler.end = False

    def save(self):
        return self.data.pickle()

    def load(self, *args):
        self.data = unpickle(args[0])
        print(self.data.values)

    def export(self):
        pass

    def new_measurement(self):
        Connection.kill = False
        Measurement.kill = False
        self.measurement_window.thread.start()
        self.connection.thread.start()

    def cancel(self):
        Connection.kill = True
        Measurement.kill = True
        print(self.data.values)

    def manager(self):
        if not self.end:
            self.handle('new_measurement', tuple())
        while not self.end:
            pass
        self.handle('cancel_measurement', tuple())
