import wx


class PanelWindow(wx.Panel):

    def __init__(self, parent, button_panel):
        # super(PanelWindow, self).__init__(parent)
        wx.Panel.__init__(self, parent=parent, pos=wx.DefaultPosition, size=wx.Size(1080, 360))
        self.button_panel = button_panel
        self.parent = parent
        self._all_elements = []
        self.box = wx.BoxSizer(wx.VERTICAL)

        # prida lable a textare-y
        labels = ["názov: ", "interval: "]
        pos_text = [250, 200]
        pos_area = [400, 200]

        for t in labels:
            s1 = wx.StaticText(parent=self, id=wx.ID_ANY, label=t, pos=pos_text)
            s1.SetFont(button_panel.font)

            t1 = wx.TextCtrl(parent=self, id=wx.ID_ANY, value="", pos=pos_area,
                             size=wx.Size(250, 35))
            t1.SetFont(button_panel.font)

            self._all_elements.append(s1)
            self._all_elements.append(t1)

            pos_text[1] += 100
            pos_area[1] += 100

            self.box.Add(s1)
            self.box.Add(t1)

        for e in self._all_elements:
            if type(e) == wx._core.TextCtrl:
                e.SetFocus()
                break

    def add_element(self, ref_class, pos, text=None):
        """Prida prvok ref_class na poziciu pos s textom text.
ref_class je referencia na typ objektu"""
        if text is not None:
            elem = ref_class(self.parent, label=text, pos=pos)
        else:
            elem = ref_class(self.parent, pos=pos)

        self._all_elements.append(elem)
        elem.SetFont(self.button_panel.font)
