import os

import wx

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200,100))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()

        file_menu = wx.Menu()
        menu_open = file_menu.Append(wx.ID_OPEN,
                                     "&Open",
                                     "Load a file")

        file_menu.AppendSeparator()

        menu_about = file_menu.Append(wx.ID_ABOUT,
                                      "&About",
                                      "Information about this program")

        file_menu.AppendSeparator()

        menu_exit = file_menu.Append(wx.ID_EXIT,
                                     "E&xit",
                                     "Terminate the program")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.OnOpen, menu_open)
        self.Bind(wx.EVT_MENU, self.OnAbout, menu_about)
        self.Bind(wx.EVT_MENU, self.OnExit, menu_exit)

        self.Show(True)

    def OnOpen(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self,
                            "Choose a file",
                            self.dirname,
                            "",
                            "*.*",
                            wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.fiilename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "body", "title", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        self.Close(True)

app = wx.App(False)
frame = MainWindow(None, "Hello world")
app.MainLoop()


