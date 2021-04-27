from tkinter import messagebox
from distutils.core import setup

def popup():
    messagebox.showinfo("Information", "Thanks for downloading.\nVisit https://github.com/Forhad95000 for more items")

setup (
	name = "HoverInfo",
	version = "1.0",
	packages = ["HoverInfo"],
	license = "MIT",
	long_description = open("README.md").read()
)

popup()
