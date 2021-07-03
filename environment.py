# import packages
from tkinter import *
from tkinter import ttk
import time
from collections import Counter
# import organisms
from cell import *
from food import *
from analyze import *
# import constants
from constants import *

## SETUP ENVIRONMENT
# instantiate application window
window = Tk()
# name application window
window.title('Cell Environment')
# let it fill empty space
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# create the canvas
background_color = '#ffffff'
canvas = Canvas(window, width=window_width, height=window_height, background=background_color)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))

## DEFINE ORGANISMS AND INTERACTIONS
# define food
food = Food(canvas)  # allows us to click to add food
# create initial number of food
for _ in range(initial_num_food):
    food.add_food_random()
# create initial number of cells
cells = [Cell(canvas, cell_cycle) for _ in range(initial_num_cells)]
# prepare for cell number tracking
with open(track_filename, 'wt') as f: f.writelines('round,clone,count\n')
# circulate movements
total_rounds = 0  # track the number of rounds we can have the cells survive in
while(len(cells) > 0):
    # track time to complete a round
    start_time = time.time()
    # complete food actions for this round
    for _ in range(food_per_round):
        food.add_food_random()  # add another piece of food
    # complete cellular actions for this round
    actions_possible = True  # we can still have cells take actions
    round_num = 1  # we continue increasing this till we reach the max cell cycle
    while(actions_possible):
        # attempt to make cells move
        made_move = 0
        for cell in cells:
            if(cell.cell_alive):  # check if marked for death
                if(cell.cell_cycle >= round_num):
                    cell.move()  # move the cell
                    n_eaten = food.eaten(cell)  # check if cell can eat food and how much
                    if(n_eaten > 0):  # only compute further actions if needed
                        new_cell = cell.eat(n_eaten)  # check if cell can eat food
                        if(new_cell is not None):  # if the cell divided
                            cells.append(new_cell)
                    window.update()
                    made_move += 1
            else:  # kill the cell
                cell.die()
                cells.remove(cell)
        # decide next course of action
        if(made_move == 0):
            actions_possible = False
        else:
            round_num += 1
    # prepare for next round
    total_rounds += 1  # track the number of rounds
    # record values
    cell_colors = Counter([cell.cell_color for cell in cells])
    for cell_color,count in cell_colors.items():
        with open(track_filename, 'at') as f: f.writelines(f'{total_rounds},{cell_color},{count}\n')
    # rest until next round
    sleep_time = round_delay - (time.time() - start_time)
    if(sleep_time > 0):
        time.sleep(sleep_time)  # so this is more readable
# report survival
print(f'Survived a total of {total_rounds} rounds for cells with lifespan of {cell_age_of_death}')
# analyze data
analyze_history()  # using the tracking file

# run simulation
window.mainloop()
