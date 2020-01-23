import wx

from connection import Connection
from measurement_data import *
from start_up import Start


class Handler:

    def __init__(self):
        self.window = None
        self.measurement_window = None
        self.data = MeasurementData()
        self.connection = Connection(self.data, self)
        self.calls = {'new_measurement': self.new_measurement, 'cancel_measurement': self.cancel,
                      'after_window': self.after_window,
                      'new_measurement_window': self.new_measurement_window, 'save': self.save,
                      'show_graph': self.graph_window, 'export': self.export, 'load': self.load}

    def handle(self, key, param):
        return self.calls[key](*param)

    def new_measurement_window(self):
        self.window.panel_handler.handle('new_measurement')

    def after_window(self):
        self.window.panel_handler.handle('after')

    def graph_window(self):
        self.window.panel_handler.handle('graph')

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
        self.window.panel_handler.handle('measurement')
        self.data = MeasurementData()
        self.connection.data = self.data
        self.connection.table = self.window.table_panel
        if self.connection.establish_connection():
            self.connection.thread = self.connection.create_thread()
            self.connection.thread.start()
        else:
            self.cancel()

    def cancel(self):
        self.connection.kill = True
        self.handle('after_window', tuple())
        print(self.data.values)


if __name__ == "__main__":
    app = wx.App()
    start = Start(Handler())
    start.Show()
    app.MainLoop()
