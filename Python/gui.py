import os
import random
import threading

import wx
import wx.lib.throbber

import farkle

class GUIHumanPlayer(object):
    def query_set_aside(self, remaining, set_aside, turn_score, total_scores):
        print "\n\nScores:\n"
        for i, score in enumerate(total_scores):
            print "Player {0}: {1}".format(i, score)

        print "Turn score: ", turn_score

        print "\nSet Aside:"
        print set_aside.get_values_as_string()

        print "\nYou roll the dice:"
        print remaining.get_values_as_string()

        choices = raw_input("\nIndicate the dice you want to set aside by entering their numbers separated by spaces.\n")

        try:
            return [int(choice) for choice in choices.split()]
        except ValueError:
            return ''

    def query_stop(self, remaining, set_aside, turn_score, total_scores):
        choice = raw_input("You have {0} points.  Hit enter to continue rolling, or type 'stop' to end your turn.\n".format(turn_score))
        if choice == '':
            return False
        else:
            return True

    def warn_invalid_set_aside(self):
        print "That set aside is invalid!"

    def warn_farkle(self, roll):
        print "You got a farkle!"
        print "Dice: " + roll.get_values_as_string()


class MainWindow(wx.Frame):
    def __init__(self, parent, title, num_players):
        wx.Frame.__init__(self, parent, title=title, size=(640,480))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()


        file_menu = wx.Menu()
        menu_new = menu_new.Append(wx.ID_NEW,
                                   "&New",
                                   "Start a new game")
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

        self.Bind(wx.EVT_MENU, self.OnNew, menu_new)
        self.Bind(wx.EVT_MENU, self.OnOpen, menu_open)
        self.Bind(wx.EVT_MENU, self.OnAbout, menu_about)
        self.Bind(wx.EVT_MENU, self.OnExit, menu_exit)

        self.rows_sizer = wx.FlexGridSizer(3, 1)

        self.title_font = wx.Font(18,
                                  wx.FONTFAMILY_SWISS,
                                  wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_NORMAL)
        self.body_font = wx.Font(14,
                                  wx.FONTFAMILY_SWISS,
                                  wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_NORMAL)
        self.title = wx.StaticText(self, label="Scores")
        self.title.SetFont(self.title_font)

        self.scores_sizer = wx.GridSizer(1, num_players)
        self.remaining_sizer = wx.GridSizer(1, 6, vgap=16, hgap=16)
        self.set_aside_sizer = wx.GridSizer(1, 6, vgap=16, hgap=16)
        self.score_labels = [wx.StaticText(self, label="Player " + str(i))
                                for i in range(num_players)]
        for text in self.score_labels:
            text.SetFont(self.body_font)
            self.scores_sizer.Add(text, 0, wx.EXPAND)


        self.dice_images = [wx.Image('die{0}.png'.format(i),
                                     wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                                for i in range(1,7)]

        self.remaining_buttons = []
        for die in self.dice_images:
            btn = wx.BitmapButton(self, -1, die)
            self.remaining_buttons.append(btn)
            self.remaining_sizer.Add(btn)
            self.Bind(wx.EVT_BUTTON, self.OnDiceClicked, btn)

        self.rows_sizer.Add(self.title, 0, wx.EXPAND)
        self.rows_sizer.Add(self.scores_sizer, 0, wx.EXPAND)
        self.rows_sizer.Add(self.remaining_sizer, 0 ,wx.EXPAND)

        self.roll_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.change_roll_images, self.roll_timer)
        self.roll_timer.Start(100)


        self.SetAutoLayout(True)
        self.SetSizer(self.rows_sizer)
        self.Layout()
        self.Show(True)

    def change_roll_images(self, e):
        for btn in self.remaining_buttons:
            btn.SetBitmapLabel(random.choice(self.dice_images))

    def OnDiceClicked(self, e):
        pass

    def OnNew(self, e):
        self.farkle = farkle.Farkle()
        self.farkle.add_player(farkle.HumanPlayer())
        self.farkle.play()
        thread = threading.Thread(target=self.farkle.play(), args=(button,))
        thread.setDaemon(True)
        thread.start()



    def OnOpen(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self,
                            "Choose a file",
                            self.dirname,
                            "",
                            "*.*",
                            wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
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
frame = MainWindow(None, "Hello world", 4)
app.MainLoop()


