'''
wapp.py
Author: Michael Leidel
Date: Jan 13 2021
'''

from tkinter import *
from tkinter.ttk import *  # defaults all widgets as ttk
from tkinter import messagebox
import os
import sys
from pathlib import Path
import requests
import threading
from ttkthemes import ThemedTk  # ttkthemes is applied to all widgets

TIMER = 0

class Application(Frame):
    ''' main class docstring '''

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        self.configure(borderwidth=5)
        self.create_widgets()
        self.loop_report()


    def create_widgets(self):
        ''' Build the Gui '''

        style = Style()
        style.configure('TLabel', font='Consolas 9')

        #family_size = "Console, 9"

        lbl = Label(self, text="Temp:")
        lbl.grid(row=2, column=1, sticky='e')

        self.vlbl_temp = StringVar()
        lbl_temp = Label(self, textvariable=self.vlbl_temp)
        lbl_temp.grid(row=2, column=2, sticky='w')
        self.vlbl_temp.set("::::::::::")

        lbl = Label(self, text="Feels:")
        lbl.grid(row=3, column=1, sticky='e')

        self.vlbl_feel = StringVar()
        lbl_feel = Label(self, textvariable=self.vlbl_feel)
        lbl_feel.grid(row=3, column=2, sticky='w')
        self.vlbl_feel.set("::::::::::")

        lbl = Label(self, text="Humid:")
        lbl.grid(row=4, column=1, sticky='e')

        self.vlbl_humidity = StringVar()
        lbl_humidity = Label(self, textvariable=self.vlbl_humidity)
        lbl_humidity.grid(row=4, column=2, sticky='w')
        self.vlbl_humidity.set("::::::::::")

        lbl = Label(self, text="Pressr:")
        lbl.grid(row=5, column=1, sticky='e')

        self.vlbl_pressure = StringVar()
        lbl_pressure = Label(self, textvariable=self.vlbl_pressure)
        lbl_pressure.grid(row=5, column=2, sticky='w')
        self.vlbl_pressure.set("::::::::::")

        lbl = Label(self, text="Wind:")
        lbl.grid(row=6, column=1, sticky='e')

        self.vlbl_wind = StringVar()
        lbl_wind = Label(self, textvariable=self.vlbl_wind)
        lbl_wind.grid(row=6, column=2, sticky='w')
        self.vlbl_wind.set("::::::::::")

        lbl = Label(self, text="From:")
        lbl.grid(row=7, column=1, sticky='e')

        self.vlbl_from = StringVar()
        lbl_from = Label(self, textvariable=self.vlbl_from)
        lbl_from.grid(row=7, column=2, sticky='w')
        self.vlbl_from.set("::::::::::")

        lbl = Label(self, text="Clouds:")
        lbl.grid(row=8, column=1, sticky='e')

        self.vlbl_clod = StringVar()
        lbl_clod = Label(self, textvariable=self.vlbl_clod)
        lbl_clod.grid(row=8, column=2, sticky='w')
        self.vlbl_clod.set("::::::::::")


        # POP UP MENU
        self.pup = Menu(self, tearoff=0)
        self.pup.add_command(label="Exit Program", command=save_location)
        self.pup.add_separator()
        self.pup.add_command(label="Toggle Exit", command=self.placement)
        self.pup.add_separator()
        self.pup.add_command(label="About", command=self.about)

        root.bind("<Button-3>", self.do_popup_pup)


    def do_popup_pup(self, event):
        ''' show the pop up menu on right mouse click '''
        try:
            self.pup.tk_popup(event.x_root,
                              event.y_root)
        finally:
            self.pup.grab_release()

    def placement(self, e=None):
        ''' toggle the signal (a file) to decorate or not '''
        if os.path.isfile('deco'):
            os.remove('deco')
        else:
            Path('deco').touch()
        save_location()


    def loop_report(self):
        ''' get new report every so many minutes '''
        global TIMER
        self.get_weather()
        TIMER = threading.Timer(600, self.loop_report)  # wait 10 min
        TIMER.start()


    def get_weather(self, e=None):
        ''' Use an API to get current weather conditions
        https://home.openweathermap.org/api_keys '''
        data = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=59999,us&appid=xxxxxxxxxxxxxxxxxxxxxxxxx")

        windarr = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]
        oftemp = data.json()['main']['temp'] * 9/5 - 459.67  # Kelvin to Fahrenheit
        oflike = data.json()['main']['feels_like'] * 9/5 - 459.67  # Kelvin to Fahrenheit
        oiprs = data.json()['main']['pressure'] * 0.029530  # millibar to inches
        owph = data.json()["wind"]["speed"] * 2.2369362920544  # meters/sec to mph
        owdr = data.json()["wind"]["deg"]

        windex = round((owdr % 360) / 22.5) + 1  # calculate index to windarr

        otmp = ('{: >5.1f}'.format(round(oftemp)))
        otfl = ('{: >5.1f}'.format(oflike))
        oprs = ('{: >5.1f}'.format(oiprs))
        ohum = ('{: >5.1f}'.format(data.json()['main']['humidity']))
        owsp = ('{: >5.1f}'.format(owph))
        clds = ('{: >5d}'.format(data.json()['clouds']['all']))
        wdir = ('{: >5s}'.format(windarr[windex]))

        self.vlbl_temp.set(otmp + " F")
        self.vlbl_humidity.set(ohum + " %")
        self.vlbl_pressure.set(oprs)
        self.vlbl_wind.set(owsp + " mph")
        self.vlbl_feel.set(otfl + " F")
        self.vlbl_clod.set(clds + " %")
        self.vlbl_from.set(wdir)


    def about(self):
        ''' about the app '''
        messagebox.showinfo("Weather App", "Weather provided by\nopenweathermap.org")

def save_location():
    ''' executes at WM_DELETE_WINDOW event '''
    global TIMER  # threading object
    TIMER.cancel()
    with open("winfoxy", "w") as fout:
        if os.path.isfile('deco'):
            fout.write(str(root.winfo_x()) + "\n" + str(root.winfo_y()-24))  # - 24 remove for windows
        else:
            fout.write(str(root.winfo_x()) + "\n" + str(root.winfo_y()))
    root.destroy()


# 'alt', 'scidsand', 'classic', 'scidblue',
# 'scidmint', 'scidgreen', 'default', 'scidpink',
# 'arc', 'scidgrey', 'scidpurple', 'clam', 'smog'
# 'kroc', 'black', 'clearlooks'
# 'radiance', 'blue' : https://wiki.tcl-lang.org/page/List+of+ttk+Themes
root = ThemedTk(theme="black")

# root.geometry("+500+500") # WxH+left+top
if os.path.isfile("winfoxy"):
    lcoor = tuple(open("winfoxy", 'r'))  # no relative path for this
    root.geometry('+%d+%d'%(int(lcoor[0].strip()), int(lcoor[1].strip())))

if not os.path.isfile("deco"):
    root.overrideredirect(True)


root.title(":::::::::::")
# Sizegrip(root).place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)
root.resizable(0, 0) # no resize & removes maximize button
# root.overrideredirect(True) # removed window decorations
# root.iconphoto(False, PhotoImage(file='icon.png'))
# root.attributes("-topmost", False)  # Keep on top of other windows
app = Application(root)
app.mainloop()
