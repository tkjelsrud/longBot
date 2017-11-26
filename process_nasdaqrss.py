#!/usr/bin/python
import re
from longbot import LongBot

class Processor:
    def process(data):
        res = {'valid': False}

        m = re.search("symbol/([a-z]+)", data)
        if m:
            res['ticker'] = m.group(1)
        else:
            res['ticker'] = None

        m = re.search("([0-9]+\\.[0-9]+)\n", data)
        if m:
            res['last'] = m.group(1)
        else:
            res['last'] = None

        if res['last'] is not None and res['ticker'] is not None:
            res['valid'] = True

        return res

    def calculate(bot):
        for pos in bot['depo']:
            # Calculate value of position vs original cost
            print(pos['ticker'] + " " + str(pos['count']))
        return None