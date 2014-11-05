

import wx

import wx.lib.scrolledpanel as scrolled
import constants as const

from TextCtrlAutoComplete import TextCtrlAutoComplete

from dataAccess import DataAccess as da

class RadioButtonPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.SetBackgroundColour(const.BACKGROUNDCOLOUR)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        radioButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        filmButton = wx.RadioButton(self, label="New Film", style=wx.RB_GROUP, name=const.FILM)
        seriesButton = wx.RadioButton(self, label="New Series", name=const.SERIES)
        musicDVDButton = wx.RadioButton(self, label="New Music DVD", name=const.MUSIC_DVD)
        self.radioButtons = [filmButton, seriesButton, musicDVDButton]
        radioButtonSizer.Add(filmButton, 0, wx.ALL, 4)
        radioButtonSizer.Add(seriesButton, 0, wx.ALL, 4)
        radioButtonSizer.Add(musicDVDButton, 0, wx.ALL, 4)

        goButton = wx.Button(self, -1, 'OK!')

        self.Bind(wx.EVT_BUTTON, self.onOK, goButton)

        mainSizer.Add(radioButtonSizer, 0, wx.ALIGN_CENTER)
        mainSizer.Add(goButton, 0, wx.ALIGN_CENTER)
        self.SetSizer(mainSizer)


    def onOK(self, event):
        for button in self.radioButtons:
            if button.GetValue() is True:
                selection = button.GetName()
                break
        if selection == const.FILM:
            panel = FilmPanel(self.Parent, self.Parent.dataAccess)
        elif selection == const.SERIES:
            panel = SeriesPanel(self.Parent, self.Parent.dataAccess)
        else:
            panel = MusicDVDPanel(self.Parent, self.Parent.dataAccess)

        self.Parent.mainSizer.Detach(self)
        self.Parent.mainSizer.Add(panel, 1, wx.EXPAND)
        self.Parent.Layout()
        self.Destroy()



class BasePanel(wx.Panel):

    def __init__(self, parent, dataAccess, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, -1, size=(-1,-1))
        self.SetBackgroundColour(const.BACKGROUNDCOLOUR)
        self.dataAccess = dataAccess
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)


        # Event Bindings

        self.SetSizer(self.mainSizer)

    def createWarningBox(self, message, isOK=False):
        if isOK:
            style = wx.OK
        else:
            style = wx.YES_NO
        dialog = wx.MessageDialog(self, message, style=style)
        result = dialog.ShowModal()
        return result == wx.ID_YES

    def onCancel(self, event):
        self.returnToMainPanel()

    def returnToMainPanel(self):
        self.dataAccess.loadAttrs()
        self.Parent.mainSizer.Detach(self)
        self.Parent.mainSizer.Add(RadioButtonPanel(self.Parent), 0, wx.ALIGN_CENTER)
        self.Parent.Layout()
        self.Destroy()


    def onAddActor(self, event):
            self.Freeze()
            panel = ActorPanel(self.actorPanel)
            self.relatingPanels.append(panel)
            self.actorPanelSizer.Add(panel, 0, wx.ALL|wx.EXPAND, 4)
            self.actorPanel.SetSizer(self.actorPanelSizer)
            self.actorPanel.SetAutoLayout(1)
            self.actorPanel.SetupScrolling()
            self.Thaw()
            event.Skip()

    def onAddCountry(self, event):
        self.Freeze()
        panel = CountryPanel(self.countryPanel)
        self.relatingPanels.append(panel)
        self.countryPanelSizer.Add(panel, 0, wx.ALL|wx.EXPAND, 4)
        self.countryPanel.SetSizer(self.countryPanelSizer)
        self.countryPanel.SetAutoLayout(1)
        self.countryPanel.SetupScrolling()
        self.Thaw()
        event.Skip()

    def isnumber(self, number):

        try:
            float(number)
            return True
        except:
            return False




