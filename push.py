import urllib3
import shelve

urllib3.disable_warnings()

class Push:
    Token = "X"
    User = "X"
    CacheFile = "push.cache"
    Cache = {}

    @staticmethod
    def send(message):
        Push.Cache = shelve.open(Push.CacheFile)

        cKey = message

        if cKey not in Push.Cache:
            #print(cKey + " was not in the chache?")
            http = urllib3.PoolManager()
            http.request('POST', "https://api.pushover.net/1/messages.json", fields={'token': Push.Token, 'user': Push.User, 'message': message})
            http.clear()
            Push.Cache[cKey] = True
            Push.Cache.close()

            return True
        return False
