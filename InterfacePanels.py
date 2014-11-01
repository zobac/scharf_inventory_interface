

import wx

import wx.lib.scrolledpanel as scrolled
import constants as const

from TextCtrlAutoComplete import TextCtrlAutoComplete

from databaseAccess import DatabaseManager as dbm


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
            panel = FilmPanel(self.Parent)
        elif selection == const.SERIES:
            panel = SeriesPanel(self.Parent)
        else:
            panel = MusicDVDPanel(self.Parent)

        self.Parent.mainSizer.Detach(self)
        self.Parent.mainSizer.Add(panel, 1, wx.EXPAND)
        self.Parent.Layout()
        self.Destroy()



class BasePanel(wx.Panel):

    def __init__(self, parent, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, -1, size=(-1,-1))
        self.SetBackgroundColour(const.BACKGROUNDCOLOUR)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)


        # Event Bindings

        self.SetSizer(self.mainSizer)


class MusicDVDPanel(BasePanel):

    def __init__(self, parent):
        BasePanel.__int__(self, parent)

    def onCreate(self, event):
            event.Skip()


    def checkArtist(self):
            pass


    def createArtist(self):
        pass


    def createArtistDVD(self):
        pass


    def onAddArtist(self, event):
        event.Skip()



class FilmPanel(BasePanel):

    def __init__(self, parent):
        BasePanel.__init__(self, parent)

        self.ignoreEvtText = False

        self.genres = self.getGenres()
        genreList = self.genres.keys()
        genreList.sort()

        self.formats = self.getFormats()
        formatList = self.formats.keys()
        formatList.sort()

        self.relatingPanels = []

        self.directors = self.getDirectors()

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
        self.formatChoice = wx.Choice(self, -1, choices=formatList)
        formatSizer.Add(self.formatChoice, 0, wx.ALL, 4)

        genreStaticBox = wx.StaticBox(self, -1, 'Genre')
        genreSizer = wx.StaticBoxSizer(genreStaticBox, wx.HORIZONTAL)
        self.genreChoice = wx.Choice(self, -1, choices=genreList)
        genreSizer.Add(self.genreChoice, 0, wx.ALL, 4)

        directorStaticBox = wx.StaticBox(self, -1, 'Director')
        directorStaticBoxSizer = wx.StaticBoxSizer(directorStaticBox, wx.HORIZONTAL)

        directorFNStaticBox = wx.StaticBox(self, -1, "First Name")
        directorFNStaticBoxSizer = wx.StaticBoxSizer(directorFNStaticBox, wx.HORIZONTAL)
        self.directorFNTextCtrl = TextCtrlAutoComplete(self, -1, choices=[key[0] for key in self.directors.keys()],size=(200, -1))
        directorFNStaticBoxSizer.Add(self.directorFNTextCtrl, 0, wx.ALL, 4)

        directorLNStaticBox = wx.StaticBox(self, -1, "Last Name")
        directorLNStaticBoxSizer = wx.StaticBoxSizer(directorLNStaticBox, wx.HORIZONTAL)
        self.directorLNTextCtrl = TextCtrlAutoComplete(self, -1,  choices=[key[1] for key in self.directors.keys()], size=(200, -1))
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
        panel = CountryPanel(self.countryPanel)
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
        panel = ActorPanel(self.actorPanel)
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
        for key in self.directors.keys():
            if text == key[0]:
                self.directorLNTextCtrl.SetValue(key[1])
        self.directorLNTextCtrl.SetChoices([key[1] for key in self.directors.keys() if text == key[0]])
        event.Skip()



    def getDirectors(self):

        dm = dbm()
        sql = '''
        SELECT id, first_name, last_name
        FROM director
        '''
        results = dm.execute(sql)
        directors = {}
        if results:
            for result in results:
                id, firstName, lastName = result
                directors[(firstName, lastName)] = id
        return directors


    def getGenres(self):

        dm = dbm()
        sql = '''
        SELECT id, genre
        FROM genre
        '''
        results = dm.execute(sql)
        genres = {}
        for result in results:
            id, genre = result
            genres[genre] = id
        return genres


    def getFormats(self):

        dm = dbm()
        sql = '''
        SELECT id, name
        FROM format
        '''
        results = dm.execute(sql)
        formats = {}
        for result in results:
            id, format = result
            formats[format] = id
        return formats



    def onCreate(self, event):
        title = self.titleBox.GetValue()
        year = self.yearBox.GetValue()
        isCriterion = int(self.criterionCheckbox.IsChecked())
        length = self.lengthBox.GetValue()
        format = self.formats[self.formatChoice.GetStringSelection()]
        genre = self.genres[self.genreChoice.GetStringSelection()]
        director = (self.directorFNTextCtrl.GetValue(), self.directorLNTextCtrl.GetValue())

        if not self.checkDirector(director):
            directorID = self.createDirector(director)
            if directorID is None:
                return
        else:
            directorID = self.directors[director]


        dialogString = "Create Film:%s\nDirector:%s\nLength:%s\nGenre:%s\nFormat:%s\nYear:%s\nCriterion:%s" %(title, director[0] + ' ' + director[1],
                                                                                                             length, self.genreChoice.GetStringSelection(),
                                                                                                             self.formatChoice.GetStringSelection(),
                                                                                                             year,
                                                                                                             self.criterionCheckbox.IsChecked())
        dialog = wx.MessageDialog(self, dialogString, style=wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            filmId = self.createFilm(title, year, genre, length, isCriterion, directorID, format)[0][0]
            if not filmId:
                return

            for panel in self.relatingPanels:
                panel.onCreate(filmId)
        else:
            dialog.Destroy()
        event.Skip()


    def onCancel(self, event):

        event.Skip()

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


    def checkDirector(self, nameTupple):
        if nameTupple in self.directors:
            return True
        else:
            return False


    def createDirector(self, nameTupple):
        dialog = wx.MessageDialog(self, 'Create Director %s %s?' %nameTupple, style=wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            dm = dbm()
            sql = 'INSERT INTO director\
            (first_name, last_name)\
            VALUES\
            (%s, %s)'%("'" + nameTupple[0] + "'", "'" + nameTupple[1] + "'")
            results = dm.execute(sql)
            dm.commit()
            if results is not False:
                sql = 'SELECT id FROM director\
                WHERE first_name = %s\
                AND last_name = %s'%("'" + nameTupple[0] + "'", "'" + nameTupple[1] + "'")
                results = dm.execute(sql)
                return results[0][0]
        else:
            dialog.Destroy()
        return False


    def createFilm(self, title, year, genre, length, isCriterion, directorID, format):
        dm = dbm()
        sql = 'INSERT INTO films\
        (title, year, genre, length, criterion_edition, director, format)\
        VALUES\
        (%s, %s, %s, %s, %s, %s, %s)\
        '%("'" + title + "'", year, genre, length, isCriterion, directorID, format)
        results = dm.execute(sql)
        dm.commit()
        if results is not False:
            sql = 'SELECT id FROM films WHERE title = %s' %("'" + title + "'")
            results = dm.execute(sql)
        return results





class SeriesPanel(BasePanel):

    def __init__(self, parent):
        BasePanel.__init__(self, parent)

    def onCreate(self, event):
        event.Skip()


    def createSeries(self):
        pass


class ActorPanel(BasePanel):
    def __init__(self, parent):
        BasePanel.__init__(self, parent, size=(-1, 100))

        self.actors = self.getActors()

        actorStaticBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        actorFNStaticBox = wx.StaticBox(self, -1, "First Name")
        actorFNStaticBoxSizer = wx.StaticBoxSizer(actorFNStaticBox, wx.HORIZONTAL)
        self.actorFNTextCtrl = TextCtrlAutoComplete(self, -1, choices=[key[0] for key in self.actors.keys()],size=(200, -1))
        actorFNStaticBoxSizer.Add(self.actorFNTextCtrl, 0, wx.ALL, 4)

        actorLNStaticBox = wx.StaticBox(self, -1, "Last Name")
        actorLNStaticBoxSizer = wx.StaticBoxSizer(actorLNStaticBox, wx.HORIZONTAL)
        self.actorLNTextCtrl = TextCtrlAutoComplete(self, -1,  choices=[key[1] for key in self.actors.keys()], size=(200, -1))
        actorLNStaticBoxSizer.Add(self.actorLNTextCtrl, 0, wx.ALL, 4)

        actorStaticBoxSizer.Add(actorFNStaticBoxSizer, 1, wx.ALL, 4)
        actorStaticBoxSizer.Add(actorLNStaticBoxSizer, 1, wx.ALL, 4)

        self.actorFNTextCtrl.Bind(wx.EVT_KILL_FOCUS, self.onActorFNKillFocus)

        self.mainSizer.Add(actorStaticBoxSizer, 1, wx.EXPAND)

    def onActorFNKillFocus(self, event):
        text = event.GetEventObject().GetValue()
        for key in self.actors.keys():
            if text == key[0]:
                self.actorLNTextCtrl.SetValue(key[1])
        self.actorLNTextCtrl.SetChoices([key[1] for key in self.actors.keys() if text == key[0]])
        event.Skip()

    def getActors(self):
        dm = dbm()
        sql = '''
        SELECT id, first_name, last_name
        FROM actor
        '''
        results = dm.execute(sql)
        actors = {}
        if results:
            for result in results:
                id, first_name, last_name = result
                actors[(first_name, last_name)] = id
        return actors



    def onCreate(self, filmId, isFilm=True):
        actor = (self.actorFNTextCtrl.GetValue(), self.actorLNTextCtrl.GetValue())
        if actor[1] == '':
            return
        if not self.checkActor(actor):
            actorId = self.createActor(actor)
            if not actorId:
                return
        else:
            actorId = self.actors[actor]
        self.relate(filmId, actorId, isFilm)


    def relate(self, filmId, actorId, isFilm):
        dm = dbm()
        if isFilm:
            sql = 'INSERT INTO film_actor\
            (film, actor)\
            VALUES\
            (%s, %s)'%(filmId, actorId)
        else:
            sql = 'INSERT INTO series_actor\
            (series, actor)\
            VALUES\
            (%s, %s)'%(filmId, actorId)

        results = dm.execute(sql)
        dm.commit()



    def checkActor(self, nameTupple):
        if nameTupple in self.actors:
            return True
        else:
            return False

    def createActor(self, nameTupple):
        dialog = wx.MessageDialog(self, 'Create actor %s %s?' %nameTupple, style=wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            dm = dbm()
            sql = 'INSERT INTO actor\
            (first_name, last_name)\
            VALUES\
            (%s, %s)'%("'" + nameTupple[0] + "'", "'" + nameTupple[1] + "'")
            results = dm.execute(sql)
            dm.commit()
            if results is not False:
                sql = 'SELECT id FROM actor\
                WHERE first_name = %s\
                AND last_name = %s'%("'" + nameTupple[0] + "'", "'" + nameTupple[1] + "'")
                results = dm.execute(sql)
                return results[0][0]
        else:
            dialog.Destroy()
        return False


class CountryPanel(BasePanel):
    def __init__(self, parent):
        BasePanel.__init__(self, parent, size=(-1, 100))

        self.countries = self.getCountries()

        self.countryStaticBox = wx.StaticBox(self, -1, 'Country')
        self.countryStaticBoxSizer = wx.StaticBoxSizer(self.countryStaticBox, wx.VERTICAL)
        self.countryText = TextCtrlAutoComplete(self, -1, choices=[key for key in self.countries.keys()],size=(200, -1))
        self.countryStaticBoxSizer.Add(self.countryText, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 4)

        self.mainSizer.Add(self.countryStaticBoxSizer, 1, wx.EXPAND)

    def getCountries(self):
        dm = dbm()
        sql = '''
        SELECT id, name
        FROM country
        '''
        results = dm.execute(sql)
        countries = {}
        for result in results:
            id, name = result
            countries[name] = id
        return countries


    def checkCountry(self, country):
        if country not in self.countries:
            return False
        return True

    def createCountry(self, country):
        dialog = wx.MessageDialog(self, 'Create Country %s?' %country, style=wx.YES_NO)
        if dialog.ShowModal() == wx.ID_YES:
            dialog.Destroy()
            dm = dbm()
            sql = 'INSERT INTO country\
            (name)\
            VALUES\
            (%s)'%("'" + country + "'")
            results = dm.execute(sql)
            dm.commit()
            if results is not False:
                sql = 'SELECT id FROM country\
                WHERE name = %s\
                '%("'" + country + "'")
                results = dm.execute(sql)
                return results[0][0]
        else:
            dialog.Destroy()
        return False

    def onCreate(self, filmId, isFilm=True):
        country = self.countryText.GetValue()
        if country == '':
            return
        if not self.checkCountry(country):
            countryId = self.createCountry(country)
            if not countryId:
                return
        else:
            countryId = self.countries[country]
        self.relate(filmId, countryId, isFilm)

    def relate(self, filmId, countryId, isFilm):
        dm = dbm()
        if isFilm:
            sql = 'INSERT INTO film_country\
            (film, country)\
            VALUES\
            (%s, %s)'%(filmId, countryId)
        else:
            sql = 'INSERT INTO series_country\
            (series, country)\
            VALUES\
            (%s, %s)'%(filmId, countryId)
        results = dm.execute(sql)
        dm.commit()




class ArtistPanel(BasePanel):
    def __init__(self, parent):
        self.artistDict = {}
        BasePanel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        inputSizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Artist Name")
        self.box = wx.TextCtrl(self, -1, size=(75, -1))
        inputSizer.Add(label, 0, wx.ALL, 4)
        inputSizer.Add(self.box, 0, wx.ALL, 4)

        sizer.Add(inputSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 4)

        # Event Bindings
        self.Bind(wx.EVT_TEXT, self.onArtistText, self.artistBox)

        self.SetSizer()


    def onCreate(self):
        #create artist
        pass

    def getArtists(self):
        return str(self.artistBox.GetValue())

    def createArtist(self):
        pass
