import re

def process(data):
    res = {}

    m = re.search("symbol/([a-z]+)", data)
    if m:
        res['ticker'] = m.group(1)
    else:
        res['ticker'] = None

    m = re.search("([0-9]+\.[0-9]+)\n", data)
    if m:
        res['last'] = m.group(1)
    else:
        res['last'] = None

    return res