import button_panel
from table import *


class Measurement:

    def __init__(self, handler, parent, measurement_data):
        self.parent = parent
        self.kill = False
        self.handler = handler
        self.measurement_data = measurement_data

        self.buttons = button_panel.Buttons(handler, parent.splitter)
        self.table_panel = Table(parent.splitter, self.buttons)
        parent.panelHandler.clear()
        parent.panelHandler.add(self.buttons, 100)
        parent.panelHandler.add(self.table_panel)
