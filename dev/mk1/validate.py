import re
import sqlite3
from datetime import datetime


def normalise(reading):
    regcodes=['AP', 'AR', 'AS', 'BR', 'CG', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OD', 'PB', 'RJ', 'SK', 'TN', 'TR', 'UP', 'UK', 'WB', 'TS', 'AN', 'CH', 'DN', 'DD', 'LD', 'DL', 'PY']
    reading=reading.upper()
    reading = re.sub(r"[ \n\-\.\_]", "", reading)
    for i in regcodes:
        plate = i + r'\s*\d{1,2}\s*[A-Z]{1,2}\s*\d{1,4}'
        plate=re.compile(plate)
        matchfound=re.findall(plate, reading)
        if matchfound:
            return matchfound[0]

def updatecache(conobj, curobj, plateval):
    curobj.execute("Select * from {}".format('cache'))
    cache=[i[0] for i in curobj.fetchall()]
    time=datetime.now()
    if plateval and plateval not in cache:
        curobj.execute("insert into cache values(?, ?)", (plateval, time))
        print('cache updated')
        conobj.commit()
        return plateval
    else:return None
    
def validate(text, database='vehicles.db'):
    connect= sqlite3.connect(database) 
    cur= connect.cursor()
    plate=normalise(text)
    if plate:
        res = updatecache(connect, cur, plate)
        return res
    else: return None

