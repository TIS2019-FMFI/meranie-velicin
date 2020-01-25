from draw_graph import Graph
from input_panel import InputPanel
from table import Table


class PanelHandler:

    def __init__(self, frame, splitter):
        self.frame = frame
        self.splitter = splitter
        self.windows = []
        self.calls = {'start': self.start_panel, 'info': self.measurement_info_panels,
                      'during': self.during_measurement_panels, 'after': self.after_panels,
                      'graph': self.graph_panels}

    def handle(self, method):
        self.calls[method]()

    def measurement_info_panels(self):
        self.frame.input_panel = InputPanel(self.frame.splitter, self.frame.buttons)
        self.clear(True)
        self.add(self.frame.input_panel, 360)
        self.add(self.frame.buttons)

    def start_panel(self):
        self.add(self.frame.buttons)

    def during_measurement_panels(self):
        self.frame.table_panel = Table(self.frame.splitter, self.frame.buttons)
        self.windows[0].Destroy()
        self.clear()
        self.add(self.frame.buttons, 100)
        self.add(self.frame.table_panel, 620)

    def after_panels(self):
        self.clear()
        self.add(self.frame.buttons, 100)
        self.add(self.frame.table_panel, 620)

    def graph_panels(self):
        self.clear()
        graph = Graph(self.frame.splitter)
        self.add(self.frame.buttons, 55)
        self.add(self.frame.table_panel, 170)
        self.add(graph, 495)
        graph.draw(self.frame.handler.data.values)

    def clear(self, second_measurement=False):
        for w in self.windows:
            self.splitter.DetachWindow(w)
            if second_measurement and (isinstance(w, Table) or isinstance(w, Graph)):
                w.Destroy()
        self.windows.clear()

    def add(self, panel, sash_pos=-1):
        self.windows.append(panel)
        self.splitter.AppendWindow(panel, sash_pos)
