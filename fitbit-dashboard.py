from tkinter import *
from tk_tools import *
from tkinter.ttk import *
from tkinter import messagebox
from time import sleep as wait
root=Tk()
import fitbit
import webbrowser
def add_alarm():
    if not hrEntry.get()=='' and not minEntry.get()=='' and connect:
        messagebox.showinfo('Success', 'Successfully added alarm')
    elif connect:
        messagebox.showerror('Error', 'Value(s) are invalid')
    else:
        messagebox.showerror('Error', 'Not connected to Fitbit')
root.title('Fitbit Dashboard')
root.grid()
root.iconbitmap('dashboard.ico')
restingHR=RotaryScale(root, unit=' BPM resting HR', max_value=100)
restingHR.grid(column=1, row=1)
steps=Gauge(root, max_value=10000, label='steps', unit='', red_low=20, yellow_low=30, red=100, yellow=100)
steps.grid(column=2, row=1)
cals=Gauge(root, max_value=2400, label='calories', unit='', red_low=20, yellow_low=30, red=100, yellow=100)
cals.grid(column=4, row=1)
dist=Gauge(root, max_value=5, label='distance', unit=' mi', red_low=20, yellow_low=30, red=100, yellow=100)
dist.grid(column=3, row=1)
actmins=Gauge(root, max_value=30, label='active minutes', unit='', red_low=20, yellow_low=30, red=100, yellow=100)
actmins.grid(column=5, row=1)
hrEntry=Spinbox(root, from_=0, to=23, state='readonly')
restingHR.set_value(0)
hrEntry.grid(column=7, row=1)
minEntry=Spinbox(root, from_=0, to=59, state='readonly')
minEntry.grid(column=8, row=1)
addbutton=Button(root, text='Add Alarm', command=add_alarm)
addbutton.grid(column=9, row=1)
connected=Led(root, size=50)
connected.grid(column=4, row=2)
error_code=SevenSegmentDigits(root, digit_color='red', background='black', digits=3, height=50)
error_code.grid(column=5, row=2)
Label(root, text='Connected').grid(column=4, row=3)
lo_bat=Led(root, size=50)
lo_bat.grid(column=3, row=2)
lo_bat.to_red(on=False)
Label(root, text='Error Code').grid(column=5, row=3)
Label(root, text='Batt Low').grid(column=3, row=3)
root.resizable(False, False)
import urllib.request
import urllib.error
while True:
    try:
        act_list=urllib.request.urlopen('https://api.fitbit.com/1/user/-/activities/date/2021-05-13.json')
        steps.set_value(act_list.read()['summary']['steps'])
        cals.set_value(act_list.read()['summary']['caloriesOut'])
        actmins.set_value(act_list.read()['summary']['veryActiveMinutes'])
        dist.set_value(0)
        connected.to_green(on=True)
        connect=True
        code.set_value(0)
        root.update()
    except urllib.error.HTTPError as e:
        connect=False
        connected.to_green(on=False)
        error_code.set_value(str(e.code))
    except OSError:
        connected.to_green(on=False)
        connect=False
        error_code.set_value('1')
    except AttributeError:
        connected.to_green(on=False)
        error_code.set_value('2')
        connect=False
    except NameError:
        connected.to_green(on=False)
        connect=False
        error_code.set_value('3')
    except:
        break
    root.update()
    wait(0.01)
