import wx


class Buttons(wx.Panel):
    def __init__(self, parent, label="Meranie", res=(1080,720)):
        wx.Panel.__init__(self, parent = parent)
        self.font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL)
 
        self.BUTTON_LABELS = ['Zastaviť meranie', 'Nové meranie', 'Zobraziť graf', 'Export do Excelu', \
                   'Uložiť meranie', 'Načítať meranie', 'OK']
        func = [self.stop_click, self.new_meas, self.display_graph, self.export, self.save, self.load, self.OK]


        self.parent = parent
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
 
        self.accel_tbl = wx.AcceleratorTable([\
            (wx.ACCEL_CTRL, ord('N'), newId),
            (wx.ACCEL_CTRL, ord('G'), displayId),
            (wx.ACCEL_CTRL, ord('E'), exportId),
            (wx.ACCEL_CTRL, ord('S'), saveId),
            (wx.ACCEL_CTRL, ord('L'), loadId),
            (wx.ACCEL_CTRL, ord('Q'), quitId)])
        self.SetAcceleratorTable(self.accel_tbl)
                                                                    

        self.allButtons = []

        for i in range(len(self.BUTTON_LABELS)):
            b = wx.Button(self, wx.ID_ANY, self.BUTTON_LABELS[i], pos=(10+220*i,10))
            b.SetFont(self.font)
            b.SetSize(self._calc_size(b))
            b.Bind(wx.EVT_BUTTON, func[i])
            b.Hide()
                                                                                                   
            self.allButtons.append(b)


    def get_element_by_ID(self, ID):
        for e in self.GetChildren():
            if e.Id == ID:
                return e
        return None


    def get_button(self, text):
        for e in self.allButtons:
            if e.GetLabelText() == text:                
                return e
        return None


    def show_button(self, text):
        for e in self.allButtons:
            if e.GetLabelText() == text:
                e.Show()
        
    
    
    def getButtons(self):
        return self.allButtons

        
    def _calc_size(self, element, margin=(20,20)):
        """Vypocita velkost pre element od velkosti FONTU tak,
        aby font nepresahoval velkost tlacidla -> tuple"""
        
        w, h = element.GetTextExtent(element.GetLabel())
        return (w + margin[0], h + margin[1])

    def on_key_pressed(self, event):
        keycode = event.GetKeyCode()
        print('X', keycode)

    def stop_click(self,event):
        from po_merani import Po_Merani
        pm = Po_Merani()
        self.parent.Hide()
        self.parent.Close()
        pm.Show()
        
    def new_meas(self, event):
        from nove_meranie import Nove_Meranie   
        self.parent.Hide()
        nm = Nove_Meranie(parent = None)
        nm.Show()
        self.parent.Close()
        self.sub = nm


    def display_graph(self, event):
        from po_merani_graf import Po_Merani_Graf   
        self.parent.Hide()
        nm = Po_Merani_Graf(parent = None)
        nm.Show()
        self.parent.Close()
        self.sub = nm
        

    def export(self, event):
        print(event)
        raise ValueError("Treba implementovat")

    def save(self, event):
        print(event)
        raise ValueError("Treba implementovat")

    def load(self, event):
        print(event)
        files = "EXCEL (*.xlsx) |*.xlsx; | Všetky súbory |*"
        with wx.FileDialog(self,"Zvoľte súbor",wildcard=files,
                           style=wx.RESIZE_BORDER | wx.DD_DIR_MUST_EXIST
                           ) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            path = dialog.GetPath()
            print(path)
        
        raise ValueError("Treba implementovat")

    def OK(self, event):
        from pocas_merania import Pocas_Merania
        pm = Pocas_Merania()
        self.parent.Hide()
        self.parent.Close()
        pm.Show()


                                                                                                   #vdaka funkcii si vypytam pole
