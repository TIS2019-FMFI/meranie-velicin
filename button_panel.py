import wx


class Buttons(wx.Panel):

    def __init__(self, handler, parent=None):
        wx.Panel.__init__(self, parent=parent)

        self.handler = handler

        self.font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        self.BUTTON_LABELS = ['Zastaviť meranie', 'Nové meranie', 'Zobraziť graf', 'Export do Excelu',
                              'Uložiť meranie', 'Načítať meranie', 'OK']
        self.func = [self.stop_click, self.new_meas, self.display_graph, self.export, self.save, self.load, self.ok]

        newId = 1
        displayId = 2
        exportId = 3
        saveId = 4
        loadId = 5
        quitId = 6
        self.Bind(wx.EVT_MENU, self.new_meas, id=newId)
        self.Bind(wx.EVT_MENU, self.display_graph, id=displayId)
        self.Bind(wx.EVT_MENU, self.export, id=exportId)
        self.Bind(wx.EVT_MENU, self.save, id=saveId)
        self.Bind(wx.EVT_MENU, self.load, id=loadId)
        self.Bind(wx.EVT_MENU, self.stop_click, id=quitId)

        self.accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('N'), newId),
            (wx.ACCEL_CTRL, ord('G'), displayId),
            (wx.ACCEL_CTRL, ord('E'), exportId),
            (wx.ACCEL_CTRL, ord('S'), saveId),
            (wx.ACCEL_CTRL, ord('L'), loadId),
            (wx.ACCEL_CTRL, ord('Q'), quitId)])
        self.SetAcceleratorTable(self.accel_tbl)

        self.all_buttons = []

        self.set_buttons()

    def set_buttons(self):
        for i in range(len(self.BUTTON_LABELS)):
            b = wx.Button(self, wx.ID_ANY, self.BUTTON_LABELS[i], pos=(10 + 220 * i, 10))
            b.SetFont(self.font)
            b.SetSize(self.calc_size(b))
            b.Bind(wx.EVT_BUTTON, self.func[i])
            b.Hide()

            self.all_buttons.append(b)

    def get_element_by_id(self, element_id):
        for e in self.GetChildren():
            if e.Id == element_id:
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

    @staticmethod
    def on_key_pressed(event):
        keycode = event.GetKeyCode()
        print('X', keycode)

    def load(self, event):
        files = "Pickle (*.pickle) |*.pickle; | Všetky súbory |*"
        with wx.FileDialog(self, "Zvoľte súbor", wildcard=files,
                           style=wx.RESIZE_BORDER | wx.DD_DIR_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.handler.handle('load', (dialog.GetPath(), ))

    def new_meas(self, event):
        #self.parent.Hide()
        self.handler.handle('new_measurement_window', tuple())

    def ok(self, event):
        self.handler.handle('start_threads', tuple())

    def stop_click(self, event):
        self.handler.handle('after_window', tuple())

    def save(self, event):
        # TODO inform user about result of saving data (saved/error)
        if self.handler.handle('save', tuple()):
            pass
        else:
            pass

    def export(self, event):
        self.handler.handle('export', tuple())

    def display_graph(self, event):
        self.handler.handle('show_graph', tuple())
