import button_panel
import wx

from handler import Handler


class Start(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Start', size=(1080, 720), pos=(243, 56))

        self.handler = Handler()
        self.handler.parent_window = self
        self.buttons = button_panel.Buttons(self.handler, parent=self)

        self.buttons.button_handler('start')


if __name__ == "__main__":
    app = wx.App()
    start = Start()
    start.Show()
    app.MainLoop()
