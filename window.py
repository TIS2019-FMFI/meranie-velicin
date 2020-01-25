from splitter import MultiSplitterWindow
import button_panel
import wx
from panel_handler import PanelHandler


class MainWindow(wx.Frame):

    def __init__(self, handler):
        self.visible_objects = []
        wx.Frame.__init__(self, parent=None, title='Multimeter', size=(1080, 720), pos=(243, 56))
        self.splitter = MultiSplitterWindow(self)

        self.handler = handler
        self.handler.window = self
        self.buttons = button_panel.Buttons(self.handler, self.splitter)

        self.table_panel = None
        self.input_panel = None
        self.panel_handler = PanelHandler(self, self.splitter)
        self.buttons.button_handler('start')
        self.panel_handler.handle('start')

        self.splitter.SetOrientation(wx.VERTICAL)

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

        self.accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('N'), new_id),
            (wx.ACCEL_CTRL, ord('G'), display_id),
            (wx.ACCEL_CTRL, ord('E'), export_id),
            (wx.ACCEL_CTRL, ord('S'), save_id),
            (wx.ACCEL_CTRL, ord('L'), load_id),
            (wx.ACCEL_CTRL, ord('Q'), quit_id)])
        self.SetAcceleratorTable(self.accel_tbl)

        self.cont_measurement = True
        self.timer = wx.Timer(self)

        # TODO bind TAB
        # self.Bind(wx.EVT_NAVIGATION_KEY, self.key)

    def update(self):
        self.Bind(wx.EVT_TIMER, self.check)
        self.timer.StartOnce(10)

    def check(self, event):
        if self.cont_measurement:
            self.Bind(wx.EVT_TIMER, self.check)
            self.timer.StartOnce(200)
        else:
            self.handler.cancel()

    def key(self, event):
        print(event)
