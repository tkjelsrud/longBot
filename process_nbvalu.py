#!/usr/bin/python
import re

class Processor:
    def process(data):
        res = {}

        m = re.search("exchange_rates/currency/([A-Za-z]+)", data)
        if m:
            res['ticker'] = m.group(1)
        else:
            res['ticker'] = None

        m = re.search("1 [A-Z]+ = ([0-9]+\\.[0-9]+) NOK", data)
        if m:
            res['last'] = m.group(1)
        else:
            res['last'] = None

        if res['last'] is not None and res['ticker'] is not None:
            res['valid'] = True

        return res