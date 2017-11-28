#!/usr/bin/python
import re
from dateutil import parser

class Processor:
    def process(data):
        res = {'valid': False}

        m = re.search("symbol/([a-z]+)", data)
        if m:
            res['ticker'] = m.group(1)
        else:
            res['ticker'] = None

        m = re.search(">([0-9]+\\.[0-9]+)", data)
        if m:
            res['last'] = m.group(1)
        else:
            res['last'] = None

        m = re.search("([0-9]{2}:[0-9]{2}:[0-9]{2})", data)
        res['time'] = None
        if m:
            res['time'] = m.group(1)

        m = re.search("([0-9]+ [A-Za-z]{3} [0-9]{4})", data)
        res['date'] = None
        if m:
            res['date'] = m.group(1)
            dt = parser.parse(res['date'])
            res['date'] = dt.strftime('%Y-%m-%d')

        if res['last'] is not None and res['ticker'] is not None:
            res['valid'] = True

        return res
