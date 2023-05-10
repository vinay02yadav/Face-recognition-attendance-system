import tkinter as tk
from tkinter import *
from tkinter import messagebox
import cv2
import os

import numpy as np
from PIL import Image, ImageTk
import datetime

from pydoc import classname
import pandas
from cv2 import *
import face_recognition
from datetime import datetime
import requests

from sms import *

window = tk.Tk()
window.title("Face_Recogniser")
window.configure(background='white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

message = tk.Label(
	window, text="Face-Recognition-System",
	bg="#6518AC", fg="white", width=50,
	height=3, font=('times', 30, 'bold'))

message.place(x=180, y=20)


# *** this images folder must only contain images only ***
path = r"C:\Users\02vya\OneDrive\Desktop\face-recognition\images"  # this is the path of images which I use in this program

images = []
classname = []
namelist = []
namelist_sms = []
# namelist2 = []
mylist = os.listdir(path)
print(mylist)  # this will print all file name in a list present in path directry. Example:- ["myphoto.jpg" , "yourphoto.jpg"]

for cl in mylist:
    curimg = cv2.imread(f"{path}/{cl}")
    images.append(curimg)
    classname.append(os.path.splitext(cl)[0])

print(classname)  # this will only print the file name without any extension. Example:- ["myphoto","yourphoto"]

# this function return encodings of the face images which is present in our path
encodelist = []

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def findencoding(images):
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)

    return encodelist


def login():
    newWindow = Toplevel(window)
    newWindow.title("LOGIN")
    newWindow.geometry("350x300")
    newWindow.resizable(False, False)
    newWindow.configure(bg='#333333')

    login_label = tk.Label(
        newWindow, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))

    password_entry = tk.Entry(newWindow, show="*", font=("Arial", 16),width=8)
    password_label = tk.Label(
        newWindow, text="Enter Password :", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    login_button = tk.Button(
        newWindow, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=lambda:[send_detail(password_entry.get())])

    login_label.place(x=120,y=20)
    password_label.place(x=120,y=100)
    password_entry.place(x=120,y=150)
    login_button.place(x=120,y=210)


    newWindow.mainloop()

def send_detail(password):
    if password == 'ece':
        send_sms()
    else:
        messagebox.showerror(title="Incorrect Password", message="You password is Incorrect.")
        login()

def send_sms():
    url = "https://us.sms.api.sinch.com/xms/v1/" + servicePlanId + "/batches"

    f = open(r"C:\Users\02vya\OneDrive\Desktop\face-recognition\attendance.txt",'r')
    mydatalist = f.read()
    payload = {"from": sinchNumber,"to": [toNumber],"body": f"{mydatalist}"}

    headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + apiToken
            }

    response = requests.post(url, json=payload, headers=headers)
    print("sms sent")
    open("attendance.txt", "w").close()
    window.destroy()

def markattendance(name):

    f = open(r"C:\Users\02vya\OneDrive\Desktop\face-recognition\attendance.txt",'r')
    mydatalist = f.read()

    f.seek(0)
    count=mydatalist.count("\n")

    for i in range(count+1):
        line = f.readline()
        line=line.replace('\n','')

        entry = line.split(",")
        namelist.append(entry[0])

    if name not in namelist:
        now = datetime.now()
        dtstr = now.strftime("%H:%M:%S")
        f = open(r"C:\Users\02vya\OneDrive\Desktop\face-recognition\attendance.txt",'a')
        f.writelines(f"\n{name},{dtstr}")

        message = tk.Label(
	    window, text=f"{name} : Present",
	    bg="green", fg="white", width=30,
	    height=3, font=('times', 20, 'bold'))
        message.place(x=540, y=570)
    else:
        message = tk.Label(
	    window, text=f"{name} : Already Present",
	    bg="green", fg="white", width=30,
	    height=3, font=('times', 20, 'bold'))
        message.place(x=540, y=570)


encodelistknown = findencoding(images)
print("encoding complete")

print("starting")
cap = cv2.VideoCapture(0)

label_widget = Label(window,width=410,height=320,borderwidth=4, relief="solid")
label_widget.place(x=555, y=200)

def star():
    takeImg = tk.Button(window, text="Start",
					command=start, fg="white", bg="#6518AC",
					width=20, height=3, activebackground="Red",state=tk.DISABLED,
					font=('times', 15, ' bold '))
    takeImg.place(x=200, y=500)

def start():

    if cap.isOpened() == False:
        print("Error opening video stream or file")

    else:
        window.configure(bg='#333333')
        _, frame = cap.read()
        # Convert image from one color space to other
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Capture the latest frame and transform to image9
        captured_image = Image.fromarray(opencv_image)

        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)

        # Displaying photoimage in the label
        label_widget.photo_image = photo_image

        # Configure image in the label
        label_widget.configure(image=photo_image)

    # # Repeat the same process after every 10 seconds
        label_widget.after(10, start)



def takephoto():
        print("taking photo ...")
        success, img = cap.read()

        if not success:
            print("failed to capture image")
        
        imgs = cv2.resize(
            img, (0, 0), None, 0.25, 0.25
        )  # resizing to a smaller image to get fast results.
        imgs = cv2.cvtColor(
            img, cv2.COLOR_RGB2BGR
        )  # converting image to black&white image to process easily

        print("image capture and resizing complete")

        facecurframe = face_recognition.face_locations(
            imgs, number_of_times_to_upsample=0, model="cnn"
        )
        encodingcurframe = face_recognition.face_encodings(imgs, facecurframe)

        print("encodingcurframe complete")

        for encodeface, faceloc in zip(encodingcurframe, facecurframe):
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            facedis = face_recognition.face_distance(encodelistknown, encodeface)
            matchindex = np.argmin(facedis)

            try:
                name = classname[matchindex].upper()
                markattendance(name)  
 
            except:
                message = tk.Label(
                window, text=f"{name} : Not Found",
                bg="green", fg="white", width=20,
                height=3, font=('times', 15, 'bold'))
                message.place(x=540, y=570)

takeImg = tk.Button(window, text="Start",
					command= lambda:[start(), star()], fg="white", bg="#6518AC",
					width=20, height=3, activebackground="Red",
					font=('times', 15, ' bold '))
takeImg.place(x=200, y=500)

trackImg = tk.Button(window, text="Take Photo",
					command=takephoto, fg="white", bg="#6518AC",
					width=20, height=3, activebackground="Red",
					font=('times', 15, ' bold '))
trackImg.place(x=1100, y=500)

quitWindow = tk.Button(window, text="Quit",
					command=login, fg="white", bg="#6518AC",
					width=20, height=3, activebackground="Red",
					font=('times', 15, ' bold '))
quitWindow.place(x=645, y=690)

window.mainloop()