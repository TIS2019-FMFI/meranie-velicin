import button_panel
from table import *


class AfterMeasurement:

    def __init__(self, handler, parent):
        self.buttons = button_panel.Buttons(handler, parent.splitter)
        self.grid = Table(parent.splitter, self.buttons)
        self.parent = parent
        parent.panelHandler.clear()
        parent.panelHandler.add(self.buttons)
        parent.panelHandler.add(self.grid)
