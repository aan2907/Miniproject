import MySQLdb
from plyer import notification
import winsound
import pyttsx3

def sound(msg0, msg1):
    tts= pyttsx3.init()
    message= msg1 + " " + msg0
    tts.setProperty("rate", 120)
    tts.say(message)
    tts.startLoop()

def notify(msg):
    notification.notify(title= msg[1], message= "Number: " + msg[0] + "\nVehicle Type: " + msg[3] + "\nVehicle Model: " + msg[2], app_icon= None, timeout= 300)
    frequency= 2000
    duration= 900
    for i in range(2):
        winsound.Beep(frequency, duration)

    sound(msg[0], msg[1])

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
    notify(i)
    
db.close()