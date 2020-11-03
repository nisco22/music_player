import os
from tkinter import *
from PIL import ImageTk, Image
from pygame import mixer
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
import tkinter.messagebox
import threading
import time


# Functions for Widgets
def open_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

# This contains the full filename path of music file to be played
playlist = []

def add_to_playlist(filename):
    filename = os.path.basename(filename_path)
    index = 0
    playlistBox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

def show_details(play_song):
    filename_ext = os.path.splitext(play_song)
    if filename_ext[1] == ".mp3":
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = '{:02d}:{:02d}'.format(mins, secs)
    totalLength["text"] = "Time Length:" + " - " + time_format

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        mins, secs = divmod(current_time, 60)
        mins = round(mins)
        secs = round(secs)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        currentTime["text"] = "Current Time:" + " - " + time_format
        time.sleep(1)
        current_time += 1

def play_music():
    global paused
    if paused:
       mixer.music.unpause()
       statusBar["text"] = "Music Resumed" + " - " + os.path.basename(filename_path)
    else:
        try:
            mixer.music.stop()
            time.sleep(1)
            selected_song = playlistBox.curselection()
            selected_song = int(selected_song[0])
            play_selected = playlist[selected_song]
            mixer.music.load(play_selected)
            mixer.music.play()
            statusBar["text"] = "Music Playing" + " - " + os.path.basename(play_selected)
            show_details(play_selected)
        except:
            tkinter.messagebox.showerror("Music Filename Error", "Music Filename Unavailable, Please load Music First!")

def stop_music():
    mixer.music.play()
    mixer.music.stop()
    statusBar["text"] = "Music Stopped"

paused = FALSE
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar["text"] = "Music Paused"

def rewind_music():
    play_music()
    statusBar["text"] = "Music Rewinded" + " - " + os.path.basename(filename_path)

mute = FALSE
def mute_music():
    global mute
    if mute:
        scaleVol.set(0)
        muteBtn["image"] = muteImage
        mute = FALSE
    else:
        scaleVol.set(70)
        mixer.music.set_volume(0.7)
        muteBtn["image"] = unmuteImage
        mute = TRUE

def set_vol(value):
    volume = float(value)/100
    mixer.music.set_volume(volume)

def del_song():
    selected_song = playlistBox.curselection()
    selected_song = int(selected_song[0])
    playlistBox.delete(selected_song)
    playlist.pop(selected_song)

def about_us():
    tkinter.messagebox.showinfo("Nisco Music Player", "Welcome To Nisco Music Player Contact Us @official_nisco instagram")

def on_closing():
    mixer.music.stop()
    root.quit()

root = tk.ThemedTk()
root.get_themes()
root.set_theme("clearlooks")
mixer.init()
root.title("Nisco Player")
root.iconbitmap("images/play_button.ico")

# Menubar
menuBar = Menu(root)
root.config(menu=menuBar)

fileMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", command=open_file)
fileMenu.add_command(label="Exit", command=root.quit)

exitMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help", menu=exitMenu)
exitMenu.add_command(label="About Us", command=about_us)

# Status bar
statusBar = Label(root, text="@Nisco 2020", bd=1, anchor=W, relief=SUNKEN, font="Ariel 10 italic")
statusBar.pack(side=BOTTOM, fill=X)

# Widgets
#LEFT & RIGHT FRAMES
leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=55)

playlistBox = Listbox(leftFrame)
playlistBox.pack()

addBtn = ttk.Button(leftFrame, text="+ Add", command=open_file)
addBtn.pack(side=LEFT, padx=3)

deleteBtn = ttk.Button(leftFrame, text="- Delete", command=del_song)
deleteBtn.pack(side=LEFT)

rightFrame = Frame(root)
rightFrame.pack()

# Top Frame
topFrame = Frame(rightFrame)
topFrame.pack(side=TOP, pady=20, padx=55)

totalLength = ttk.Label(topFrame, text="Total Length: --:--")
totalLength.pack(pady=3)

currentTime = ttk.Label(topFrame, text="Current Time: --:--", relief=GROOVE)
currentTime.pack()

# MiddleFrame with buttons
middleFrame = Frame(rightFrame)
middleFrame.pack(pady=20, padx=55)

playImage = ImageTk.PhotoImage(Image.open("images/play.png"))
playBtn = ttk.Button(middleFrame, image=playImage, command=play_music)
playBtn.grid(row=0, column=0, padx=3, pady=3)

stopImage = ImageTk.PhotoImage(Image.open("images/stop_button.png"))
stopBtn = ttk.Button(middleFrame, image=stopImage, command=stop_music)
stopBtn.grid(row=0, column=1, padx=3, pady=3)

pauseImage = ImageTk.PhotoImage(Image.open("images/pause.png"))
pauseBtn = ttk.Button(middleFrame, image=pauseImage, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=3, pady=3)

# BottomFrame widgets
bottomFrame = Frame(rightFrame)
bottomFrame.pack(pady=25, padx=55)

rewindImage = ImageTk.PhotoImage(Image.open("images/rewind_btn.png"))
rewindBtn = ttk.Button(bottomFrame, image=rewindImage, command=rewind_music)
rewindBtn.grid(row=0, column=0, padx=3)

muteImage = ImageTk.PhotoImage(Image.open("images/muted.png"))
unmuteImage = ImageTk.PhotoImage(Image.open("images/unmutee.png"))
muteBtn = ttk.Button(bottomFrame, image=unmuteImage, command=mute_music)
muteBtn.grid(row=0, column=1, padx=3)

scaleVol = ttk.Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scaleVol.set(70)
mixer.music.set_volume(0.7)
scaleVol.grid(row=0, column=2, padx=3)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()



