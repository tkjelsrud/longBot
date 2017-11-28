import unittest

class TestSentiment(unittest.TestCase):
    def test_sentimentDict(self):
        from sentiment import Sentiment
        s = Sentiment()
        self.assertTrue(len(Sentiment.Dict) > 0)

        self.assertTrue(s.scoreTitle("stocks down") < 0.0)
        self.assertTrue(s.scoreTitle("opening up") > 0.0)

        self.assertTrue(s.scoreDate("Mon, 04 Jan 2017 07:54:27 -0400") == 0.0)

    def test_sentiment(self):
        from sentiment import Sentiment

        s = Sentiment()
        score = s.parseRss("sentiment.testdata")
        #print(str(score))
        self.assertTrue(score < 0.0)

if __name__=='__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise