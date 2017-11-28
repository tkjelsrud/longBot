#!/usr/bin/python
from longbot import LongBot
from push import Push
import sys

if len(sys.argv) > 1:
    print("TEST123" + str(sys.argv))

    cnd = LongBot.fetch("daily")
    cnh = LongBot.fetch("hourly")

    if cnd > 0 and cnh > 0:
        bots = LongBot.loadBots("0")

        for b in bots:
            res, warn = b.calcDepo()
            print(str(res))

            for w in warn:
                print("Issue push " + str(w))
                Push.send(w)
    else:
        print("ERROR\tProblems with fetch")

else:
    print("No timer argument - exit")