import button_panel
from wx.lib.splitter import MultiSplitterWindow
import wx


class PanelWindow(wx.Panel):

    def __init__(self, parent, button_panel):
        wx.Panel.__init__(self, parent=parent)
        self.button_panel = button_panel
        self.parent = parent
        self._all_elements = []

        # prida lable a textare-y
        labels = ["názov: ", "interval: "]
        pos_text = [250, 200]

        for t in labels:
            self.add_element(wx.StaticText, pos=pos_text, text=t)

            # vypocitaj poziciu
            # x = sirka elementu + x
            # y je rovnake
            pos = [(button_panel.calc_size(self._all_elements[-1])[0] +
                    pos_text[0]), pos_text[1]]

            # posun y
            pos_text[1] += button_panel.calc_size(self._all_elements[-1])[1]

            # pridaj textarea
            self.add_element(wx.TextCtrl, pos=pos)

            # nastav rozmer textfieldu
            last = self._all_elements[-1]
            if type(last) == wx._core.TextCtrl:
                last.SetSize(250, self._all_elements[-2].GetSize()[1])

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


class NewMeasurement(wx.Frame):

    def __init__(self, handler, parent=None):
        wx.Frame.__init__(self, parent=parent, title='Nové meranie', size=(1080, 720), pos=(243, 56))
        splitter = MultiSplitterWindow(self)

        self.buttons = button_panel.Buttons(handler, splitter)

        self.buttons.show_button('OK')
        b = self.buttons.get_button('OK')
        b.SetPosition((600, 400))
        b.Bind(wx.EVT_BUTTON, self.ok)

        panel_window = PanelWindow(splitter, self.buttons)

        splitter.AppendWindow(panel_window)
        splitter.AppendWindow(self.buttons)

    def ok(self, event):
        self.buttons.ok(event)
        self.Hide()

    def get_file_name(self):
        return 'file_test'
