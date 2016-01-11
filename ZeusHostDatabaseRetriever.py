#!/usr/bin/env python
# author = Vitali
# -*- coding: iso-8859-15 -*-
import sqlite3 as lite

con = lite.connect('zeustrackerhosts.sqlite')
f = open('hosts.txt','w+')

with con:    
    cur = con.cursor()    
    cur.execute("SELECT name FROM Hosts")
    rows = cur.fetchall()
    for row in rows:
        f.write(' '.join(row) + '\n')
 
f.close()
