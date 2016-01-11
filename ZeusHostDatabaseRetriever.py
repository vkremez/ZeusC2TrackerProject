#!/usr/bin/env python
# author = Vitali

import sqlite3 as lite

con = lite.connect('zeustrackerhosts.sqlite')
f = open('hosts.txt','w+')

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT name FROM Hosts")

    rows = cur.fetchall()

    for row in rows:
        print row
        
f.close()
