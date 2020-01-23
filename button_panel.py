import wx


class Buttons(wx.Panel):

    def __init__(self, handler, parent=None):
        wx.Panel.__init__(self, parent=parent)

        self.handler = handler

        self.font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        self.button_labels = ['Zastaviť meranie', 'Nové meranie', 'Zobraziť graf', 'Export do Excelu',
                              'Uložiť meranie', 'Načítať meranie', 'OK']
        self.functions = [self.stop_click, self.new_measurement, self.display_graph, self.export, self.save, self.load,
                          self.start_measurement]
        new_id = 1
        display_id = 2
        export_id = 3
        save_id = 4
        load_id = 5
        quit_id = 6
        self.Bind(wx.EVT_MENU, self.new_measurement, id=new_id)
        self.Bind(wx.EVT_MENU, self.display_graph, id=display_id)
        self.Bind(wx.EVT_MENU, self.export, id=export_id)
        self.Bind(wx.EVT_MENU, self.save, id=save_id)
        self.Bind(wx.EVT_MENU, self.load, id=load_id)
        self.Bind(wx.EVT_MENU, self.stop_click, id=quit_id)

        self.accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('N'), new_id),
            (wx.ACCEL_CTRL, ord('G'), display_id),
            (wx.ACCEL_CTRL, ord('E'), export_id),
            (wx.ACCEL_CTRL, ord('S'), save_id),
            (wx.ACCEL_CTRL, ord('L'), load_id),
            (wx.ACCEL_CTRL, ord('Q'), quit_id)])
        self.SetAcceleratorTable(self.accel_tbl)

        self.all_buttons = []

        self.set_buttons()

    def set_buttons(self):
        for i in range(len(self.button_labels)):
            b = wx.Button(self, wx.ID_ANY, self.button_labels[i], pos=(10 + 220 * i, 10))
            b.SetFont(self.font)
            b.SetSize(self.calc_size(b))
            b.Bind(wx.EVT_BUTTON, self.functions[i])
            b.Hide()

            self.all_buttons.append(b)

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

    def load(self, event):
        directory = r'data'
        files = "Pickle (*.pickle) |*.pickle; | Všetky súbory |*"
        with wx.FileDialog(self, "Zvoľte súbor", wildcard=files, defaultDir=directory,
                           style=wx.RESIZE_BORDER | wx.DD_DIR_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.handler.handle('load', (dialog.GetPath(),))

    def new_measurement(self, event):
        self.handler.handle('new_measurement_window', tuple())

    def start_measurement(self, event):
        self.handler.handle('new_measurement', tuple())

    def stop_click(self, event):
        self.handler.handle('cancel_measurement', tuple())

    def save(self, event):
        self.handler.handle('save', tuple())

    def export(self, event):
        self.handler.handle('export', tuple())

    def display_graph(self, event):
        self.handler.handle('show_graph', tuple())

    def button_handler(self, window):
        methods = {'new_measurement': self.new_measurement_buttons, 'start': self.start_buttons,
                   'during_measurement': self.during_measurement_buttons, 'graph': self.graph_buttons,
                   'after_measurement': self.after_measurement_buttons}
        self.hide_all()
        methods[window]()

    def hide_all(self):
        for button in self.all_buttons:
            button.Hide()

    def new_measurement_buttons(self):
        button = self.get_button('OK')
        button.SetPosition((600, 100))
        button.Show()

    def start_buttons(self):
        load_button = self.get_button('Načítať meranie')
        load_button.SetPosition((550, 300))

        new_measurement_button = self.get_button('Nové meranie')
        new_measurement_button.SetPosition((250, 300))

        new_measurement_button.Show()
        load_button.Show()

    def during_measurement_buttons(self):
        stop_button = self.get_button('Zastaviť meranie')
        stop_button.Show()

    def graph_buttons(self):
        x, y = 0, 0
        gap = 30
        for b in self.get_buttons():
            if b.GetLabel() not in ('Zastaviť meranie', 'Zobraziť graf', 'OK'):
                b.Show()
                b.SetPosition((x, y))
                x += b.GetTextExtent(b.GetLabel()).GetWidth() + gap

    def after_measurement_buttons(self):
        x, y = 0, 0
        gap = 30

        for b in self.get_buttons():
            if b.GetLabel() not in ('Zastaviť meranie', 'OK'):
                b.Show()
                b.SetPosition((x, y))
                x += b.GetTextExtent(b.GetLabel()).GetWidth() + gap
