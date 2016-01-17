#!/usr/bin/env python
# Coded by Vitali
import urllib
import sqlite3
import re

u = urllib.urlopen('http://www.cybercrime-tracker.net/index.php?s=0&m=10000&search=zeus')

data = u.read().split('/>')

mdate = re.findall(r'<tr><td>([0-9-]{8,11})</td>', str(data))

url = re.findall(r'/latest-scan/http://(.{4,120})"', str(data))
for i in url:
	url = ' '.join(url).replace('" target="_blank','').split()
	
ip = re.findall(r'/ip-address/([0-9\.]{0,20})/information/', str(data))

rtype = []
for i in range(len(url)):
	i = 'Zeus'
	rtype.append(i) 
	
rsource = []
for i in range(len(url)):
	i = 'CyberCrimeTracker.net'
	rsource.append(i)

u2 = urllib.urlopen('https://zeustracker.abuse.ch/monitor.php?filter=all')
xdata = u2.read().split()

host = []
for line in xdata:
	if line.startswith('href="/monitor.php?host='):
		host.append(line.split('href="/monitor.php?host=')[1])
		host = ' '.join(host).replace('"','').split()

rdate = re.findall(r'"><td>([0-9-]{8,11})</td><td>', str(xdata))

malwr = re.findall(r'</td><td>(.{0,15})</td><td><a', str(xdata))

ips = re.findall(r'ipaddress=([0-9\.]{0,20})"', str(xdata))

bsource = []
for i in range(len(malwr)):
	i = 'ZeusTracker.ch'
	bsource.append(i)

mdate = mdate + rdate
url = url + host
ip = ip + ips
rtype = rtype + malwr
rsource = rsource + bsource

f = open('hosts.txt', 'w+')
for i in url:
	f.write(i+'\n')
f.close()

zipped = zip(mdate, url, ip, rtype, rsource)

conn = sqlite3.connect('ZeusC2Tracker.sqlite')
cur = conn.cursor()
conn.text_factory = str
# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS ZeusC2Tracker;
CREATE TABLE ZeusC2Tracker (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    mdate 	TEXT,
    url 	TEXT,
    ip    	TEXT,
    rtype 	TEXT,
    rsource  	TEXT
);
''')


for element in zipped:
	mdate = element[0]
	url = element[1]
	ip = element[2]
	rtype = element[3]
	rsource = element[4]

	cur.execute('''INSERT OR REPLACE INTO ZeusC2Tracker (mdate, url, ip, rtype, rsource) VALUES ( ?, ?, ?, ?, ? )''', ( mdate, url, ip, rtype, rsource ) )

conn.commit()
