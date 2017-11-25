import mysql.connector
from mysql.connector import Error
import urllib3


class LongBot:
    CfgFile = "longbot.cfg"

    def fetch(self, freq):
        if freq in ("hourly", "daily"):
            # Do daily stuff
            try:
                self.sqlConnect()
                rows = self.sqlFetchFromSource(freq)
                http = urllib3.PoolManager()

                for r in rows:
                    urllib3.disable_warnings()
                    #print(r[0])
                    r = http.request('GET', r[1])
                    #print(len(r._body))
                http.clear()

            except Error as e:
                print(e)
            finally:
                self.sqlClose()
        else:
            return False
        return True

    def readCfg(self):
        with open(LongBot.CfgFile) as fp:
            for line in fp:
                ar = line.split("=", 1)
                self.props[ar[0].strip()] = ar[1].strip()

    def get(self, key):
        return self.props[key]

    def sqlFetchFromSource(self, freq):
        rows = None
        try:
            cursor = self.sql.cursor()
            cursor.execute("SELECT * FROM source WHERE frequency = '%s'" % (freq))
            rows = cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            cursor.close()

        return rows

    def sqlConnect(self):
        self.sql = mysql.connector.connect(user=self.get('db.user'), password=self.get('db.pass'),
                              host=self.get('db.host'),database=self.get('db.db'))

    def sqlClose(self):
        if self.sql:
            self.sql.close()

    def __init__(self):
        # Read config
        self.props = {}
        self.readCfg()
        self.sql = None