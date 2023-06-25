import os, sys
import threading


try:
    import validate
    import ocr
    import alertsystem
except ModuleNotFoundError as e:
    print("Error(S):" + str(e) + "\nCheck if all script files are present in the same directory as main")
    exit(0)

import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

refreshrate=0.5
goodstring="All Good"

path=os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
res_path=os.path.join(path, 'runs', 'detect', 'predict', 'crops', 'license-plate')

def process_segment(segment_path=res_path, log=False):
    window=GUI()
    while True:
        try:
            curr=os.listdir(segment_path)
        except FileNotFoundError:
            continue
        for segment in curr:
            if segment:
                try:
                    img = os.path.join(segment_path, segment)
                    platenum=ocr.runOcr(img)
                    print(platenum)
                    valid = validate.validate(platenum)
                    if valid and valid not in window.reglist:
                        st = alertsystem.seandnot(valid, log=log)
                        status=st if st else goodstring
                        window.addrow(img, valid, status)
                except Exception as e:
                    print(e)
            
        #delete already processed images
        try:
            for i in curr:os.remove(os.path.join(segment_path, i))
        except PermissionError:
            pass


class GUI(threading.Thread):
    def __init__(self):
        self.imgarr, self.reglist, self.statuslist=[],[],[]
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        #self.root.quit()
        sys.exit()

    def run(self):
        self.root = tk.Tk()
        self.root.title("Analysis")
        width=650
        height=700
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, int(screenwidth/2), int((screenheight-height)/2))
        self.root.geometry(alignstr)

        columns = ("Reg. No", "Status")
        self.tree = ttk.Treeview(master=self.root)

        style = ttk.Style(master=self.root)
        style.configure("Treeview", rowheight=40)
        self.tree["columns"] = columns

        self.tree.heading("#0", text="Plate")
        for col in columns:
            self.tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(fill="both", expand=True)

        self.root.mainloop()

    def addrow(self, path, regno, status):
        with Image.open(path) as image:
            image = image.resize((100, 35))
            self.image = ImageTk.PhotoImage(master=self.root, image=image)
        self.imgarr.append(self.image)
        self.reglist.append(regno)
        self.statuslist.append(status)
        self.tree.insert(parent='', index=tk.END, image=self.image, values=(regno, status))
        self.tree.pack(fill="both", expand=True)

