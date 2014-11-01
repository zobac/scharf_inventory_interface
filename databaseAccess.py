
import MySQLdb as mysql
import _mysql_exceptions as mysqle
import constants as const

class DatabaseManager(object):

    def __init__(self):

        self.db = mysql.connect(host=const.HOST, user=const.USER,
                                passwd=const.PASSWORD, db=const.DATABASE)
        self.cursor = self.db.cursor()

    def execute(self, sql):

        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results

        except mysqle.MySQLError:
            self.cursor.close()
            self.cursor = self.db.cursor()
            return False


    def commit(self):
        self.db.commit()


    def close():
        self.cursor.close()
