import csv
import pandas as pd
from datetime import datetime


def loginp(count, vnum, time):
    row= []
    data= [count, vnum, time]
    row.append(data)

    fname= "logs.csv"
    with open(fname, "a", newline="") as csvfile:
        csvw= csv.writer(csvfile)
        csvw.writerows(row)
        csvfile.close()
    printlog()    

def printlog():
    data= pd.read_csv("logs.csv")
    print(data)