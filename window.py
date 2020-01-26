from input_panel import InputPanel
from splitter import MultiSplitterWindow
from button_panel import Buttons
import wx
from panel_handler import PanelHandler
from table import Table


class MainWindow(wx.Frame):

    def __init__(self):
        self.visible_objects = []
        wx.Frame.__init__(self, parent=None, title='Multimeter', size=(1080, 720), pos=(243, 56))
        self.splitter = MultiSplitterWindow(self)

        self.handler = None
        self.buttons: Buttons = None
        self.table_panel: Table = None
        self.input_panel: InputPanel = None
        self.panel_handler: PanelHandler = None

        self.cont_measurement = True
        self.timer = wx.Timer(self)

        # TODO bind TAB
        # self.Bind(wx.EVT_NAVIGATION_KEY, self.key)

    def create_splitter(self, handler):
        self.handler = handler
        self.buttons = Buttons(self.handler, self.splitter)
        self.panel_handler = PanelHandler(self, self.splitter)
        self.splitter.SetOrientation(wx.VERTICAL)

        self.handler.panel_handler = self.panel_handler
        self.handler.buttons = self.buttons
        self.handler.handle('main', tuple())

    def bind_buttons(self):
        new_id = 1
        display_id = 2
        export_id = 3
        save_id = 4
        load_id = 5
        quit_id = 6

        self.Bind(wx.EVT_MENU, self.buttons.info, id=new_id)
        self.Bind(wx.EVT_MENU, self.buttons.graph, id=display_id)
        self.Bind(wx.EVT_MENU, self.buttons.export, id=export_id)
        self.Bind(wx.EVT_MENU, self.buttons.save, id=save_id)
        self.Bind(wx.EVT_MENU, self.buttons.load, id=load_id)
        self.Bind(wx.EVT_MENU, self.buttons.stop, id=quit_id)

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('N'), new_id),
            (wx.ACCEL_CTRL, ord('G'), display_id),
            (wx.ACCEL_CTRL, ord('E'), export_id),
            (wx.ACCEL_CTRL, ord('S'), save_id),
            (wx.ACCEL_CTRL, ord('L'), load_id),
            (wx.ACCEL_CTRL, ord('Q'), quit_id)])
        self.SetAcceleratorTable(accel_tbl)

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
