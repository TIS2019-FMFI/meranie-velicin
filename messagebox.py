import wx


class AlertBox:

    def show(self, text):
        wx.MessageBox(text, 'Upozornenie', wx.OK | wx.ICON_WARNING)
