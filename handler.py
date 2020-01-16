from connection import Connection
from measurement_data import *
from measurement import Measurement
from after_measurement import AfterMeasurement
from new_measurement import NewMeasurement
from draw_graph import DrawGraph


class Handler:

    def __init__(self):
        self.parent_window = None
        self.measurement_window = None
        self.data = None
        self.connection = Connection(self.data, self)
        self.calls = {'new_measurement': self.new_measurement, 'cancel_measurement': self.cancel,
                      'after_window': self.after_window,
                      'new_measurement_window': self.new_measurement_window, 'save': self.save,
                      'show_graph': self.graph_window, 'export': self.export, 'load': self.load}

    def handle(self, key, param):
        return self.calls[key](*param)

    def new_measurement_window(self):
        self.parent_window.Close()
        self.parent_window = NewMeasurement(self)
        self.parent_window.buttons.button_handler('new_measurement')
        self.parent_window.Show()
        self.data = MeasurementData()
        self.connection.data = self.data
        self.data.file_name = self.parent_window.get_file_name()

    def after_window(self):
        self.parent_window = AfterMeasurement(self)
        self.parent_window.buttons.button_handler('after_measurement')
        self.parent_window.Show()

    def graph_window(self):
        self.parent_window = DrawGraph(self)
        self.parent_window.buttons.button_handler('graph')
        self.parent_window.Show()

    def save(self):
        if self.data.pickle():
            pass
        else:
            pass

    def load(self, *args):
        self.data = unpickle(args[0])
        print(self.data.values)
        self.handle('after_window', tuple())

    def export(self):
        if self.data.export_to_excel():
            pass
        else:
            pass

    def new_measurement(self):
        self.measurement_window = Measurement(self, self.data)
        self.measurement_window.Show()
        self.parent_window.Close()
        self.parent_window = self.measurement_window
        self.parent_window.buttons.button_handler('during_measurement')
        self.connection.table = self.measurement_window.table_panel
        if self.connection.establish_connection():
            try:
                self.connection.thread.start()
            except RuntimeError:
                self.connection.thread = self.connection.create_thread()
                self.connection.thread.start()
        else:
            self.cancel()

    def cancel(self):
        self.parent_window.Close()
        self.connection.kill = True
        self.handle('after_window', tuple())
        print(self.data.values)
