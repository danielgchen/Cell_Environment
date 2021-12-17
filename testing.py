# import packages
from tkinter import *
from tkinter import ttk
import time
# import organisms
from cell import *
from food import *
from vent import *
from analyze import *
# import constants
from utils import *

## SETUP ENVIRONMENT
# instantiate application window
window = Tk()
# name application window
window.title('Cell Environment')
# let it fill empty space (we have 1 row, 1 col)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# create the canvas
canvas = Canvas(window, width=window_width, height=window_height, background=background_color)
canvas.grid(column=0, row=0, sticky=NW)  # start from middle centered to the upper left

vents = [Vent(canvas) for _ in range(2)]
vents_attrs = np.array([np.append(vent.radius, vent.center) for vent in vents])  # TODO: do the conversion here where just get all the attributes
while(len(vents) > 0):
    time.sleep(1)
    for vent in vents:
        if(len(vent.foods) > 0):
            vent.diffuse_foods()
        for _ in range(core_rng.integers(1,10)):
            vent.add_food()
window.mainloop()
