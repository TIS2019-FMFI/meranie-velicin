import wx

from window import MainWindow

if __name__ == "__main__":
    app = wx.App()
    window = MainWindow()
    window.handler.main()
    window.Show()
    app.MainLoop()
