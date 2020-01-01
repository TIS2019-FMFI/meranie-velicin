import threading

import wx
from new_measurement import NewMeasurement
from draw_graph import DrawGraph
from after_measurement import AfterMeasurement
from measurement import Measurement
from handler import Handler


class Buttons(wx.Panel):

    end = False

    def __init__(self, parent=None):
        self.handler = Handler()

        wx.Panel.__init__(self, parent=parent)

        self.font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        self.BUTTON_LABELS = ['Zastaviť meranie', 'Nové meranie', 'Zobraziť graf', 'Export do Excelu',
                              'Uložiť meranie', 'Načítať meranie', 'OK']
        func = [self.stop_click, self.new_meas, self.display_graph, self.export, self.save, self.load, self.ok]

        self.parent = parent
        new = wx.ID_ANY
        display = wx.ID_ANY
        export = wx.ID_ANY
        save = wx.ID_ANY
        load = wx.ID_ANY
        self.Bind(wx.EVT_MENU, self.new_meas, id=new)
        self.Bind(wx.EVT_MENU, self.display_graph, id=display)
        self.Bind(wx.EVT_MENU, self.export, id=export)
        self.Bind(wx.EVT_MENU, self.save, id=save)
        self.Bind(wx.EVT_MENU, self.load, id=load)

        self.accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('N'), new),
            (wx.ACCEL_CTRL, ord('G'), display),
            (wx.ACCEL_CTRL, ord('E'), export),
            (wx.ACCEL_CTRL, ord('S'), save),
            (wx.ACCEL_CTRL, ord('L'), load)])
        self.SetAcceleratorTable(self.accel_tbl)

        self.all_buttons = []

        for i in range(len(self.BUTTON_LABELS)):
            b = wx.Button(self, wx.ID_ANY, self.BUTTON_LABELS[i], pos=(10 + 220 * i, 10))
            b.SetFont(self.font)
            b.SetSize(self.calc_size(b))
            b.Bind(wx.EVT_BUTTON, func[i])
            b.Hide()

            self.all_buttons.append(b)

    def get_element_by_id(self, id):
        for e in self.GetChildren():
            if e.Id == id:
                return e
        return None

    def get_button(self, text):
        for e in self.all_buttons:
            if e.GetLabelText() == text:
                return e
        return None

    def show_button(self, text):
        for e in self.all_buttons:
            if e.GetLabelText() == text:
                e.Show()

    def get_buttons(self):
        return self.all_buttons

    @staticmethod
    def calc_size(element, margin=(20, 20)):
        """Vypocita velkost pre element od velkosti FONTU tak,
        aby font nepresahoval velkost tlacidla -> tuple"""

        w, h = element.GetTextExtent(element.GetLabel())
        return w + margin[0], h + margin[1]

    def on_key_pressed(self, event):
        keycode = event.GetKeyCode()
        print('X', keycode)

    def stop_click(self, event):
        pm = AfterMeasurement()
        pm.Show()
        Buttons.end = True

    def new_meas(self, event):
        nm = NewMeasurement()
        nm.Show()

    def display_graph(self, event):
        nm = DrawGraph()
        nm.Show()

    def export(self, event):
        print(event)
        raise ValueError("Treba implementovat")

    def save(self, event):
        print(event)
        raise ValueError("Treba implementovat")

    def load(self, event):
        print(event)
        files = "EXCEL (*.xlsx) |*.xlsx; | Všetky súbory |*"
        with wx.FileDialog(self, "Zvoľte súbor", wildcard=files,
                           style=wx.RESIZE_BORDER | wx.DD_DIR_MUST_EXIST
                           ) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = dialog.GetPath()
            print(path)

        raise ValueError("Treba implementovat")

    def ok(self, event):
        pm = Measurement()
        pm.Show()
        Buttons.end = False
        self.thread = threading.Thread(target=self.manager)
        self.thread.start()

    def manager(self):
        if not self.end:
            self.handler.handle('new_measurement', tuple())
        while not self.end:
            pass
        self.handler.handle('cancel_measurement', tuple())
