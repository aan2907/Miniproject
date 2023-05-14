import MySQLdb
from plyer import notification
import winsound

def notify(msg):
    notification.notify(title= "Alert", message= msg, app_icon= None, timeout= 50)
    frequency= 2000
    duration= 900
    for i in range(4):
        winsound.Beep(frequency, duration)

num= "KL01BH8776"
f= 0

db= MySQLdb.connect("localhost","root","admin","anpr" )
cursor= db.cursor()

cursor.execute("Select * from vehiclelist")
details= cursor.fetchall()

for i in details:
    if num == i[0]:
        f= 1
        break

        
if f == 1:
    notify(i[1])
    
db.close()