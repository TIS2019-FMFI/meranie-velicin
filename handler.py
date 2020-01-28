from connection import Connection
from measurement_data import *
from panel_handler import PanelHandler
from messagebox import AlertBox


class Handler:

    def __init__(self, main_window):
        self.window = main_window
        self.panel_handler = PanelHandler(self.window, self.window.splitter)
        self.window.panel_handler = self.panel_handler
        self.buttons = self.window.buttons
        self.data = MeasurementData()
        self.connection = Connection(self.data, self)
        self.alert = AlertBox()

    def info(self):
        self.buttons.input_buttons()
        self.panel_handler.info_panels()

    def after(self):
        self.buttons.after_buttons()
        self.panel_handler.after_panels()

    def graph(self):
        self.buttons.graph_buttons()
        self.panel_handler.graph_panels()

    def save(self):
        if self.data.pickle():
            self.alert.show('Meranie bolo uložené!')
        else:
            self.alert.show('Meranie sa nepodarilo uložiť!')

    def load(self, *args):
        self.panel_handler.clear(True)
        self.window.create_table_panel()
        self.data = unpickle(args[0])
        for value in self.data.values:
            self.window.table_panel.add(value[0], value[1][0], True)
        self.after()

    def export(self):
        if self.data.export_to_excel():
            self.alert.show('Údaje boli exportované do excelu!')
        else:
            self.alert.show('Údaje sa nepodarilo exportovať!')

    def during(self):
        if self.window.input_panel.correct_values():
            name, interval = self.window.input_panel.user_input
            interval = float(interval)
            self.window.input_panel.clear()
        else:
            return
        self.window.cont_measurement = True
        self.window.update()

        self.data.clear()
        self.data.file_name = name
        self.connection.data = self.data
        self.connection.interval = interval
        self.data.interval = interval
        self.panel_handler.before_connection()
        if self.connection.establish_connection():
            self.buttons.during_buttons()
            self.panel_handler.during_measurement_panels()
            self.connection.table = self.panel_handler.table
            self.connection.thread = self.connection.create_thread()
            self.connection.thread.start()
        else:
            self.alert.show('Nepodarilo sa vytvoriť spojenie s prístrojom!')
            self.info()

    def cancel(self, error=False):
        if error:
            self.alert.show('Device Error')
        self.connection.kill = True
        self.after()
        print(self.data.values)

    def main(self):
        self.buttons.start_buttons()
        self.panel_handler.start_panel()
