import xml.etree.ElementTree as ET
import re
import math
from datetime import datetime, timezone
import dateutil.parser as dparser

class Sentiment:
    DictFile = "sentiment.dictionary"
    Dict = {}

    def parseRss(self, rssFile):
        tree = ET.parse(rssFile)
        channel = tree.getroot()[0]
        score = 0
        for item in channel.findall('item'):
            s = self.scoreTitle(item.find('title').text)
            s = s * self.scoreDate(item.find('pubDate').text)
            #print(item.find('title').text + "\t" + item.find('pubDate').text + "\t" + str(s))
            score = score + s
            #itr = itr + 1
        return score

    def scoreTitle(self, title):
        # Temp create a table here
        s = 0
        for p, v in Sentiment.Dict.items():
            if title.lower().find(p) >= 0:
                s = s + v
        return s

    def scoreDate(self, date):
        dt = dparser.parse(date,fuzzy=True)
        delta = datetime.now(timezone.utc) - dt
        if delta.days > 100:
            return 0
        return math.log(delta.days) / 10.

    @staticmethod
    def LoadDict():
        if len(Sentiment.Dict) == 0:
            fp = open(Sentiment.DictFile,'r')
            data = fp.readlines()
            fp.close()
            for l in data:
                if len(l.strip()) > 0:
                    sc, phr = l.strip().split(" ", 1)
                    phrList = re.split(",", phr)

                    for p in phrList:
                        Sentiment.Dict[p.strip().lower()] = float(sc)

    def __init__(self):
        Sentiment.LoadDict()