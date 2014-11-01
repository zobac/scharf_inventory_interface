
import wx
import InterfacePanels as ip
import constants as const

class MainFrame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, -1, 'Inventory Interface', size=const.INTERFACE_SIZE)
        self.SetBackgroundColour(const.BACKGROUNDCOLOUR)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        panel = ip.RadioButtonPanel(self)

        self.mainSizer.Add(panel, 0, wx.ALIGN_CENTER)
        self.SetSizer(self.mainSizer)


class App(wx.App):
    def __init__(self, redirect=False, handler = None):

        wx.App.__init__(self, redirect)
        self.frame = MainFrame()
    def OnInit(self):
        return True


if __name__ == '__main__':
    app = App()
    app.frame.Show()
    app.SetTopWindow(app.frame)
    app.MainLoop()