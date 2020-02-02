from input_panel import InputPanel
from splitter import MultiSplitterWindow
from button_panel import ButtonPanel
import wx
from table_panel import TablePanel
from handler import Handler


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Multimeter', size=(1080, 720), pos=(243, 56))
        self.splitter = MultiSplitterWindow(self)
        self.splitter.SetOrientation(wx.VERTICAL)

        self.buttons = ButtonPanel(self.splitter)
        self.table_panel = TablePanel(self.splitter, self.buttons)
        self.input_panel = InputPanel(self.splitter)
        self.table_panel.Hide()
        self.input_panel.Hide()
        self.panel_handler = None
        self.handler = Handler(self)
        self.buttons.handler = self.handler

        self.cont_measurement = True
        self.timer = wx.Timer(self)

        self.bind_buttons()

        self.buttons.get_button('Zastaviť meranie').Bind(wx.EVT_KILL_FOCUS, self.to_grid)
        self.buttons.get_button('Načítať meranie').Bind(wx.EVT_KILL_FOCUS, self.to_grid)

    def bind_buttons(self):
        new_id = 1
        display_id = 2
        export_id = 3
        save_id = 4
        load_id = 5
        quit_id = 6
        read_id = 7

        self.Bind(wx.EVT_MENU, self.buttons.info, id=new_id)
        self.Bind(wx.EVT_MENU, self.buttons.graph, id=display_id)
        self.Bind(wx.EVT_MENU, self.buttons.export, id=export_id)
        self.Bind(wx.EVT_MENU, self.buttons.save, id=save_id)
        self.Bind(wx.EVT_MENU, self.buttons.load, id=load_id)
        self.Bind(wx.EVT_MENU, self.buttons.stop, id=quit_id)
        self.Bind(wx.EVT_MENU, self.read, id=read_id)

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('N'), new_id),
            (wx.ACCEL_CTRL, ord('G'), display_id),
            (wx.ACCEL_CTRL, ord('E'), export_id),
            (wx.ACCEL_CTRL, ord('S'), save_id),
            (wx.ACCEL_CTRL, ord('L'), load_id),
            (wx.ACCEL_CTRL, ord('Q'), quit_id),
            (wx.ACCEL_CTRL, ord('R'), read_id),
        ])
        self.SetAcceleratorTable(accel_tbl)

    def read(self, event):
        if self.table_panel is not None and self.cont_measurement:
            self.table_panel.read_last(event)

    def update(self):
        self.Bind(wx.EVT_TIMER, self.check)
        self.timer.StartOnce(10)

    def check(self, event):
        if self.cont_measurement:
            self.Bind(wx.EVT_TIMER, self.check)
            self.timer.StartOnce(200)
        else:
            self.handler.cancel(True)

    def key(self, event):
        print(event)

    def create_table_panel(self):
        self.table_panel = TablePanel(self.splitter, self.buttons)
        self.table_panel.Hide()
        self.panel_handler.table = self.table_panel

    def to_grid(self, event):
        if self.cont_measurement and len(self.buttons.get_visible()) > 0:
            self.buttons.get_visible()[0].SetFocus()
            return
        if isinstance(self.FindFocus(), type(self.table_panel.grid)):
            self.table_panel.grid.SetGridCursor(1, 0)
            self.table_panel.grid.MakeCellVisible(1, 0)
