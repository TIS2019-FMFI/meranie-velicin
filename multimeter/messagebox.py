import wx


class AlertBox:

    @staticmethod
    def show(text):
        wx.MessageBox(text, 'Upozornenie', wx.OK | wx.ICON_WARNING)
