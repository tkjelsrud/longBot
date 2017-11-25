DROP TABLE source;
CREATE TABLE source (name VARCHAR(20), url VARCHAR(200), frequency VARCHAR(10), handler VARCHAR(20));
INSERT INTO source (name, url, frequency, handler) VALUES('USDNOK', 'http://www.norges-bank.no/en/rss-feeds/US-dollar-USD---daily-exchange-rate-from-Norges-Bank/', 'daily', 'nbvalu');
INSERT INTO source (name, url, frequency, handler) VALUES('EURNOK', 'http://www.norges-bank.no/en/rss-feeds/Euro-EUR---daily-exchange-rate-from-Norges-Bank/', 'daily', 'nbvalu');
INSERT INTO source (name, url, frequency, handler) VALUES('QQQC', 'http://www.nasdaq.com/aspxcontent/NasdaqRSS.aspx?data=quotes&symbol=QQQC&', 'hourly', 'nasdaqrss');

DROP TABLE bot;
CREATE TABLE bot (name VARCHAR(20), hash VARCHAR(32), data VARCHAR(1000), updated timestamp not null default current_timestamp on update current_timestamp);
INSERT INTO bot (name, data) VALUES("ChinaBot", "{}")