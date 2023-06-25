import sys, os
import threading, shutil
import sqlite3
import subprocess
import time

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont

try:
    import cv2
    from ultralytics import YOLO
except ModuleNotFoundError as e:
    print("Error(S):" + str(e) + "\nUse \"pip install -r requirements.txt\"")
    exit(0)

try:
    import process
except ModuleNotFoundError as e:
    print("Error(S):" + str(e) + "\nCheck if all script files are present in the same directory as main")
    exit(0)

#All relevent paths
path=os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
db=os.path.join(path, 'db')
models=os.path.join(path, "models")
vidrun=os.path.join(path, "runs", "detect", "predict")
runs=os.path.join(path, "runs", "detect", "predict", "crops", "license-plate")
modelpath=os.path.join(models, "best.pt")
dbpath=os.path.join(db, 'vehicles.db')

#Editable parameters
#Default:
#conf=0.75
#frame_stride=4
#viddelay=0.2
#live_detection=False

conf=0.75
frame_stride=4
viddelay=0.2
live_detection=False

#Delete any pre existing runs data
def deleteruns():
    try:
        shutil.rmtree(os.path.join(path, 'runs', 'detect', 'predict'))
    except FileNotFoundError:
        pass

#Main Class
class MainWindow():
    def __init__(self, root, conf=0.75, frame_stride=4, viddelay=0.2):
        self.root = root
        root.title("ANPR System")
        self.width=650
        self.height=700
        self.screenwidth = root.winfo_screenwidth()
        self.screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, int((self.screenwidth/2)-self.width), int((self.screenheight-self.height)/2))
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        canvas=Canvas(root, width=self.width, height=self.height)
        canvas.place(x=0, y=0)
        padding=5
        canvas.create_rectangle(padding, padding+self.height/2,self.width-2*padding+2,self.height-2*padding+2)

        # Initialize video path variable
        self.video_path, self.vidpathstr = None, StringVar()
        self.log=IntVar(value=1)
        self.selection_var = tk.IntVar()
        self.device_var = tk.StringVar()
        self.conf, self.frame_stride, self.viddelay=conf, frame_stride, viddelay
        self.live_detection=live_detection
        self.vid_name=''

        #Main Heading
        ft = tkFont.Font(family='Times',size=10)
        Label(root, font=ft,justify = LEFT, text = "Main Menu : ").place(x=2*padding, y=2*padding)

        # Create radio buttons to choose between camera or video
        ft = tkFont.Font(family='Times',size=10)
        tk.Label(root,font = ft, justify=LEFT, text = "Feed :").place(x=50,y=80,width=70,height=25)
        
        tk.Radiobutton(root, text="Camera", variable=self.selection_var, value=1, command=self.enable_camera).place(x=120,y=70,width=85,height=25)
        tk.Radiobutton(root, text="Video", variable=self.selection_var, value=2, command=self.enable_video).place(x=115,y=95,width=85,height=25)

        # Create dropdown menu for camera devices
        tk.Label(root, text="Camera Device:").place(x=50,y=140,width=87,height=30)
        self.device_dropdown = tk.OptionMenu(root, self.device_var, *self.get_camera_devices())
        self.device_dropdown.place(x=150,y=140,width=150,height=25)

        #Get Video Path
        self.source_label = tk.Label(root,font = ft, justify = LEFT, text = "Video Path : ")
        self.source_label.place(x=50,y=200,width=70,height=25)
        self.source_entry = tk.Entry(root, font = ft, justify = LEFT, textvariable = self.vidpathstr)
        self.source_entry.place(x=130,y=200,width=285,height=30)

        self.invalid_label = tk.Label(root,font=tkFont.Font(family='Times',size=9), justify = LEFT)
        self.invalid_label.place(x=150, y=155)

        self.browse_button=tk.Button(root,font = ft, text = "Browse", cursor="hand2", command=self.browse_video)
        self.browse_button.place(x=410,y=200,width=82,height=30)

        # Create button to open camera feed or load video
        self.open_button = tk.Button(root, text="Open Camera Feed", command=self.analyse)
        self.open_button.place(x=50,y=260,width=126,height=30)

        #View logs
        tk.Label(root, font=ft, text="Logs : ").place(x=390,y=50)
        tk.Checkbutton(root, text="Add to logs", variable=self.log).place(x=420,y=80,width=70,height=25)
        tk.Button(root, text="View Logs", command=self.viewlogs).place(x=415,y=110,width=83,height=30)
        canvas.create_rectangle(389, 55, 533, 160)

        #Quit Button
        tk.Button(root, text="Quit", command=self.quit).place(x=200,y=260,width=112,height=30)

        #Videostatus label
        tk.Label(root, font=ft, text="Feed : ").place(x=2*padding, y=2*padding+int(self.height/2))
        ft = tkFont.Font(family='Times',size=15)
        self.status_label=tk.Label(root,font = ft, justify = LEFT)
        self.status_label.place(x=int(self.width/2)-100,y=int(0.75*self.height)-50)


    def enable_camera(self):
        self.device_dropdown.configure(state=tk.NORMAL)
        self.open_button.config(text="Open Camera Feed")
        self.browse_button.config(state=DISABLED)

    def enable_video(self):
        self.device_dropdown.configure(state=tk.DISABLED)
        self.open_button.config(text="Open Video")
        self.browse_button.config(state=NORMAL)

    def browse_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
        self.vid_name = os.path.basename(file_path)
        self.vidpathstr.set(file_path) 
        self.video_path = file_path

    def get_camera_devices(self):
        # Get available camera devices using OpenCV
        devices = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                devices.append(f"Camera {i}")
                cap.release()
        return devices

    def playvideo(self, path, delay, width=650, height=350):
        video = cv2.VideoCapture(path)
        cv2.namedWindow("Feed", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Feed", int((self.screenwidth/2)-self.width), int(self.screenheight/2))
        cv2.resizeWindow("Feed", width, height)
        while True:
            ret, frame = video.read()
            if not ret:
                break
            cv2.imshow("Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(delay)
        video.release()
        cv2.destroyAllWindows()

    def process(self):
        log=self.log.get()
        if log==1:
            process.process_segment(runs, log=True)
        else:
            process.process_segment(runs)

    def analyse(self):
        selection = self.selection_var.get()
        source=self.video_path
        if selection == 2 and not self.live_detection:
            self.status_label.config(text="Detection Model Running...")
            source=self.video_path
            self.platedetect(source,livedet=False, modelpath=modelpath)
            self.source_thread = threading.Thread(target=lambda:self.playvideo(os.path.join(vidrun, self.vid_name), self.viddelay))
            self.status_label.config(text="")
        else:
            if selection == 1:
                self.live_detection=True
                source = int(self.device_var.get().split()[1])
            self.source_thread = threading.Thread(target=lambda:self.platedetect(source, livedet=True, modelpath=modelpath))

        self.process_thread = threading.Thread(target=self.process)
        self.source_thread.daemon=True
        self.process_thread.daemon=True
        self.source_thread.start()
        self.process_thread.start()

    def platedetect(self, source, livedet=False,modelpath=modelpath):
        if livedet:
            model= YOLO(modelpath)
            cap = cv2.VideoCapture(source)
            while cap.isOpened():
                success, frame = cap.read()
                if success:
                    results = model(frame, classes=0, save_crop=True)
                    annotated_frame = results[0].plot()
                    cv2.namedWindow("Feed", cv2.WINDOW_NORMAL)
                    cv2.moveWindow("Feed", int((self.screenwidth/2)-self.width), int(self.screenheight/2))
                    cv2.resizeWindow("Feed", self.width, int(self.height/2))
                    cv2.imshow("Feed", annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()
        else:
            command = f'yolo task=detect mode=predict model={modelpath} save=True conf={self.conf} source={self.video_path} classes=0 vid_stride={self.frame_stride} save_crop=True'
            subprocess.check_output(command, shell=True, encoding='utf-8')
            
    def viewlogs(self, db=dbpath, logtablename="logs"):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {}".format(logtablename))
        rows = cursor.fetchall()

        window = tk.Tk()
        window.title("Logs")
        width, height=self.width, self.height
        screenwidth, screenheight=self.screenwidth, self.screenheight
        alignstr = '%dx%d+%d+%d' % (width, height, int(screenwidth/2), int((screenheight-height)/2))
        window.geometry(alignstr)

        tree = ttk.Treeview(window)
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        tree["show"] = "headings"  # Hide the default first empty column

        columns = ("SLNO", "VEHICLE REGISTRATION", "TIME")
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)
        window.mainloop()

    def quit(self):
        sys.exit()


if __name__ == "__main__":
    deleteruns()
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
