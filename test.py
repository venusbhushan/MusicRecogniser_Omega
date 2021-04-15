import pywhatkit as kit
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pafy
import urllib.request
import re
from pytube import YouTube
import sys
import os
import PIL.Image
import PIL.ImageTk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
import time



root = tk.Tk()
root.title("Omega")
root.geometry("1000x1000")
root.resizable(False,False)



def listen():
    os.system("python recognize-from-microphone.py")

    global image
    global label
    global  mp3_button
    global mp4_button
    def download_mp3():
        #location = r'C:\Users\KIIT\Deskto
        search_key = lines[6]
        search_key = search_key.replace(" ", "")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_key)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        link = "https://www.youtube.com/watch?v=" + video_ids[0]
        audio = pafy.new(link)
        bestaudio = audio.getbestaudio()
        bestaudio.download()
        clear.config(state="normal")


    mp3_button = tk.Button(root, text="Download Mp3", command=download_mp3, width=13, height=1,
                           activebackground='green')
    mp3_button.pack(side="top",pady=2)
    # def download_mp4():
    #     # location = r'C:\Users\KIIT\Desktop'
    #     search_key=lines[6]
    #     search_key=search_key.replace(" ", "")
    #     html=urllib.request.urlopen("https://www.youtube.com/results?search_query="+ search_key)
    #     video_ids=re.findall(r"watch\?v=(\S{11})",html.read().decode())
    #     link = "https://www.youtube.com/watch?v=" + video_ids[0]
    #     myvideo = YouTube(link)
    #     myvideo.streams.order_by('resolution').desc().first().download()
    #     clear.config(state="normal")
    # mp4_button = tk.Button(root, text="Download Mp4", command=download_mp4, width=13, height=1,
    #                        activebackground='green')
    # mp4_button.pack(side="top",pady=8)
    with open('out.txt', 'r') as f:
        lines = f.readlines()
        configfile.insert(INSERT, lines[1])
        configfile.insert(INSERT, lines[2])
        configfile.insert(INSERT, lines[3])
        configfile.insert(INSERT, lines[4])
        configfile.insert(INSERT, lines[5])

    configfile.pack(fill="none", expand=False)


    global img
    global panel
    global youtube_button
    global clear


    def youtube():
        listen_button.config(state='disabled')
        kit.playonyt(lines[6])
    youtube_button = tk.Button(root, text="Watch on Youtube", command=youtube, width=16,fg='white', height=1, bg='red')
    youtube_button.pack(pady=1)

    img = PIL.ImageTk.PhotoImage(PIL.Image.open("example.jpg").resize((300, 300)), master=root)

    panel = tk.Label(root, image=img)
    panel.pack(side="top",fill="none",expand="yes")
    listen_button.config(state='disabled')
    clear.config(state="normal")


# variable1=tk.StringVar(value="Listening for 6 seconds")
# display=ttk.Label(root,textvariable=variable1).pack(pady=8)

listen_button = tk.Button(root, text="Listen", command=listen,width=13,height=1,activebackground='green')
listen_button.pack(pady=8)

configfile = Text(root, wrap=WORD, width=45, height= 10)
def clear():
    youtube_button.destroy()
    configfile.delete(1.0, END)
    panel.destroy()
    listen_button.config(state='normal',text='Listen')
    mp3_button.destroy()
    clear.config(state="disabled")
    # mp4_button.destroy()
    # configfile.destroy()

clear = Button(root, text='Clear', command=clear,width=13,height=1,state='disabled')
clear.pack(pady=8)

quit = tk.Button(root, text="Quit", command=root.destroy,width=13,height=1,activebackground='red')
quit.pack(pady=8)





root.mainloop()
