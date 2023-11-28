import tkinter as tk
from tkinter import messagebox
from Mod1.Main1 import Module_1
from Mod2 import Main2
from Mod3 import Main3
#from Mod4 import Main4

def function1():
    messagebox.showinfo("Button 1", "Function 1 called!")
    Module_1()

def function2():
    messagebox.showinfo("Button 2", "Function 2 called!")

def function3():
    messagebox.showinfo("Button 3", "Function 3 called!")

def function4():
    messagebox.showinfo("Button 4", "Function 4 called!")

# Create the main window
root = tk.Tk()
root.title("Road-Safe : An All In One Solution")

# Set the background color to white
root.configure(bg="#FFFFFF")

# Increase the window size
root.geometry("500x300")

# Use a different font and relief style for the buttons
button_font = ("Helvetica", 12, "bold")
button_relief = "ridge"

# Create buttons with blue color
button1 = tk.Button(root, text="Drowsyness Detection", command=function1, height=3, width=15, bg="#0000FF", fg="white", font=button_font, relief=button_relief)
button2 = tk.Button(root, text="Crash Detection", command=function2, height=3, width=15, bg="#0000FF", fg="white", font=button_font, relief=button_relief)
button3 = tk.Button(root, text="Pothole Detection", command=function3, height=3, width=15, bg="#0000FF", fg="white", font=button_font, relief=button_relief)
button4 = tk.Button(root, text="Sign Detection", command=function4, height=3, width=15, bg="#0000FF", fg="white", font=button_font, relief=button_relief)

# Place buttons in the center of the window
button1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
button2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
button3.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
button4.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

# Configure row and column weights for centering
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the main loop
root.mainloop()