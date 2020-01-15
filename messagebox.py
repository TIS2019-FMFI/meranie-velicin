import wx

class AlertBox():
    def show(self, text):
         wx.MessageBox(text, 'Upozornenie', wx.OK | wx.ICON_WARNING)


#volanie jednoducho
#   ab = AlertBox()
#   ab.show('lubovolny text')

#volanie cez Bind
#   self.ab = AlertBox()
#   XYButton.Bind(wx.EVT_BUTTON, self.XYfunkcia)
#   def XYfunkcia(self,event):
#        self.ab.show('lubovolny text')
