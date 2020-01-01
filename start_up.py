import button_panel
import wx


class Start(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Start', size=(1080, 720))

        self.buttons = button_panel.Buttons(self)

        for i in self.buttons.get_buttons():
            if isinstance(i, wx._core.Button):
                if i.GetLabel() == 'Nové meranie':
                    i.SetPosition((250, 300))
                    i.Show()
                elif i.GetLabel() == 'Načítať meranie':
                    i.SetPosition((550, 300))
                    i.Show()


if __name__ == "__main__":
    app = wx.App()
    start = Start()
    start.Show()
    app.MainLoop()
