import os, sys
import time

import validate
import ocr
import alertsystem

import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk

refreshrate=0.5
goodstring="All Good"

path=os.path.dirname(os.path.abspath(sys.argv[0]))
res_path=os.path.join(path, 'runs', 'detect', 'predict', 'crops', 'license-plate')


free=[True, True, True, True, True, True, True, True]
imagelist=[True, True, True, True, True, True, True, True]
reglist=[True, True, True, True, True, True, True, True]
statuslist=[True, True, True, True, True, True, True, True]

def process_segment(segment_path=res_path):
    root=tk.Tk()
    window=GUI(root)
    root.update()
    while True:
        refreshlock=False
        if not refreshlock:
            try:
                curr=os.listdir(segment_path)
            except FileNotFoundError:
                continue
            for segment in curr:
                if segment:
                    img = os.path.join(segment_path, segment)
                    platenum=ocr.runOcr(img)
                    if platenum:
                        valid = validate.validate(platenum)
                        if valid and valid not in reglist:
                            #print(valid)
                            root.update()
                            st = alertsystem.seandnot(valid)
                            status=st if st else goodstring
                            add(window, img, valid, status)
                
            #delete already processed images
            for i in curr:os.remove(os.path.join(segment_path, i))
        '''t=time.time()
        while time.time()-t<=refreshrate:
            root.update()
'''

def add(window, img, valid, status):
    print("Values to write, ", valid, status)
    global free, imagelist, reglist, statuslist

    image=Image.open(img)
    res = image.resize((100, 35))

    plateobjlist=[window.plate_label1, window.plate_label2, window.plate_label3, window.plate_label4, window.plate_label5, window.plate_label6, window.plate_label7, window.plate_label8]
    regobjlist=[window.reg_label1, window.reg_label2, window.reg_label3, window.reg_label4, window.reg_label5, window.reg_label6, window.reg_label7, window.reg_label8]
    statusobjlist=[window.status_label1, window.status_label2, window.status_label3, window.status_label4, window.status_label5, window.status_label6, window.status_label7, window.status_label8]
    foundslot=False

    for i in range(8):
        if free[i]==True:
            window.imgarr[i]=ImageTk.PhotoImage(res)
            #print("image:", window.imgarr[i])
            plateobjlist[i].config(image=window.imgarr[i])
            regobjlist[i].config(text=valid)
            statusobjlist[i].config(text=status)
            if status==goodstring:statusobjlist[i].config(fg='green')
            else:statusobjlist[i].config(fg='red')
            foundslot=True
            free[i], reglist[i], statuslist[i]=False, valid, status
            break
    if not foundslot:
        #Moving each plate one level up, discarding the first
        for i in range(7):
            plateobjlist[i].config(image=window.imgarr[i+1])
            regobjlist[i].config(text=reglist[i+1])
            statusobjlist[i].config(text=statuslist[i+1])

        '''free[7], imagelist[7]=True, None
        reglist, statuslist=reglist[1:] + [None], statuslist[1:] + [None]
        window.imgarr=window.imgarr[1:] + [None]
        print(free, reglist, statuslist, window.imgarr)'''
        
        window.imgarr[7]=ImageTk.PhotoImage(res)
        plateobjlist[7].config(image=window.imgarr[7])
        regobjlist[7].config(text=valid)
        statusobjlist[7].config(text=status)
        if status==goodstring:statusobjlist[7].config(fg='green')
        else:statusobjlist[7].config(fg='red')
        free[7], reglist[7], statuslist[7]=False, valid, status



