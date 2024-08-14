from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import tkinter.simpledialog
import requests
from tkinter import *
import pandas
import numpy as np
import os
import collections
api_key_alpha = os.getenv("api_alpha")
api_key_polygon = os.getenv("api_polygon")
coordination_key = [[700, 500], [80, 250], [240, 250], [400, 250], [80, 310], [240, 310], [400, 310], [980, 250], [1140, 250], [1300, 250], [980, 320], [1140, 320], [1300, 320], [80, 535], [80, 595], [80, 675], [80, 740], [570, 410], [570, 600], [1050, 540], [1050, 560], [1270, 540], [1270, 560]]
coordination_value = [[700, 450], [80, 140], [240, 140], [400, 140], [80, 400], [240, 420], [400, 440], [980, 140], [1140, 140], [1300, 140], [980, 420], [1140, 420], [1300, 420], [245, 740], [245, 675], [245, 535], [245, 595], [800, 600], [800, 410], [1050, 700], [1050, 720], [1270, 700], [1270, 720]]
# pid = os.fork()
print(len(coordination_value))
print(len(coordination_key))
restrict = []
settings = NONE
x = NONE
y = NONE




root = Tk()

#setting up a tkinter canvas
w = Canvas(root, width=1000, height=1000)
w.pack()

#adding the image
File = askopenfilename(parent=root, initialdir="./",title='Select an image')
original = Image.open(File)
original = original.resize((1000,1000)) #resize image
img = ImageTk.PhotoImage(original)
w.create_image(0, 0, image=img, anchor="nw")

#ask for pressure and temperature extent
xmt = tkinter.simpledialog.askfloat("Temperature", "degrees in x-axis")
ymp = tkinter.simpledialog.askfloat("Pressure", "bars in y-axis")

#ask for real PT values at origin
xc = tkinter.simpledialog.askfloat("Temperature", "Temperature at origin")
yc = tkinter.simpledialog.askfloat("Pressure", "Pressure at origin")

#instruction on 3 point selection to define grid
messagebox.showinfo("Instructions", "Click: \n"
                                            "1) Origin \n"
                                            "2) Temperature end \n"
                                            "3) Pressure end")

# From here on I have no idea how to get it to work...

# Determine the origin by clicking
def getorigin(eventorigin):
    global x0,y0
    x0 = eventorigin.x
    y0 = eventorigin.y
    print(x0,y0)
    w.bind("<Button 1>",getextentx)
#mouseclick event
w.bind("<Button 1>",getorigin)

# Determine the extent of the figure in the x direction (Temperature)
def getextentx(eventextentx):
    global xe
    xe = eventextentx.x
    print(xe)
    w.bind("<Button 1>",getextenty)

# Determine the extent of the figure in the y direction (Pressure)
def getextenty(eventextenty):
    global ye
    ye = eventextenty.y
    print(ye)
    tkinter.messagebox.showinfo("Grid", "Grid is set. You can start picking coordinates.")
    w.bind("<Button 1>",printcoords)

#Coordinate transformation into Pressure-Temperature space
def printcoords(event):
    xmpx = xe-x0
    xm = xmt/xmpx
    ympx = ye-y0
    ym = -ymp/ympx

    #coordinate transformation
    newx = (event.x-x0)*(xm)+xc
    newy = (event.y-y0)*(ym)+yc

    #outputting x and y coords to console
    print(newx,newy)


root.mainloop()


def doit(**kwargs):
    # dict_0 = {}
    # for all in kwargs:
        # dict_0.update(all)
    global restrict
    super_dict = {}
    for s in range(1, 4):
        if f"data_{s}" in kwargs:
            super_dict.update(kwargs[f"data_{s}"])

    dict_1 = pandas.DataFrame([super_dict])
    new_dict = dict_1.drop(dict_1.columns[restrict], axis=1)
    values_array = new_dict.values
    keys_array = new_dict.columns
    new_values_array = np.array([])

    for value in values_array:
        new_values_array = np.append(new_values_array, value)
    return [keys_array, new_values_array]


def initiate(h):
    global restrict
    company = input("What company do you want to seek?: ")
    print("Wait about 10 seconds.... and CHECK new pop up APPLICATION with PYTHON SYMBOL.")
    if h == "OVERVIEW":
        data_1 = requests.get(f"https://www.alphavantage.co/query?function={h}&symbol={company}&apikey={api_key_alpha}").json()
        restrict = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15, 17, 24, 29, 38, 39, 44, 45]  # 23
        return doit(restrict=restrict, data_1=data_1)
    if h == "tickers":
        global settings
        setting = "tickers"
        data = requests.get(f'https://api.polygon.io/v3/reference/{h}/{company}?apiKey={api_key_polygon}').json()
        restrict = [] #remember 21
        data_1 = pandas.DataFrame(data["results"]["address"], index=[0]).to_dict()
        data_2 = pandas.DataFrame(data["results"]["branding"], index=[0]).to_dict()
        data_3 = pandas.DataFrame(data["results"], index=[0]).to_dict()

        return doit(data_1=data_1, data_2=data_2, data_3=data_3)
    if h == "BALANCE_SHEET":
        pass
        # return overview(data, restrict=restrict)
    if h == "CASH_FLOW":
        pass
        # return overview(data, restrict=restrict)


def applying_process(final_output_data_keys, final_output_data_values):
    x = 0
    while x < len(coordination_value):
        canvas.create_text(coordination_key[x][0], coordination_key[x][1], font=("Arial TUR", 9), text=final_output_data_keys[x])
        canvas.create_text(coordination_value[x][0], coordination_value[x][1], font=("Arial TUR", 9), text=final_output_data_values[x])
        x += 1


input_find = input("What choice of Info?: ('OVERVIEW', 'tickers', 'INCOME_STATEMENT', 'CASH_FLOW')?: ")
f = initiate(h=input_find)
final_output_data_keys = f[0]
final_output_data_values = f[1]

window = Tk()
window.title("Stocks!")
window.config(padx=50, pady=30, bg="lavender")


canvas = Canvas(width=1406, height=757)
image_1 = PhotoImage(file="Background.png")
canvas.create_image(703, 379, image=image_1)
canvas.pack()


window.after(10000, applying_process(final_output_data_keys, final_output_data_values))






window.mainloop()
