import wx

from button_panel import Buttons
from connection import Connection
from measurement_data import *
from panel_handler import PanelHandler
from window import MainWindow
from messagebox import AlertBox


class Handler:

    def __init__(self, main_window):
        self.window = main_window
        self.panel_handler: PanelHandler = None
        self.buttons: Buttons = None
        self.data = MeasurementData()
        self.connection = Connection(self.data, self)
        self.alert = AlertBox()
        self.calls = {'during': self.during, 'cancel': self.cancel, 'after': self.after, 'info': self.info,
                      'save': self.save, 'graph': self.graph, 'export': self.export, 'load': self.load,
                      'main': self.main}

    def handle(self, key, param):
        return self.calls[key](*param)

    def info(self):
        self.buttons.button_handler('info')
        self.panel_handler.handle('info')

    def after(self):
        self.buttons.button_handler('after')
        self.panel_handler.handle('after')

    def graph(self):
        self.buttons.button_handler('graph')
        self.panel_handler.handle('graph')

    def save(self):
        if self.data.pickle():
            pass
        else:
            pass

    def load(self, *args):
        self.window.table_panel = self.panel_handler.create_table_panel()
        self.data = unpickle(args[0])
        for value in self.data.values:
            self.window.table_panel.add(value[0], value[1][0], True)
        self.handle('after', tuple())

    def export(self):
        if self.data.export_to_excel():
            pass
        else:
            pass

    def during(self):
        if self.window.input_panel.correct_values():
            name, interval = self.window.input_panel.user_input
        else:
            return
        self.window.cont_measurement = True
        self.window.update()

        self.data = MeasurementData()
        self.data.file_name = name
        self.connection.data = self.data
        self.connection.interval = float(interval)
        if self.connection.establish_connection():
            self.buttons.button_handler('during')
            self.panel_handler.handle('during')
            self.connection.table = self.window.table_panel
            self.connection.thread = self.connection.create_thread()
            self.connection.thread.start()
        else:
            self.alert.show('Nepodarilo sa vytvoriť spojenie s prístrojom!')
            self.info()

    def cancel(self, error=False):
        if error:
            self.alert.show('Device Error')
        self.connection.kill = True
        self.handle('after', tuple())
        print(self.data.values)

    def main(self):
        self.buttons.button_handler('start')
        self.panel_handler.handle('start')


if __name__ == "__main__":
    app = wx.App()
    window = MainWindow()
    window.create_splitter(Handler(window))
    window.bind_buttons()
    window.Show()
    app.MainLoop()