class MusicDVDPanel(BasePanel):

    def __init__(self, parent, dataAccess):
        BasePanel.__init__(self, parent, dataAccess)

        self.relatingPanels = []

        infoSizer1 = wx.BoxSizer(wx.HORIZONTAL)


        nameStaticBox = wx.StaticBox(self, -1, 'Name')
        nameSizer = wx.StaticBoxSizer(nameStaticBox, wx.HORIZONTAL)
        self.nameBox = wx.TextCtrl(self, -1, size=(200, -1))
        nameSizer.Add(self.nameBox, 0, wx.ALL, 4)

        yearStaticBox = wx.StaticBox(self, -1, 'Year')
        yearSizer = wx.StaticBoxSizer(yearStaticBox, wx.HORIZONTAL)
        self.yearBox = wx.TextCtrl(self, -1, size=(47, -1))
        self.yearBox.SetMaxLength(4)
        yearSizer.Add(self.yearBox, 0, wx.ALL, 4)

        infoSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        formatStaticBox = wx.StaticBox(self, -1, 'Format')
        formatSizer = wx.StaticBoxSizer(formatStaticBox, wx.HORIZONTAL)
        self.formatChoice = wx.Choice(self, -1, choices=self.dataAccess.formats.keys())
        self.formatChoice.SetStringSelection('DVD')
        formatSizer.Add(self.formatChoice, 0, wx.ALL, 4)

        self.artistPanel = scrolled.ScrolledPanel(self, -1, size=(-1, 350))
        self.artistPanel.SetBackgroundColour(const.BACKGROUNDCOLOUR)
        artistPanelStaticBox = wx.StaticBox(self, -1, "artists")
        self.artistPanelStaticBoxSizer = wx.StaticBoxSizer(artistPanelStaticBox, wx.VERTICAL)
        self.artistPanelSizer = wx.BoxSizer(wx.VERTICAL)
        addartistButton = wx.Button(self, -1, 'Add artist')

        self.artistPanelStaticBoxSizer.Add(addartistButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)
        self.artistPanelStaticBoxSizer.Add(self.artistPanel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 4)
        panel = ArtistPanel(self.artistPanel, self.dataAccess)
        self.relatingPanels.append(panel)
        self.artistPanelSizer.Add(panel, 0, wx.ALL|wx.EXPAND, 4)

        self.artistPanel.SetSizer(self.artistPanelSizer)
        self.artistPanel.SetAutoLayout(1)
        self.artistPanel.SetupScrolling()

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        createButton = wx.Button(self, -1, 'Add musicDVD')
        cancelButton = wx.Button(self, -1, 'Cancel')
        buttonSizer.Add(createButton, 0, wx.ALIGN_CENTER|wx.ALIGN_BOTTOM|wx.ALL, 4)
        buttonSizer.Add(cancelButton, 0, wx.ALIGN_CENTER|wx.ALL, 4)

        infoSizer1.Add(nameSizer, 2, wx.ALL, 4)
        infoSizer1.Add(yearSizer, 1, wx.ALL, 4)

        infoSizer2.Add(formatSizer, 1 , wx.ALL, 4)

        self.Bind(wx.EVT_BUTTON, self.onCreate, createButton)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelButton)
        self.Bind(wx.EVT_BUTTON, self.onAddartist, addartistButton)

        self.mainSizer.Add(infoSizer1, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(infoSizer2, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(self.artistPanelStaticBoxSizer, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(buttonSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)

    def onCreate(self, event):

        title = self.nameBox.GetValue()
        if title == "":
            self.createWarningBox("Please type a title for this musicDVD!", True)
            return

        year = self.yearBox.GetValue()
        if not self.isnumber(year) or len(year) < 4:
            self.createWarningBox("Invalid entry for year!", True)
            return

        format = self.dataAccess.formats[self.formatChoice.GetStringSelection()]

        dialogString = "Create musicDVD:%s\nGenre:%s\nYear:%s" %(title,
                                                                 self.formatChoice.GetStringSelection(),
                                                                 year)
        if title in self.dataAccess.getMusicDVDs():
            dialogString += '\nTHIS title IS ALREADY PRESENT IN THE DATABASE'

        dialog = wx.MessageDialog(self, dialogString, style=wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            musicDVDId = self.dataAccess.createMusicDVD(title, year, format)[-1][-1]
            if not musicDVDId:
                self.createWarningBox('Failed to create this musicDVD.', True)

            for panel in self.relatingPanels:
                panel.onCreate(musicDVDId, True)
        else:
            dialog.Destroy()
        event.Skip()


    def onAddartist(self, event):
        self.Freeze()
        panel = ArtistPanel(self.artistPanel, self.dataAccess)
        self.relatingPanels.append(panel)
        self.artistPanelSizer.Add(panel, 0, wx.ALL|wx.EXPAND, 4)
        self.artistPanel.SetSizer(self.artistPanelSizer)
        self.artistPanel.SetAutoLayout(1)
        self.artistPanel.SetupScrolling()
        self.Thaw()
        event.Skip()



class FilmPanel(BasePanel):

    def __init__(self, parent, dataAccess):
        BasePanel.__init__(self, parent, dataAccess)

        self.ignoreEvtText = False

        self.relatingPanels = []

        infoSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        titleStaticBox = wx.StaticBox(self, -1, 'Title')
        titleSizer = wx.StaticBoxSizer(titleStaticBox, wx.HORIZONTAL)
        self.titleBox = wx.TextCtrl(self, -1, size=(200, -1))
        titleSizer.Add(self.titleBox, 0, wx.ALL, 4)

        yearStaticBox = wx.StaticBox(self, -1, 'Year')
        yearSizer = wx.StaticBoxSizer(yearStaticBox, wx.HORIZONTAL)
        self.yearBox = wx.TextCtrl(self, -1, size=(47, -1))
        self.yearBox.SetMaxLength(4)
        yearSizer.Add(self.yearBox, 0, wx.ALL, 4)

        lengthStaticBox = wx.StaticBox(self, -1, 'Length(minutes)', size=(120,-1))
        lengthSizer = wx.StaticBoxSizer(lengthStaticBox, wx.HORIZONTAL)
        self.lengthBox = wx.TextCtrl(self, -1, size=(47, -1))
        self.lengthBox.SetMaxLength(3)
        lengthSizer.Add(self.lengthBox, 0, wx.ALL, 4)

        infoSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.criterionCheckbox = wx.CheckBox(self, -1, 'Criterion Edition')

        formatStaticBox = wx.StaticBox(self, -1, 'Format')
        formatSizer = wx.StaticBoxSizer(formatStaticBox, wx.HORIZONTAL)
        self.formatChoice = wx.Choice(self, -1, choices=self.dataAccess.formats.keys())
        self.formatChoice.SetStringSelection('DVD')
        formatSizer.Add(self.formatChoice, 0, wx.ALL, 4)

        genreStaticBox = wx.StaticBox(self, -1, 'Genre')
        genreSizer = wx.StaticBoxSizer(genreStaticBox, wx.HORIZONTAL)
        self.genreChoice = wx.Choice(self, -1, choices=self.dataAccess.genres.keys())
        genreSizer.Add(self.genreChoice, 0, wx.ALL, 4)

        directorStaticBox = wx.StaticBox(self, -1, 'Director')
        directorStaticBoxSizer = wx.StaticBoxSizer(directorStaticBox, wx.HORIZONTAL)

        directorFNStaticBox = wx.StaticBox(self, -1, "First Name")
        directorFNStaticBoxSizer = wx.StaticBoxSizer(directorFNStaticBox, wx.HORIZONTAL)
        self.directorFNTextCtrl = TextCtrlAutoComplete(self, -1, choices=[key[0] for key in self.dataAccess.directors],size=(200, -1))
        directorFNStaticBoxSizer.Add(self.directorFNTextCtrl, 0, wx.ALL, 4)

        directorLNStaticBox = wx.StaticBox(self, -1, "Last Name")
        directorLNStaticBoxSizer = wx.StaticBoxSizer(directorLNStaticBox, wx.HORIZONTAL)
        self.directorLNTextCtrl = TextCtrlAutoComplete(self, -1,  choices=[key[1] for key in self.dataAccess.directors], size=(200, -1))
        directorLNStaticBoxSizer.Add(self.directorLNTextCtrl, 0, wx.ALL, 4)

        directorStaticBoxSizer.Add(directorFNStaticBoxSizer, 1, wx.ALL, 4)
        directorStaticBoxSizer.Add(directorLNStaticBoxSizer, 1, wx.ALL, 4)

        self.countryPanel = scrolled.ScrolledPanel(self, -1, size=(-1, 125))
        self.countryPanel.SetBackgroundColour(const.BACKGROUNDCOLOUR)
        countryPanelStaticBox = wx.StaticBox(self, -1, "Countries")
        self.countryPanelStaticBoxSizer = wx.StaticBoxSizer(countryPanelStaticBox, wx.VERTICAL)
        self.countryPanelSizer = wx.BoxSizer(wx.VERTICAL)
        addCountryButton = wx.Button(self, -1, 'Add Country')

        self.countryPanelStaticBoxSizer.Add(addCountryButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)
        self.countryPanelStaticBoxSizer.Add(self.countryPanel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 4)
        panel = CountryPanel(self.countryPanel, self.dataAccess)
        self.relatingPanels.append(panel)
        self.countryPanelSizer.Add(panel, 0, wx.ALL|wx.EXPAND, 4)

        self.countryPanel.SetSizer(self.countryPanelSizer)
        self.countryPanel.SetAutoLayout(1)
        self.countryPanel.SetupScrolling()

        self.actorPanel = scrolled.ScrolledPanel(self, -1, size=(-1, 125))
        self.actorPanel.SetBackgroundColour(const.BACKGROUNDCOLOUR)
        actorPanelStaticBox = wx.StaticBox(self, -1, "Actors")
        self.actorPanelStaticBoxSizer = wx.StaticBoxSizer(actorPanelStaticBox, wx.VERTICAL)
        self.actorPanelSizer = wx.BoxSizer(wx.VERTICAL)
        addactorButton = wx.Button(self, -1, 'Add actor')

        self.actorPanelStaticBoxSizer.Add(addactorButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)
        self.actorPanelStaticBoxSizer.Add(self.actorPanel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 4)
        panel = ActorPanel(self.actorPanel, self.dataAccess)
        self.relatingPanels.append(panel)
        self.actorPanelSizer.Add(panel, 0, wx.ALL|wx.EXPAND, 4)

        self.actorPanel.SetSizer(self.actorPanelSizer)
        self.actorPanel.SetAutoLayout(1)
        self.actorPanel.SetupScrolling()

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        createButton = wx.Button(self, -1, 'Add Film')
        cancelButton = wx.Button(self, -1, 'Cancel')
        buttonSizer.Add(createButton, 0, wx.ALIGN_CENTER|wx.ALIGN_BOTTOM|wx.ALL, 4)
        buttonSizer.Add(cancelButton, 0, wx.ALIGN_CENTER|wx.ALL, 4)

        infoSizer1.Add(titleSizer, 2, wx.ALL, 4)
        infoSizer1.Add(yearSizer, 1, wx.ALL, 4)
        infoSizer1.Add(lengthSizer, 1, wx.ALL, 4)

        infoSizer2.Add(self.criterionCheckbox, 0 , wx.ALL, 4)
        infoSizer2.Add(formatSizer, 1 , wx.ALL, 4)
        infoSizer2.Add(genreSizer, 1 , wx.ALL, 4)

        self.Bind(wx.EVT_BUTTON, self.onCreate, createButton)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelButton)
        self.Bind(wx.EVT_BUTTON, self.onAddCountry, addCountryButton)
        self.Bind(wx.EVT_BUTTON, self.onAddActor, addactorButton)

        self.directorFNTextCtrl.Bind(wx.EVT_KILL_FOCUS, self.onDirectorFNKillFocus)

        self.mainSizer.Add(infoSizer1, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(infoSizer2, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(directorStaticBoxSizer, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(self.countryPanelStaticBoxSizer, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(self.actorPanelStaticBoxSizer, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(buttonSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)


    def onDirectorFNKillFocus(self, event):
        text = event.GetEventObject().GetValue()
        for key in self.dataAccess.directors:
            if text == key[0]:
                self.directorLNTextCtrl.SetValue(key[1])
        self.directorLNTextCtrl.SetChoices([key[1] for key in self.dataAccess.directors if text == key[0]])
        event.Skip()


    def onCreate(self, event):

        title = self.titleBox.GetValue()
        if title == "":
            self.createWarningBox("Please type a title for this film!", True)
            return

        year = self.yearBox.GetValue()
        if not self.isnumber(year) or len(year) < 4:
            self.createWarningBox("Invalid entry for year!", True)
            return

        isCriterion = int(self.criterionCheckbox.IsChecked())

        length = self.lengthBox.GetValue()
        if length == '':
            if not self.createWarningBox("You didn't enter a length for this film.\n\nCreate it anyway?"):
                return
            else:
                length = 'NULL'
        elif not self.isnumber(length):
            self.createWarningBox("Invalid entry for length!", True)
            return

        format = self.dataAccess.formats[self.formatChoice.GetStringSelection()]

        genre = self.dataAccess.genres[self.genreChoice.GetStringSelection()]

        director = (self.directorFNTextCtrl.GetValue(), self.directorLNTextCtrl.GetValue())
        if director == ("", ""):
            if not self.createWarningBox("You didn't enter a director for this film.\n\nCreate it anyway?"):
                return
        elif director[0] == '':
            if not self.createWarningBox("You didn't enter a last name for the director of this film.\n\nCreate it anyway?"):
                return
        if not self.dataAccess.checkDirector(director):
            dialog = wx.MessageDialog(self, 'Create Director %s %s?' %director, style=wx.YES_NO)
            if dialog.ShowModal() == wx.ID_YES:
                dialog.Destroy()
                directorID = self.dataAccess.createDirector(director)
                if directorID is False:
                    return
            else:
                dialog.Destroy()
                return
        else:
            directorID = self.directors[director]


        dialogString = "Create Film:%s\nDirector:%s\nLength:%s\nGenre:%s\nFormat:%s\nYear:%s\nCriterion:%s" %(title, director[0] + ' ' + director[1],
                                                                                                             length, self.genreChoice.GetStringSelection(),
                                                                                                             self.formatChoice.GetStringSelection(),
                                                                                                             year,
                                                                                                             self.criterionCheckbox.IsChecked())
        if title in self.dataAccess.films:
            dialogString += '\nTHIS TITLE IS ALREADY PRESENT IN THE DATABASE'

        dialog = wx.MessageDialog(self, dialogString, style=wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            filmId = self.dataAccess.createFilm(title, year, genre, length, isCriterion, directorID, format)[-1][-1]
            if not filmId:
                return

            for panel in self.relatingPanels:
                panel.onCreate(filmId)
        else:
            dialog.Destroy()
        event.Skip()


class SeriesPanel(BasePanel):

    def __init__(self, parent, dataAccess):
        BasePanel.__init__(self, parent, dataAccess)

        self.relatingPanels = []

        infoSizer1 = wx.BoxSizer(wx.HORIZONTAL)


        nameStaticBox = wx.StaticBox(self, -1, 'Name')
        nameSizer = wx.StaticBoxSizer(nameStaticBox, wx.HORIZONTAL)
        self.nameBox = wx.TextCtrl(self, -1, size=(200, -1))
        nameSizer.Add(self.nameBox, 0, wx.ALL, 4)

        yearStaticBox = wx.StaticBox(self, -1, 'Year')
        yearSizer = wx.StaticBoxSizer(yearStaticBox, wx.HORIZONTAL)
        self.yearBox = wx.TextCtrl(self, -1, size=(47, -1))
        self.yearBox.SetMaxLength(4)
        yearSizer.Add(self.yearBox, 0, wx.ALL, 4)

        infoSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        formatStaticBox = wx.StaticBox(self, -1, 'Format')
        formatSizer = wx.StaticBoxSizer(formatStaticBox, wx.HORIZONTAL)
        self.formatChoice = wx.Choice(self, -1, choices=self.dataAccess.formats.keys())
        self.formatChoice.SetStringSelection('DVD')
        formatSizer.Add(self.formatChoice, 0, wx.ALL, 4)

        genreStaticBox = wx.StaticBox(self, -1, 'Genre')
        genreSizer = wx.StaticBoxSizer(genreStaticBox, wx.HORIZONTAL)
        self.genreChoice = wx.Choice(self, -1, choices=self.dataAccess.genres.keys())
        genreSizer.Add(self.genreChoice, 0, wx.ALL, 4)

        self.countryPanel = scrolled.ScrolledPanel(self, -1, size=(-1, 175))
        self.countryPanel.SetBackgroundColour(const.BACKGROUNDCOLOUR)
        countryPanelStaticBox = wx.StaticBox(self, -1, "Countries")
        self.countryPanelStaticBoxSizer = wx.StaticBoxSizer(countryPanelStaticBox, wx.VERTICAL)
        self.countryPanelSizer = wx.BoxSizer(wx.VERTICAL)
        addCountryButton = wx.Button(self, -1, 'Add Country')

        self.countryPanelStaticBoxSizer.Add(addCountryButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)
        self.countryPanelStaticBoxSizer.Add(self.countryPanel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 4)
        panel = CountryPanel(self.countryPanel, self.dataAccess)
        self.relatingPanels.append(panel)
        self.countryPanelSizer.Add(panel, 0, wx.ALL|wx.EXPAND, 4)

        self.countryPanel.SetSizer(self.countryPanelSizer)
        self.countryPanel.SetAutoLayout(1)
        self.countryPanel.SetupScrolling()

        self.actorPanel = scrolled.ScrolledPanel(self, -1, size=(-1, 175))
        self.actorPanel.SetBackgroundColour(const.BACKGROUNDCOLOUR)
        actorPanelStaticBox = wx.StaticBox(self, -1, "Actors")
        self.actorPanelStaticBoxSizer = wx.StaticBoxSizer(actorPanelStaticBox, wx.VERTICAL)
        self.actorPanelSizer = wx.BoxSizer(wx.VERTICAL)
        addactorButton = wx.Button(self, -1, 'Add actor')

        self.actorPanelStaticBoxSizer.Add(addactorButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)
        self.actorPanelStaticBoxSizer.Add(self.actorPanel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 4)
        panel = ActorPanel(self.actorPanel, self.dataAccess)
        self.relatingPanels.append(panel)
        self.actorPanelSizer.Add(panel, 0, wx.ALL|wx.EXPAND, 4)

        self.actorPanel.SetSizer(self.actorPanelSizer)
        self.actorPanel.SetAutoLayout(1)
        self.actorPanel.SetupScrolling()

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        createButton = wx.Button(self, -1, 'Add series')
        cancelButton = wx.Button(self, -1, 'Cancel')
        buttonSizer.Add(createButton, 0, wx.ALIGN_CENTER|wx.ALIGN_BOTTOM|wx.ALL, 4)
        buttonSizer.Add(cancelButton, 0, wx.ALIGN_CENTER|wx.ALL, 4)

        infoSizer1.Add(nameSizer, 2, wx.ALL, 4)
        infoSizer1.Add(yearSizer, 1, wx.ALL, 4)

        infoSizer2.Add(formatSizer, 1 , wx.ALL, 4)
        infoSizer2.Add(genreSizer, 1 , wx.ALL, 4)

        self.Bind(wx.EVT_BUTTON, self.onCreate, createButton)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelButton)
        self.Bind(wx.EVT_BUTTON, self.onAddCountry, addCountryButton)
        self.Bind(wx.EVT_BUTTON, self.onAddActor, addactorButton)

        self.mainSizer.Add(infoSizer1, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(infoSizer2, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(self.countryPanelStaticBoxSizer, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(self.actorPanelStaticBoxSizer, 0, wx.ALL|wx.EXPAND, 4)
        self.mainSizer.Add(buttonSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)

    def onCreate(self, event):

        name = self.nameBox.GetValue()
        if name == "":
            self.createWarningBox("Please type a name for this series!", True)
            return

        year = self.yearBox.GetValue()
        if not self.isnumber(year) or len(year) < 4:
            self.createWarningBox("Invalid entry for year!", True)
            return

        format = self.dataAccess.formats[self.formatChoice.GetStringSelection()]

        genre = self.dataAccess.genres[self.genreChoice.GetStringSelection()]

        dialogString = "Create series:%s\nGenre:%s\nFormat:%s\nYear:%s" %(name,
                                                                          self.genreChoice.GetStringSelection(),
                                                                          self.formatChoice.GetStringSelection(),
                                                                          year)
        if name in self.dataAccess.getseries():
            dialogString += '\nTHIS name IS ALREADY PRESENT IN THE DATABASE'

        dialog = wx.MessageDialog(self, dialogString, style=wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            seriesId = self.dataAccess.createseries(name, year, genre, format)[-1][-1]
            if not seriesId:
                self.createWarningBox('Failed to create this series.', True)

            for panel in self.relatingPanels:
                panel.onCreate(seriesId, False)
        else:
            dialog.Destroy()
        event.Skip()



class ActorPanel(BasePanel):
    def __init__(self, parent, dataAccess):
        BasePanel.__init__(self, parent, dataAccess, size=(-1, 100))

        actorStaticBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        actorFNStaticBox = wx.StaticBox(self, -1, "First Name")
        actorFNStaticBoxSizer = wx.StaticBoxSizer(actorFNStaticBox, wx.HORIZONTAL)
        self.actorFNTextCtrl = TextCtrlAutoComplete(self, -1, choices=[key[0] for key in self.dataAccess.actors],size=(200, -1))
        actorFNStaticBoxSizer.Add(self.actorFNTextCtrl, 0, wx.ALL, 4)

        actorLNStaticBox = wx.StaticBox(self, -1, "Last Name")
        actorLNStaticBoxSizer = wx.StaticBoxSizer(actorLNStaticBox, wx.HORIZONTAL)
        self.actorLNTextCtrl = TextCtrlAutoComplete(self, -1,  choices=[key[1] for key in self.dataAccess.actors], size=(200, -1))
        actorLNStaticBoxSizer.Add(self.actorLNTextCtrl, 0, wx.ALL, 4)

        actorStaticBoxSizer.Add(actorFNStaticBoxSizer, 1, wx.ALL, 4)
        actorStaticBoxSizer.Add(actorLNStaticBoxSizer, 1, wx.ALL, 4)

        self.actorFNTextCtrl.Bind(wx.EVT_KILL_FOCUS, self.onActorFNKillFocus)

        self.mainSizer.Add(actorStaticBoxSizer, 1, wx.EXPAND)

    def onActorFNKillFocus(self, event):
        text = event.GetEventObject().GetValue()
        for key in self.dataAccess.actors:
            if text == key[0]:
                self.actorLNTextCtrl.SetValue(key[1])
        self.actorLNTextCtrl.SetChoices([key[1] for key in self.dataAccess.actors if text == key[0]])
        event.Skip()

    def onCreate(self, filmId, isFilm=True):
        actor = (self.actorFNTextCtrl.GetValue(), self.actorLNTextCtrl.GetValue())
        if actor[1] == '':
            return
        if not self.dataAccess.checkActor(actor):
            dialog = wx.MessageDialog(self, 'Create Actor %s %s?' %actor, style=wx.YES_NO)
            if dialog.ShowModal() == wx.ID_YES:
                dialog.Destroy()
                actorId = self.dataAccess.createActor(actor)
                if not actorId:
                    return
            else:
                dialog.Destroy()
                return
        else:
            actorId = self.dataAccess.actors[actor]
        self.dataAccess.relateActor(filmId, actorId, isFilm)


class CountryPanel(BasePanel):
    def __init__(self, parent, dataAccess):
        BasePanel.__init__(self, parent, dataAccess, size=(-1, 100))


        self.countryStaticBox = wx.StaticBox(self, -1, 'Country')
        self.countryStaticBoxSizer = wx.StaticBoxSizer(self.countryStaticBox, wx.VERTICAL)
        self.countryText = TextCtrlAutoComplete(self, -1, choices=[key for key in self.dataAccess.countries],size=(200, -1))
        self.countryStaticBoxSizer.Add(self.countryText, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)

        self.mainSizer.Add(self.countryStaticBoxSizer, 1, wx.EXPAND)


    def onCreate(self, filmId, isFilm=True):
        country = self.countryText.GetValue()
        if country == '':
            return
        if not self.dataAccess.checkCountry(country):
            dialog = wx.MessageDialog(self, 'Create Country %s?' %country, style=wx.YES_NO)
            if dialog.ShowModal() == wx.ID_YES:
                dialog.Destroy()
                countryId = self.dataAccess.createCountry(country)
                if not countryId:
                    return
            else:
                dialog = wx.MessageDialog(self, 'Create Country %s?' %country, style=wx.YES_NO)
                return
        else:
            countryId = self.dataAccess.countries[country]
        self.dataAccess.relateCountry(filmId, countryId, isFilm)




class ArtistPanel(BasePanel):

    def __init__(self, parent, dataAccess):
        BasePanel.__init__(self, parent, dataAccess, size=(-1, 100))

        self.artistStaticBox = wx.StaticBox(self, -1, 'artist')
        self.artistStaticBoxSizer = wx.StaticBoxSizer(self.artistStaticBox, wx.VERTICAL)
        self.artistText = TextCtrlAutoComplete(self, -1, choices=[key for key in self.dataAccess.artists],size=(200, -1))
        self.artistStaticBoxSizer.Add(self.artistText, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)

        self.mainSizer.Add(self.artistStaticBoxSizer, 1, wx.EXPAND)


    def onCreate(self, diskId, isDVD=True):
        artist = self.artistText.GetValue()
        if artist == '':
            return
        if not self.dataAccess.checkArtist(artist):
            dialog = wx.MessageDialog(self, 'Create artist %s?' %artist, style=wx.YES_NO)
            if dialog.ShowModal() == wx.ID_YES:
                dialog.Destroy()
                artistId = self.dataAccess.createArtist(artist)
                if not artistId:
                    return
            else:
                dialog.Destroy()
                return
        else:
            artistId = self.dataAccess.artists[artist]
        self.dataAccess.relateArtistMusic(artistId, diskId, isDVD)
