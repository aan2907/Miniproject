import sys, os
import threading, shutil

import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk

import cv2
from PIL import Image, ImageTk

import yolosegment
import process

path=os.path.dirname(os.path.abspath(sys.argv[0]))
shutil.rmtree(os.path.join(path, 'runs', 'detect', 'predict'))

class CameraApp:
    def __init__(self, root):
        self.root = root
        root.title("ANPR System")
        width=400
        height=250
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        p=os.path.join(path, "bg.png")
        self.image = Image.open(p)
        self.image=self.image.resize((width, height))
        self.image = ImageTk.PhotoImage(self.image)
        bg_label = tk.Label(root, image=self.image).place(relwidth=1, relheight=1)
        #root.wm_attributes("-transparentcolor", "grey")

        self.model=None
        self.trainloc, self.scanloc, self.mod=tk.StringVar(), tk.StringVar(), tk.IntVar()
        # Initialize video path variable
        self.video_path, self.vidpathstr = None, StringVar()

        #Main Heading
        ft = tkFont.Font(family='Times',size=22)
        self.label1=tk.Label(root, font=ft,justify = LEFT, text = "ANPR")
        self.label1.place(x=135,y=10)

        # Create radio buttons to choose between camera or video
        ft = tkFont.Font(family='Times',size=10)
        self.label2=tk.Label(root,font = ft, justify=LEFT, text = "Feed :")
        self.label2.place(x=30,y=60)
        self.selection_var = tk.IntVar()
        self.camera_radio = tk.Radiobutton(root, text="Camera", variable=self.selection_var, value=1, command=self.enable_camera)
        self.camera_radio.place(x=80,y=60)
        self.video_radio = tk.Radiobutton(root, text="Video", variable=self.selection_var, value=2, command=self.enable_video)
        self.video_radio.place(x=160,y=60)

        # Create dropdown menu for camera devices
        self.device_var = tk.StringVar()
        self.device_label = tk.Label(root, text="Camera Device:")
        self.device_label.place(x=30,y=90)
        self.device_dropdown = tk.OptionMenu(root, self.device_var, *self.get_camera_devices())
        self.device_dropdown.place(x=120,y=90)

        #Get Video Path
        ft = tkFont.Font(family='Times',size=10)
        self.label2=tk.Label(root,font = ft, justify = LEFT, text = "Video Path : ")
        self.label2.place(x=30,y=135)

        self.path_entry=tk.Entry(root, font = ft, justify = LEFT, textvariable = self.vidpathstr)
        self.path_entry.place(x=120,y=135,width=150,height=30)

        self.invalid_label = tk.Label(root,font = tkFont.Font(family='Times',size=9), justify = LEFT)
        self.invalid_label.place(x=150, y=155)

        self.browse_button=tk.Button(root,font = ft, text = "Browse", cursor="hand2")
        self.browse_button.place(x=270,y=135,width=60,height=30)
        self.browse_button["command"] = self.browse_video

        # Create button to open camera feed or load video
        self.open_button = tk.Button(root, text="Open Camera Feed", command=self.analyse)
        self.open_button.place(x=30,y=185,width=120,height=30)

        #Quit Button
        self.quit_button = tk.Button(root, text="Quit", command=self.quit)
        self.quit_button.place(x=170,y=185,width=60,height=30)

    def process(self):
        process.process_segment()

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

    def open_source(self):
        segment=""
        selection = self.selection_var.get()
        if selection == 1:
            #self.open_camera()
            source = int(self.device_var.get().split()[1])
        elif selection == 2:
            #self.open_video()
            source=self.video_path
        yolosegment.segment(source)

    def analyse(self):
        self.source_thread = threading.Thread(target=self.open_source)
        self.process_thread = threading.Thread(target=self.process)
        self.source_thread.daemon, self.process_thread.daemon=True, True
        self.source_thread.start()
        self.process_thread.start()

    def quit(self):
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
