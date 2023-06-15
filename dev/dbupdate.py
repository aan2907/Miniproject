import sqlite3

db="vehicles.db"
connect= sqlite3.connect(db) 
c= connect.cursor()

c.execute("insert into blacklists(regno,offence,model,vtype)values('KL01AW1505','Stolen Vehicle','Maruti WagonR','Car')")
c.execute("insert into blacklists(regno,offence,model,vtype)values('KL33H7780','Fine Unpaid','Activa','Two Wheeler')")
c.execute("insert into blacklists(regno,offence,model,vtype)values('KL33J8150','Overloading','Bajaj Auto','Auto')")
c.execute("insert into blacklists(regno,offence,model,vtype)values('KL15A1022','Hit and Run','KSRTC','Bus')")
c.execute("insert into blacklists(regno,offence,model,vtype)values('KL67C0184','Armed Robbery','Maruti Alto','Car')")
c.execute("insert into blacklists(regno,offence,model,vtype)values('KL01AV1505','Hit and Run','WagonR','Car')")

c.execute("Select * from blacklists")
print(c.fetchall())
connect.commit()
connect.close()
