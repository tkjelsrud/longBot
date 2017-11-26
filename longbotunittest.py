import unittest

class TestLongBot(unittest.TestCase):

    def test_create(self):
        from longbot import LongBot
        lb = LongBot()
        self.assertTrue(len(lb.props.keys()) > 0)

    def test_sql(self):
        from longbot import LongBot
        lb = LongBot()
        #lb.sqlConnect()

        self.assertTrue(len(lb.props.keys()) > 0)

    def test_sqlFetch(self):
        from longbot import LongBot
        lb = LongBot()
        #Creates too many requests

        #lb.sqlConnect()
        #lb.fetch("daily")
        #self.assertTrue(len(lb.props.keys()) > 0)

    def test_processNasdaqRss(self):
        import process_nasdaqrss
        data = ""
        fp = open("process_nasdaqrss.testdata",'r')
        data = fp.read()
        fp.close()
        self.assertTrue(len(data) > 100)
        res = process_nasdaqrss.Processor.process(data)
        self.assertEqual(res['ticker'], "qqqc")
        self.assertEqual(res['last'], "32.178")

    def test_processNorgesBankEUR(self):
        import process_nbvalu
        data = ""
        fp = open("process_nbvalu.testdata",'r')
        data = fp.read()
        fp.close()
        self.assertTrue(len(data) > 100)
        res = process_nbvalu.Processor.process(data)
        self.assertEqual(res['ticker'], "EUR")
        self.assertEqual(res['last'], "9.6608")

if __name__=='__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise