import wx
from connection import Connection
from measurement_data import *
from window import MainWindow


class Handler:

    def __init__(self):
        self.window = None
        self.measurement_window = None
        self.data = MeasurementData()
        self.connection = Connection(self.data, self)
        self.calls = {'during': self.during, 'cancel': self.cancel, 'after': self.after, 'info': self.info,
                      'save': self.save, 'graph': self.graph, 'export': self.export, 'load': self.load}

    def handle(self, key, param):
        return self.calls[key](*param)

    def info(self):
        self.window.buttons.button_handler('info')
        self.window.panel_handler.handle('info')

    def after(self):
        self.window.buttons.button_handler('after')
        self.window.panel_handler.handle('after')

    def graph(self):
        self.window.buttons.button_handler('graph')
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

    def during(self):
        name, interval = self.window.input_panel.get_txt()
        self.window.cont_measurement = True
        self.window.update()
        self.window.buttons.button_handler('during')
        self.window.panel_handler.handle('during')
        self.data = MeasurementData()
        self.connection.data = self.data
        self.connection.interval = 1
        self.connection.table = self.window.table_panel
        if self.connection.establish_connection():
            self.connection.thread = self.connection.create_thread()
            self.connection.thread.start()
        else:
            self.cancel()

    def cancel(self):
        self.connection.kill = True
        self.handle('after', tuple())
        print(self.data.values)


if __name__ == "__main__":
    app = wx.App()
    window = MainWindow(Handler())
    window.Show()
    app.MainLoop()
