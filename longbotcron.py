#!/usr/bin/python
from longbot import LongBot

import sys

if len(sys.argv) > 1:
    lb = LongBot()
    print("Running fetch: " + sys.argv[1])
    lb.fetch(sys.argv[1])
else:
    print("No timer argument - exit")