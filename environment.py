# import packages
from tkinter import *
from tkinter import ttk
import time
# import organisms
from cell import *
from food import *
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

## DEFINE ORGANISMS AND INTERACTIONS
# create fresh outputs directory
if(os.path.exists('outputs/')):
    os.system('rm -rf outputs/')
os.mkdir('outputs/')
# define food
food = Food(canvas)  # allows us to click to add food
# create initial number of food
for _ in range(initial_num_food):
    food.add_food_random()
# create initial number of cells
cells = [Cell(canvas) for _ in range(initial_num_cells)]
cells_attrs = np.array([[cell.cell_radius] + list(cell.cell_center) for cell in cells])  # TODO: do the conversion here where just get all the attributes
# prepare for cell number tracking
with open(f'outputs/{track_filename}.txt', 'wt') as f:
    f.writelines('round,clone,count\n')
# circulate movements
round_num = 0  # track the number of rounds we can have the cells survive in
round_label = Label(window, text=f'Round {round_num}')  # add label
round_label.grid(row=0, column=0, sticky=NW)  # configure it to top left
measure_first = time.time()
while(cells_attrs.shape[0] > 0 and round_num < 20):  # keep looping through the rounds as long as there are cells
    # > instantiate round
    start_time = time.time()  # track start time
    round_num += 1  # add to round number
    round_label['text'] = f'Round {round_num}'
    # > complete food actions for this round
    for _ in range(food_per_round):
        food.add_food_random()  # add another piece of food
    # > complete cellular actions for this round
    cells_acted = True  # track if the cell has acted
    cell_cycle_round = 1  # track the cell cycle round we're on
    while(cells_acted):  # keep looping until cells cannot act
        cells_acted = False  # instantiate no action yet
        for idx, cell in enumerate(cells):  # loop through each cell
            if(cell.cell_alive):  # check if marked for death
                if(cell.get_cell_cycle() >= cell_cycle_round):  # only move if allowed
                    cell.move(food, cells_attrs)  # move the cell
                    n_eaten = food.get_eaten(cell)  # check if cell can eat food and how much
                    if(n_eaten > 0):  # only compute further actions if needed
                        new_cell = cell.eat(n_eaten)  # check if cell can eat food
                        if(new_cell is not None):  # if the cell divided
                            cells.append(new_cell)
                            cells_attrs = np.append(cells_attrs, [[new_cell.cell_radius] + list(new_cell.cell_center)], 0)
                    window.update()  # update the window with move + divide
                    cells_acted = True  # at least one cell could act
            else:  # kill the cell
                cell.die()
                cells = cells.remove(cell)
                cells_attrs = np.delete(cells_attrs, idx)
        cell_cycle_round += 1
    # > record values
    record_snapshot(cells, round_num)
    record_population(cells, round_num)
    # > rest until next round
    sleep_time = round_delay - (time.time() - start_time)
    if(sleep_time > 0):
        time.sleep(sleep_time)
measure_last = time.time() - measure_first
print(measure_last)
# report survival
print(f'Survived a total of {round_num} rounds for cells with lifespan of {cell_age_of_death}')
# analyze data
analyze_history()  # using the tracking file
# run simulation
window.mainloop()
