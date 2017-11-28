DROP TABLE IF EXISTS source;
CREATE TABLE source (name VARCHAR(20), url VARCHAR(200), frequency VARCHAR(10), handler VARCHAR(20));
INSERT INTO source (name, url, frequency, handler) VALUES('USDNOK', 'http://www.norges-bank.no/en/rss-feeds/US-dollar-USD---daily-exchange-rate-from-Norges-Bank/', 'daily', 'nbvalu');
INSERT INTO source (name, url, frequency, handler) VALUES('EURNOK', 'http://www.norges-bank.no/en/rss-feeds/Euro-EUR---daily-exchange-rate-from-Norges-Bank/', 'daily', 'nbvalu');
INSERT INTO source (name, url, frequency, handler) VALUES('QQQC', 'http://www.nasdaq.com/aspxcontent/NasdaqRSS.aspx?data=quotes&symbol=QQQC&', 'hourly', 'nasdaqrss');

DROP TABLE IF EXISTS bot;
CREATE TABLE bot (name VARCHAR(20), hash VARCHAR(32), data VARCHAR(1000), updated timestamp not null default current_timestamp on update current_timestamp);
INSERT INTO bot (name, hash, data) VALUES("ChinaBot", "0", '{"depo": [{"ticker": "QQQC", "count": 100, "at": "USD32.63", "cost": "NOK26875.24", "fees": "NOK99", "date": "24.11.2017", "rating": "B"}], "logic": {"FFF": -30, "FF": -20, "F": -15, "E": -10, "D": -7, "C": 0, "B": 5, "A": 10, "AA": 15, "AAA": 20}, "currLogic": {"C": -2, "B": 0, "A": 2}}');

DROP TABLE IF EXISTS data;
CREATE TABLE data (name VARCHAR(20), data VARCHAR(10000), updated timestamp not null default current_timestamp on update current_timestamp);