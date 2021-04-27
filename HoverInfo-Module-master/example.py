#This code can create error "bad window path name" but it is not critical.

from tkinter import *
from HoverInfo import HoverText

app = Tk()
app.title("HoverInfo Module Example")
app.geometry("360x60+0+0")

label = Label(app, text="Keep cursor here")
label.pack()

HoverText(label, "This is a sample hover text")

app.mainloop()
