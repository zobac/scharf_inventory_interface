
from databaseAccess import DatabaseManager as dbm


class DataAccess(object):

    def __init__(self):
        self.loadAttrs()


    def loadAttrs(self):
        self.genres = self.getGenres()

        self.formats = self.getFormats()

        self.directors = self.getDirectors()

        self.genres = self.getGenres()

        self.formats = self.getFormats()

        self.actors = self.getActors()

        self.countries = self.getCountries()

        self.artists = self.getArtists()

        self.films = self.getfilms()

        self.musicDVDs = self.getMusicDVDs()


    def getMusicDVDs(self):

        dm = dbm()
        sql = '''
        SELECT id, title
        FROM music_dvd
        '''
        results = dm.execute(sql)
        musicDVDs = {}
        for result in results:
            id, musicDVD = result
            musicDVDs[musicDVD] = id
        return musicDVDs


    def createMusicDVD(self, title, year, format):
        dm = dbm()
        sql = 'INSERT INTO music_dvd\
        (title, year, format)\
        VALUES\
        (%s, %s, %s)\
        '%("'" + title + "'", year, format)
        results = dm.execute(sql)
        dm.commit()
        if results is not False:
            sql = 'SELECT id FROM music_dvd WHERE title = %s' %("'" + title + "'")
            results = dm.execute(sql)
        return results


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


    def getfilms(self):
        dm = dbm()
        sql = '''
        SELECT title
        FROM films
        '''
        results = dm.execute(sql)
        films = []
        if results:
            for result in results:

                films.append(result[0])
        return films


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


    def createDirector(self, nameTupple):

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
        return False




    def getseries(self):
        dm = dbm()
        sql = '''
        SELECT name
        FROM series
        '''
        results = dm.execute(sql)
        series = []
        if results:
            for result in results:

                series.append(result[0])
        return series


    def createseries(self, name, year, genre, format):
        dm = dbm()
        sql = 'INSERT INTO series\
        (name, year, genre, format)\
        VALUES\
        (%s, %s, %s, %s)\
        '%("'" + name + "'", year, genre, format)
        results = dm.execute(sql)
        dm.commit()
        if results is not False:
            sql = 'SELECT id FROM series WHERE name = %s' %("'" + name + "'")
            results = dm.execute(sql)
        return results


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


    def createActor(self, nameTupple):
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
        return False


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

    def createCountry(self, country):
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
        return False


    def getArtists(self):
        dm = dbm()
        sql = '''
        SELECT id, name
        FROM artist
        '''
        results = dm.execute(sql)
        artists = {}
        for result in results:
            id, name = result
            artists[name] = id
        return artists



    def createArtist(self, artist):
        dm = dbm()
        sql = 'INSERT INTO artist\
        (name)\
        VALUES\
        (%s)'%("'" + artist + "'")
        results = dm.execute(sql)
        dm.commit()
        if results is not False:
            sql = 'SELECT id FROM artist\
            WHERE name = %s\
            '%("'" + artist + "'")
            results = dm.execute(sql)
            return results[0][0]
        return False


    def checkDirector(self, nameTupple):
        if nameTupple in self.directors:
            return True
        else:
            return False

    def checkActor(self, nameTupple):
        if nameTupple in self.actors:
            return True
        else:
            return False

    def checkCountry(self, country):
        if country not in self.countries:
            return False
        return True

    def checkArtist(self, artist):
        if artist not in self.artists:
            return False
        return True


    def relateActor(self, filmId, actorId, isFilm):
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


    def relateCountry(self, filmId, countryId, isFilm):
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

    def relateArtistMusic(self, artisdId, diskId, isDVD):
        dm = dbm()
        if isDVD:
            sql = 'INSERT INTO artist_dvd\
            (artist, dvdid)\
            VALUES\
            (%s, %s)'%(artisdId, diskId)
        else:
            sql = 'INSERT INTO series_cd\
            (artist, cdid)\
            VALUES\
            (%s, %s)'%(artisdId, diskId)
        results = dm.execute(sql)
        dm.commit()

