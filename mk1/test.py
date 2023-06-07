import sqlite3

db='vehicles.db'
connect= sqlite3.connect(db) 
cur= connect.cursor()

cur.execute("CREATE TABLE CACHE(REGNO TEXT PRIMARY KEY, TIME DATETIME)")
connect.commit()