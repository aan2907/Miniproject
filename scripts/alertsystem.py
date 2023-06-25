import os, sys
import sqlite3
try:
    from datetime import datetime
    from plyer import notification
    import winsound
    import pyttsx3
except ModuleNotFoundError as e:
    print("Error(S):" + str(e) + "\nUse \"pip install -r requirements.txt\"")
    exit(0)



path=os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
path=os.path.join(path, "db")

def sound(msg0, msg1):
    tts= pyttsx3.init()
    message= msg1 + " " + msg0
    tts.setProperty("rate", 120)
    tts.say(message)
    tts.runAndWait()

def notify(msg):
    notification.notify(title= msg[1], message= "Number: " + msg[0] + "\nVehicle Type: " + msg[3] + "\nVehicle Model: " + msg[2], app_icon= None, timeout= 100)
    frequency= 2000
    duration= 900
    for i in range(2):
        winsound.Beep(frequency, duration)
    sound(msg[0], msg[1])

def seandnot(vnum, db="vehicles.db",log=False, offendtablename= "blacklists", logtablename= "logs"):
    connect= sqlite3.connect(os.path.join(path, db)) 
    c= connect.cursor()
    c.execute("Select * from {}".format(offendtablename))
    details= c.fetchall()
    offense=None

    for i in details:
        if vnum == i[0]:
            notify(i)
            log=True
            offense=i[1]
            break
            
    if log:
        c.execute("SELECT * from {}".format(logtablename))
        count= len(c.fetchall())+1
        time= datetime.now()
        c.execute("INSERT INTO {} VALUES(?, ?, ?)".format(logtablename),(count, vnum, time))
    
    connect.commit()
    connect.close()
    return offense
