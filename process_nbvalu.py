#!/usr/bin/python
import re

class Processor:
    def process(data):
        res = {}

        m = re.search("exchange_rates/currency/([A-Za-z]+)", data)
        res['ticker'] = None
        if m:
            res['ticker'] = m.group(1)

        m = re.search("1 [A-Z]+ = ([0-9]+\\.[0-9]+) NOK", data)
        res['last'] = None
        if m:
            res['last'] = m.group(1)

        m = re.search("([0-9]{2}:[0-9]{2}:[0-9]{2}) GMT", data)
        res['time'] = None
        if m:
            res['time'] = m.group(1)

        m = re.search("([0-9]{4}-[0-9]{2}-[0-9]{2})", data)
        res['date'] = None
        if m:
            res['date'] = m.group(1)

        if res['last'] is not None and res['ticker'] is not None:
            res['valid'] = True

        return res