# import all functions from tkinter
from tkinter import *
# import the ttk submodule, we'll want to do this in the future because there are functions and classes from both the super and submodule that are named the same but unequal in terms of function and proper usage
from tkinter import ttk

# define the main function we'll be using to calculate values
def calculate(*args):
    try:
        # we use the global arguments feet and meters to both set and retrieve values
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

# we instantiate the main application window
root = Tk()
# we name the window
root.title("Feet to Meters")

# we create a frame to hold our data, this defines our application, we use frame so we can control the entire window rather than just the areas around the widgets, specifically it goes width, height, padding right, padding bottom
mainframe = ttk.Frame(root, padding="3 3 12 12")
# this defines the coordinate structure of our grid, sticky defines which directions the widget will stick to the given frame
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# tells it to expand to fill empty space both for columns and rows
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# this is the entry widget for inputting data, string of variable length
feet = StringVar()
# here we define the widget itself, we use entry to specify we want it for input, and say the textvariable is the stringvar we just defined
feet_entry = ttk.Entry(mainframe, width=4, textvariable=feet)
# here we define the .grid part informs Tk how to organize the widget allowing it to put it on screen, so column2, row1, attach it to the left and right side of this column
feet_entry.grid(column=2, row=1, sticky=(W, E))

# we repeat for meters
meters = StringVar()
# this is a label we don't want to get info but show it
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

# this is how we'll define the calculation function
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

# we provide the remaining labels
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

# thicken the lining around the widgets
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# tells the cursor to have clicked on the entry to feet
feet_entry.focus()
# key binds
root.bind("<Return>", calculate)
# start the program
root.mainloop()