class GUI:
    def __init__(self, root):
        #setting title
        root.title("Analysis")
        #setting window size
        width=520
        height=540
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.img1, self.img2, self.img3, self.img4, self.img5, self.img6, self.img7, self.img8=None, None, None, None, None, None, None, None,
        self.imgarr=[self.img1, self.img2, self.img3, self.img4, self.img5, self.img6, self.img7, self.img8]

        #x cordinates and width of all 4 columns for easy change
        x1,w1=0,70
        x2,w2=60, 165
        x3,w3=200, 100
        x4,w4=340, 140

        ft = tkFont.Font(family='Times',size=8)

        self.heading1_label=tk.Label(root)
        self.heading1_label["font"] = ft
        self.heading1_label["fg"] = "#333333"
        self.heading1_label["justify"] = LEFT
        self.heading1_label["text"] = "Plate"
        self.heading1_label.place(x=x2+20,y=20,width=w2-20,height=25)

        self.heading2_label=tk.Label(root)
        self.heading2_label["font"] = ft
        self.heading2_label["fg"] = "#333333"
        self.heading2_label["justify"] = LEFT
        self.heading2_label["text"] = "Registration"
        self.heading2_label.place(x=x3+20,y=20,width=w3,height=25)

        self.heading3_label=tk.Label(root)
        self.heading3_label["font"] = ft
        self.heading3_label["fg"] = "#333333"
        self.heading3_label["justify"] = LEFT
        self.heading3_label["text"] = "Status"
        self.heading3_label.place(x=x4+20,y=20,width=w4-20,height=25)

        tk.Label(root, font=ft, text="1").place(x=x1,y=70,width=w1,height=25)
        tk.Label(root, font=ft, text="2").place(x=x1,y=120,width=w1,height=25)
        tk.Label(root, font=ft, text="3").place(x=x1,y=170,width=w1,height=25)
        tk.Label(root, font=ft, text="4").place(x=x1,y=220,width=w1,height=25)
        tk.Label(root, font=ft, text="5").place(x=x1,y=270,width=w1,height=25)
        tk.Label(root, font=ft, text="6").place(x=x1,y=320,width=w1,height=25)
        tk.Label(root, font=ft, text="7").place(x=x1,y=370,width=w1,height=25)
        tk.Label(root, font=ft, text="8").place(x=x1,y=420,width=w1,height=25)

        self.plate_label1=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.plate_label1["font"] = ft
        self.plate_label1["fg"] = "#333333"
        self.plate_label1["justify"] = LEFT
        self.plate_label1.place(x=x2,y=70,width=w2,height=35)

        self.plate_label2=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.plate_label2["font"] = ft
        self.plate_label2["fg"] = "#333333"
        self.plate_label2["justify"] = LEFT
        self.plate_label2.place(x=x2,y=120,width=w2,height=35)

        self.plate_label3=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.plate_label3["font"] = ft
        self.plate_label3["fg"] = "#333333"
        self.plate_label3["justify"] = LEFT
        self.plate_label3.place(x=x2,y=170,width=w2,height=35)

        self.plate_label4=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.plate_label4["font"] = ft
        self.plate_label4["fg"] = "#333333"
        self.plate_label4["justify"] = LEFT
        self.plate_label4.place(x=x2,y=220,width=w2,height=35)

        self.plate_label5=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.plate_label5["font"] = ft
        self.plate_label5["fg"] = "#333333"
        self.plate_label5["justify"] = LEFT
        self.plate_label5.place(x=x2,y=270,width=w2,height=35)

        self.plate_label6=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.plate_label6["font"] = ft
        self.plate_label6["fg"] = "#333333"
        self.plate_label6["justify"] = LEFT
        self.plate_label6.place(x=x2,y=320,width=w2,height=35)

        self.plate_label7=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.plate_label7["font"] = ft
        self.plate_label7["fg"] = "#333333"
        self.plate_label7["justify"] = LEFT
        self.plate_label7.place(x=x2,y=370,width=w2,height=35)

        self.plate_label8=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.plate_label8["font"] = ft
        self.plate_label8["fg"] = "#333333"
        self.plate_label8["justify"] = LEFT
        self.plate_label8.place(x=x2,y=420,width=w2,height=35)

        self.reg_label1=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.reg_label1["font"] = ft
        self.reg_label1["fg"] = "#333333"
        self.reg_label1["justify"] = LEFT
        self.reg_label1.place(x=x3,y=70,width=w3,height=35)

        self.reg_label2=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.reg_label2["font"] = ft
        self.reg_label2["fg"] = "#333333"
        self.reg_label2["justify"] = LEFT
        self.reg_label2.place(x=x3,y=120,width=w3,height=35)

        self.reg_label3=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.reg_label3["font"] = ft
        self.reg_label3["fg"] = "#333333"
        self.reg_label3["justify"] = LEFT
        self.reg_label3.place(x=x3,y=170,width=w3,height=35)

        self.reg_label4=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.reg_label4["font"] = ft
        self.reg_label4["fg"] = "#333333"
        self.reg_label4["justify"] = LEFT
        self.reg_label4.place(x=x3,y=220,width=w3,height=35)

        self.reg_label5=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.reg_label5["font"] = ft
        self.reg_label5["fg"] = "#333333"
        self.reg_label5["justify"] = LEFT
        self.reg_label5.place(x=x3,y=270,width=w3,height=35)

        self.reg_label6=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.reg_label6["font"] = ft
        self.reg_label6["fg"] = "#333333"
        self.reg_label6["justify"] = LEFT
        self.reg_label6.place(x=x3,y=320,width=w3,height=35)

        self.reg_label7=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.reg_label7["font"] = ft
        self.reg_label7["fg"] = "#333333"
        self.reg_label7["justify"] = LEFT
        self.reg_label7.place(x=x3,y=370,width=w3,height=35)

        self.reg_label8=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.reg_label8["font"] = ft
        self.reg_label8["fg"] = "#333333"
        self.reg_label8["justify"] = LEFT
        self.reg_label8.place(x=x3,y=420,width=w3,height=35)

        self.status_label1=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.status_label1["font"] = ft
        self.status_label1["fg"] = "#333333"
        self.status_label1["justify"] = LEFT
        self.status_label1.place(x=x4,y=70,width=w4,height=35)

        self.status_label2=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.status_label2["font"] = ft
        self.status_label2["fg"] = "#333333"
        self.status_label2["justify"] = LEFT
        self.status_label2.place(x=x4,y=120,width=w4,height=35)

        self.status_label3=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.status_label3["font"] = ft
        self.status_label3["fg"] = "#333333"
        self.status_label3["justify"] = LEFT
        self.status_label3.place(x=x4,y=170,width=w4,height=35)

        self.status_label4=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.status_label4["font"] = ft
        self.status_label4["fg"] = "#333333"
        self.status_label4["justify"] = LEFT
        self.status_label4.place(x=x4,y=220,width=w4,height=35)

        self.status_label5=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.status_label5["font"] = ft
        self.status_label5["fg"] = "#333333"
        self.status_label5["justify"] = LEFT
        self.status_label5.place(x=x4,y=270,width=w4,height=35)

        self.status_label6=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.status_label6["font"] = ft
        self.status_label6["fg"] = "#333333"
        self.status_label6["justify"] = LEFT
        self.status_label6.place(x=x4,y=320,width=w4,height=35)

        self.status_label7=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.status_label7["font"] = ft
        self.status_label7["fg"] = "#333333"
        self.status_label7["justify"] = LEFT
        self.status_label7.place(x=x4,y=370,width=w4,height=35)

        self.status_label8=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.status_label8["font"] = ft
        self.status_label8["fg"] = "#333333"
        self.status_label8["justify"] = LEFT
        self.status_label8.place(x=x4,y=420,width=w4,height=35)

        # Create button to open camera feed or load video
        self.open_button = tk.Button(root, text="View Logs", command=self.view_logs)
        self.open_button.place(x=30,y=490,width=114,height=30)

        #Go Back Button
        self.quit_button = tk.Button(root, text="Go back", command=self.goback)
        self.quit_button.place(x=180,y=490,width=125,height=30)

    def view_logs(self):
        pass

    def shiftimg(self):
        new=self.imgarr[1:] + [None]
        return new

    def goback(self):
        sys.exit()

process_segment()
