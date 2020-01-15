import wx
 
class AlertBox():
    def __init__(self, text):
        self.text = text

    def show(self, event):
         wx.MessageBox(self.text, 'Upozornenie', wx.OK | wx.ICON_WARNING)


#volanie
#   mb = AlertBox('lubovolna hlaska')
#   XYbutton.Bind(wx.EVT_BUTTON, mb.show)
 





