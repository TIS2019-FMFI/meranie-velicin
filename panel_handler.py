from graph_panel import GraphPanel
from input_panel import InputPanel
from table_panel import TablePanel


class PanelHandler:

    def __init__(self, window, splitter):
        self.window = window
        self.input = self.window.input_panel
        self.buttons = self.window.buttons
        self.table = self.window.table_panel
        self.splitter = splitter
        self.panels = []

    def info_panels(self):
        self.clear(True)
        if self.input is None:
            self.input = InputPanel(self.splitter)
        self.add((self.input, 360), (self.buttons, -1))
        self.input.focus()

    def start_panel(self):
        self.add((self.buttons, -1))

    def during_measurement_panels(self):
        self.add((self.buttons, 60), (self.table, 170))

    def after_panels(self):
        self.clear()
        self.add((self.buttons, 55), (self.table, 170))
        self.table.show_scrollbar()

    def graph_panels(self):
        self.clear()
        graph = GraphPanel(self.splitter, self.window.handler.data.values)
        self.add((self.buttons, 55), (self.table, 170), (graph, 445))

    def clear(self, second_measurement=False):
        for panel in self.panels:
            self.splitter.DetachWindow(panel)
            if second_measurement and (isinstance(panel, TablePanel) or isinstance(panel, GraphPanel)):
                self.window.create_table_panel()
                panel.Destroy()
        self.panels.clear()

    def add(self, *args):
        for panel, sash_pos in args:
            self.panels.append(panel)
            self.splitter.AppendWindow(panel, sash_pos)

    def before_connection(self):
        self.panels[0].Hide()
        self.clear()
