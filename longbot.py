from sql import SQL
import shelve, sys, importlib, json, urllib3
#from process_nasdaqrss import Processor

urllib3.disable_warnings()

class LongBot:
    Data = {} # Static data array
    CfgFile = "longbot.cfg"
    CacheFile = "longbot.cache"

    @staticmethod
    def splitCur(val):
        cur = val[0:3]
        val = val[3:]
        return (cur, val)

    @staticmethod
    def getData(key):
        #if key in LongBot.Data:
        return LongBot.Data[key.upper()]
        #return None

    @staticmethod
    def setData(key, val):
        LongBot.Data[key.upper()] = val

    @staticmethod
    def cacheData():
        LongBot.Data = shelve.open(LongBot.CacheFile)

    @staticmethod
    def closeCache():
        LongBot.Data.close()

    @staticmethod
    def loadBots(hash):
        # Load all bots matching hash
        bots = []
        s = SQL()
        s.connect()
        rows = s.fetchBots(hash)
        for r in rows:
            #print("LOAD bot " + r['name'] + " --> " + r['data'])
            lb = LongBot(r['name'], r['data'])
            bots.append(lb)
        s.close()
        return bots

    @staticmethod
    def fetch(freq):
        fCnt = 0
        if freq in ("hourly", "daily"):
            # Do daily stuff
            try:
                s = SQL()
                s.connect()
                rows = s.fetchFromSource(freq)
                http = urllib3.PoolManager()
                #print("Fetch sources" + str(len(rows)))
                for r in rows:
                    try:
                        cache = None
                        try:
                            cache = LongBot.getData(r['url'])
                        except Exception as e:
                            #print("Not in cache i guess")
                            None

                        if not cache:
                            print("INFO\tNot cached, loading " + r['url'])
                            res = http.request('GET', r['url'])
                            if res.status == 200:
                                Processor = getattr(importlib.import_module("process_" + r['handler']), "Processor")
                                pres = Processor.process(str(res._body))
                                print(str(pres))
                                if pres['valid']:
                                    LongBot.setData(pres['ticker'], pres['last'])
                                    fCnt = fCnt + 1
                                    LongBot.setData(r['url'], True)
                            else:
                                print("WARN\tCould not download from " + r['url'])
                                print(str(res._body))
                        else:
                            print("INFO\tCached, not loading " + r['url'])
                            fCnt = fCnt + 1
                    except Exception as e:
                        print("ERROR\t" + r['name'] + "\t" + str(e))
                http.clear()
            except Exception as e:
                print(str(e))
            finally:
                s.close()
        return fCnt

    def calcDepo(self):
        pDepo = {}
        pWarn = []

        if len(LongBot.Data) == 0:
            print("No data loaded, aborting")
            return None

        for pos in self.getDepo():
            # Calculate value of position vs original cost
            # TODO add improved error checking/handling

            perf = {'currency': {"pc": 0.0, "at": 0, "now": 0}, 'position': {"pc": 0.0, "at": 0, "now": 0}, 'rating': ""}

            count = float(pos['count'])
            cost  = LongBot.splitCur(pos['cost'])
            fees  = LongBot.splitCur(pos['fees'])
            oCost = float(cost[1]) - float(fees[1])
            oExch = 1

            at = LongBot.splitCur(pos['at'])
            #atNOK = at[1]
            if at[0] in ("EUR", "USD"):
                #atNOK = float(at[1]) * float(LongBot.getData(at[0]))
                oExch = oCost / (count * float(at[1]))

                perf['currency']['pc'] = (1 - (oExch / float(LongBot.getData(at[0])))) * 100.0
                perf['currency']['at'] = oExch
                perf['currency']['now'] = float(LongBot.getData(at[0]))

            nCost = count * float(LongBot.getData(pos['ticker'])) * float(LongBot.getData(at[0]))
            perf['position']['pc'] = (1 - (oCost / nCost)) * 100.0
            perf['position']['at'] = oCost
            perf['position']['now'] = nCost
            perf['result'] = nCost - float(cost[1])
            perf['rating'] = self.depoRating(perf['position']['pc'])

            if pos['rating'] != perf['rating']:
                # Rating has changed - issue warning
                pWarn.append(pos['ticker'] + " Rating change "  + pos['rating'] + " to " + perf['rating'] + " (" + str(round(perf['result'])) + "NOK " + str(round(perf['position']['pc'], 2)) + "%)")

            pDepo[pos['ticker']] = perf

        return (pDepo, pWarn)

    def depoRating(self, pc):
        # Find a rating based on percentage
        logi = self.getLogic()
        for l in logi.keys():
            if float(pc) <= logi[l]:
                return l
        return None

    def readCfg(self):
        with open(LongBot.CfgFile) as fp:
            for line in fp:
                ar = line.split("=", 1)
                self.props[ar[0].strip()] = ar[1].strip()

    def parseProfile(self, profile):
        self.profile = json.loads(profile)

    def getDepo(self):
        if self.profile and "depo" in self.profile:
            return self.profile["depo"]
        return None

    def getLogic(self):
        if self.profile and "logic" in self.profile:
            return self.profile["logic"]
        return None

    def get(self, key):
        if key in self.props:
            return self.props[key]
        return None

    def set(self, key, val):
        self.props[key] = val

    def __init__(self, name, profile):
        self.name = name
        self.props = {}
        self.readCfg()
        self.parseProfile(profile)
        self.sql = SQL()