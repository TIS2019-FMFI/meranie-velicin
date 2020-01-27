from graph_panel import GraphPanel
from input_panel import InputPanel
from table_panel import TablePanel


class PanelHandler:

    def __init__(self, window, splitter):
        self.window = window
        self.splitter = splitter
        self.panels = []

    def info_panels(self):
        if self.window.input_panel is None:
            self.window.input_panel = InputPanel(self.window.splitter)
        self.clear(True)
        self.add(self.window.input_panel, 360)
        self.add(self.window.buttons)

    def start_panel(self):
        self.add(self.window.buttons)

    def during_measurement_panels(self):
        self.panels[0].Hide()
        self.window.input_panel.clear()
        self.clear()
        self.window.create_table_panel()
        self.add(self.window.buttons, 60)
        self.add(self.window.table_panel, 170)

    def after_panels(self):
        self.clear()
        self.add(self.window.buttons, 55)
        self.add(self.window.table_panel, 170)
        self.window.table_panel.show_scrollbar()

    def graph_panels(self):
        self.clear()
        graph = GraphPanel(self.window.splitter)
        self.add(self.window.buttons, 55)
        self.add(self.window.table_panel, 170)
        self.add(graph, 445)
        graph.draw(self.window.handler.data.values)

    def clear(self, second_measurement=False):
        for panel in self.panels:
            self.splitter.DetachWindow(panel)
            if second_measurement and (isinstance(panel, TablePanel) or isinstance(panel, GraphPanel)):
                panel.Destroy()
        self.panels.clear()

    def add(self, panel, sash_pos=-1):
        self.panels.append(panel)
        self.splitter.AppendWindow(panel, sash_pos)
