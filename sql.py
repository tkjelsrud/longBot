import MySQLdb
import MySQLdb.cursors

class SQL:
    CfgFile = "longbot.cfg"

    def connect(self):
        self.con = MySQLdb.connect(user=self.props['db.user'], passwd=self.props['db.pass'],
                    host=self.props['db.host'],db=self.props['db.db'], cursorclass=MySQLdb.cursors.DictCursor)

    def close(self):
        if self.con:
            self.con.close()

    def fetchFromSource(self, freq):
        rows = None
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT name, url, handler, frequency FROM source WHERE frequency = '%s'" % (freq))
            rows = cursor.fetchall()
        except MySQLdb.Error as e:
            print(e)
        finally:
            cursor.close()

        return rows

    def insertTickerData(self, name, price, volume = -1, fdate = ""):
        res = None
        try:
            cursor = self.con.cursor()
            res = cursor.execute("INSERT INTO ticker (name, price, volume, fdate) VALUES('%s', %s, %s, '%s')" % (name, price, volume, fdate))
            self.con.commit()
        except MySQLdb.Error as e:
            print(e)
        finally:
            cursor.close()

        return res

    def fetchBots(self, hash):
        rows = None
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT name, data, updated FROM bot WHERE hash = '%s'" % (hash))
            rows = cursor.fetchall()
        except MySQLdb.Error as e:
            print(e)
        finally:
            cursor.close()

        return rows

    def readCfg(self):
        with open(SQL.CfgFile) as fp:
            for line in fp:
                ar = line.split("=", 1)
                self.props[ar[0].strip()] = ar[1].strip()

    def __init__(self):
        self.con = None
        self.props = {}
        self.readCfg()
