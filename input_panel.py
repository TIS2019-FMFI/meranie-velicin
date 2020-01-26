import wx
from messagebox import AlertBox


class InputPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, pos=wx.DefaultPosition, size=wx.Size(1080, 360))
        self.font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.all_elements = []
        self.box = wx.BoxSizer(wx.VERTICAL)

        self.place_elements()

        for element in self.all_elements:
            self.box.Add(element)
            element.SetFont(self.font)
        self.all_elements[1].SetFocus()

        self.user_input = []
        self.alert = AlertBox()

    def place_elements(self):
        labels = ['názov:', 'interval:']
        text_position = [250, 200]
        field_position = [400, 200]

        for label in labels:
            text = wx.StaticText(parent=self, id=wx.ID_ANY, label=label, pos=text_position)
            input_field = wx.TextCtrl(parent=self, id=wx.ID_ANY, value='', pos=field_position, size=(250, 35))

            self.all_elements.append(text)
            self.all_elements.append(input_field)

            text_position[1] += 100
            field_position[1] += 100

    def correct_values(self):
        self.user_input.clear()
        self.user_input.append(self.all_elements[1].GetValue())
        self.user_input.append(self.all_elements[3].GetValue().replace(',', '.'))
        if len(self.user_input[0]) == 0:
            self.alert.show('Názov merania nebol zadaný!')
            self.all_elements[1].SetFocus()
            return False
        try:
            float(self.user_input[1])
            return True
        except ValueError:
            self.alert.show('Nesprávne zadaný interval merania!')
            self.all_elements[3].SetFocus()
            self.all_elements[3].Clear()
            return False

    def clear(self):
        self.user_input.clear()
        self.all_elements[1].Clear()
        self.all_elements[3].Clear()
