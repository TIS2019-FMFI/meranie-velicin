import wx


class ButtonPanel(wx.Panel):

    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent=parent)

        self.handler = None

        self.font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        self.button_labels = ['Zastaviť meranie', 'Nové meranie', 'Zobraziť graf', 'Export do Excelu',
                              'Uložiť meranie', 'Načítať meranie', 'OK']
        self.functions = [self.stop, self.info, self.graph, self.export, self.save, self.load,
                          self.start]

        self.all_buttons = []

        self.set_buttons()

        self.window_type = None

    def set_buttons(self):
        for i in range(len(self.button_labels)):
            button = wx.Button(self, wx.ID_ANY, self.button_labels[i], pos=(10 + 220 * i, 10))
            button.SetFont(self.font)
            button.SetSize(self.calc_size(button))
            button.Bind(wx.EVT_BUTTON, self.functions[i])
            button.Hide()

            self.all_buttons.append(button)

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
    def calc_size(element):
        margin = (20, 20)
        w, h = element.GetTextExtent(element.GetLabel())
        return w + margin[0], h + margin[1]

    def load(self, event):
        if self.window_type in ['start', 'after', 'graph']:
            directory = r'data'
            files = "Pickle (*.pickle) |*.pickle; | Všetky súbory |*"
            with wx.FileDialog(self, "Zvoľte súbor", wildcard=files, defaultDir=directory,
                               style=wx.RESIZE_BORDER | wx.DD_DIR_MUST_EXIST) as dialog:
                if dialog.ShowModal() == wx.ID_CANCEL:
                    return
                self.handler.handle('load', (dialog.GetPath(),))

    def info(self, event):
        if self.window_type in ['start', 'after', 'graph']:
            self.handler.handle('info', tuple())

    def start(self, event):
        if self.window_type in ['info']:
            self.handler.handle('during', tuple())

    def stop(self, event):
        if self.window_type in ['during']:
            self.handler.handle('cancel', tuple())

    def save(self, event):
        if self.window_type in ['after', 'graph']:
            self.handler.handle('save', tuple())

    def export(self, event):
        if self.window_type in ['after', 'graph']:
            self.handler.handle('export', tuple())

    def graph(self, event):
        if self.window_type in ['after']:
            self.handler.handle('graph', tuple())

    def button_handler(self, window):
        methods = {'info': self.measurement_info_buttons, 'start': self.start_buttons,
                   'during': self.during_measurement_buttons, 'graph': self.graph_buttons,
                   'after': self.after_measurement_buttons}
        self.hide_all()
        self.window_type = window
        methods[window]()
        self.get_visible()

    def get_visible(self):
        for button in self.all_buttons:
            if button.Shown:
                self.handler.window.visible_objects.append(button)

    def hide_all(self):
        for button in self.all_buttons:
            button.Hide()

    def measurement_info_buttons(self):
        self.hide_all()
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
