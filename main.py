from tkinter import *
from tkinter.ttk import *
import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplleaflet
import threading


def crime_by_location():
    url = "https://phl.carto.com/api/v2/sql?q="
    radius = my_entry.get()  # in meters
    query = "SELECT * FROM incidents_part1_part2 WHERE ST_DWithin(the_geom::geography," \
            "ST_GeographyFromText('POINT(-75.155351200 39.981193500)'), " + str(radius) + ")"  # by gps coordinate
    df = pd.DataFrame(requests.get(url + query).json()['rows'])
    print(len(df))
    plt.scatter(df.point_x, df.point_y, marker='o')  # Draw red squares
    mplleaflet.show()


def retrieve():
    if Var1.get() is 1:
        crime_by_location()


def tk_general() -> object:
    _root = Tk()
    _root.geometry("250x150")
    _frame = Frame(_root)
    _frame.pack()
    return _root, _frame


if __name__ == '__main__':
    root, frame = tk_general()

    left_frame = Frame(root)
    left_frame.pack(side=LEFT)

    right_frame = Frame(root)
    right_frame.pack(side=RIGHT)

    label = Label(frame, text="Welcome to OpenDataPhilly Fun")
    label.pack()

    Var1 = IntVar()

    RBttn = Radiobutton(frame, text="Crime", variable=Var1, value=1)
    RBttn.pack(padx=5, pady=5)

    my_entry = Entry(frame, width=20)
    my_entry.insert(0, 'Radius in meters')
    my_entry.pack(padx=5, pady=5)

    Button = Button(frame, text="Submit", command=retrieve)
    Button.pack()

    root.title("ODP Explorer")
    threading.Thread(target=mainloop()).start()
