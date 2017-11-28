import unittest

class TestLongBot(unittest.TestCase):

    def test_create(self):
        from longbot import LongBot
        lb = LongBot("Test", '{"depo": [{"ticker": "QQQC", "count": 100, "at": "USD32.63", "cost": "NOK26875.24"}]}')
        self.assertTrue(len(lb.props.keys()) > 0)

    def test_sql(self):
        from longbot import LongBot
        lb = LongBot("Test", "{}")
        #lb.sqlConnect()

        self.assertTrue(len(lb.props.keys()) > 0)

    def test_sqlFetch(self):
        from longbot import LongBot
        lb = LongBot("Test", "{}")
        #Creates too many requests

        #lb.sqlConnect()
        #lb.fetch("daily")
        #self.assertTrue(len(lb.props.keys()) > 0)

    def test_sqlGetBots(self):
        from longbot import LongBot
        list = LongBot.loadBots("0")
        self.assertTrue(len(list) > 0)

    def test_processNasdaqRss(self):
        import importlib
        Processor = getattr(importlib.import_module("process_nbvalu"), "Processor")
        Processor = getattr(importlib.import_module("process_nasdaqrss"), "Processor")

        data = ""
        fp = open("process_nasdaqrss.testdata",'r')
        data = fp.read()
        fp.close()
        self.assertTrue(len(data) > 100)
        res = Processor.process(data)
        self.assertEqual(res['ticker'], "qqqc")
        self.assertEqual(res['last'], "32.178")
        self.assertEqual(res['time'], "13:00:00")
        self.assertEqual(res['date'], "2017-11-24")

    def test_processNorgesBankEUR(self):
        import importlib
        Processor = getattr(importlib.import_module("process_nbvalu"), "Processor")
        data = ""
        fp = open("process_nbvalu.testdata",'r')
        data = fp.read()
        fp.close()
        self.assertTrue(len(data) > 100)
        res = Processor.process(data)
        self.assertEqual(res['ticker'], "EUR")
        self.assertEqual(res['last'], "9.6608")
        self.assertEqual(res['time'], "15:01:00")
        self.assertEqual(res['date'], "2017-11-24")

    def test_insertTickerData(self):
        from sql import SQL
        s = SQL()
        s.connect()
        r = s.insertTickerData("TEST", 123.34, 1000, "2017-11-24 13:00:00")
        s.close()

        self.assertEqual(r, 1)

    def test_valueChain(self):
        from longbot import LongBot
        from push import Push

        LongBot.cacheData()

        cn = LongBot.fetch("daily")
        self.assertTrue(cn > 0)

        if LongBot.fetch("hourly"):
            bots = LongBot.loadBots("0")

            for b in bots:
                res, warn = b.calcDepo()

                for w in warn:
                    Push.send(w)
        else:
            print("Unable to fetch")

        LongBot.closeCache()

    def test_pushover(self):
        from push import Push

        # Uncomment to send push message, will only send once if cached
        Push.send("Test message 123")

if __name__=='__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise