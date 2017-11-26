
import urllib3
import json
from sql import SQL

urllib3.disable_warnings()

class LongBot:
    CfgFile = "longbot.cfg"

    @staticmethod
    def loadBots(hash):
        # Load all bots matching hash
        bots = []
        s = SQL()
        s.connect()
        rows = s.fetchBots(hash)
        for r in rows:
            #print("LOAD bot " + r['name'])
            lb = LongBot(r['name'], r['data'])
            bots.append(lb)
        s.close()
        return bots

    @staticmethod
    def fetch(freq):
        data = {}
        if freq in ("hourly", "daily"):
            # Do daily stuff
            try:
                s = SQL()
                s.connect()
                rows = SQL.fetchFromSource(freq)
                http = urllib3.PoolManager()

                for r in rows:
                    try:
                        res = http.request('GET', r['url'])
                        print("B" + str(res._body))
                        if res.status == 200:
                            exec('from process_' + r['handler'] + ' import Processor')
                            pres = exec('Processor.process(str(res._body))')
                            if pres['valid']:
                                data[pres['ticker']] = pres['last']
                        else:
                            print("Could not download from " + r['url'])
                            print(str(res._body))
                    except Exception as e:
                        print(r['name'] + str(e))
                http.clear()
            except Exception as e:
                print(str(e))
            finally:
                s.close()
        else:
            return False
        return True

    def readCfg(self):
        with open(LongBot.CfgFile) as fp:
            for line in fp:
                ar = line.split("=", 1)
                self.props[ar[0].strip()] = ar[1].strip()

    def parseProfile(self, profile):
        self.profile = json.loads(profile)

    def get(self, key):
        if key in self.props:
            return self.props[key]
        return None

    def set(self, key, val):
        self.props[key] = val

    def __init__(self, name, profile):
        # Read config
        #print(os.path.dirname(os.path.realpath(__file__)))
        self.name = name
        self.props = {}
        self.readCfg()
        self.profile = self.parseProfile(profile)
        self.sql = SQL()