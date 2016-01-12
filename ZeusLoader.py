#!/usr/bin/env python
# Coded by Vitali

import urllib
import sqlite3
u = urllib.urlopen('https://zeustracker.abuse.ch/monitor.php?filter=all')
data = u.read().split()

host = []
for line in data:
	if line.startswith('href="/monitor.php?host='):
		host.append(line.split('href="/monitor.php?host=')[1])
		host = ' '.join(host).replace('"','').split()

f = open('hosts.txt', 'r+')
for i in host:
	f.write(i+'\n')
f.close()
rdate = []
for line in data:
	if line.startswith('bgcolor="#FFFFFF"><td>'):
		rdate.append(line[22:32])
		# rdate = ' '.join(rdate).split()

malwr = []
for line in data:
	if line.startswith('bgcolor="#FFFFFF"><td>'):
		 malwr.append(line.split('</td><td>')[1])

zipped = zip(rdate, malwr, host)
print zipped

conn = sqlite3.connect('zeustrackerhosts.sqlite')
cur = conn.cursor()
conn.text_factory = str
# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Hosts;
CREATE TABLE Hosts (
id  		INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
mdate 		TEXT,
malware 	TEXT,
name    	TEXT UNIQUE
);
''')

for element in zipped:
	mdate = element[0]
	malware = element[1]
	name = element[2]

	cur.execute('''INSERT OR REPLACE INTO Hosts (mdate, malware, name) VALUES ( ?, ?, ? )''', ( mdate, malware, name ) )

conn.commit()
