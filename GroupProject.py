# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:21:52 2024

@author: herman
"""

import numpy as np

#%% Function to grow trees in the forest.
def GrowTrees(forest, p, ageList, infectionTime):
    """
    Function to pgrow new trees in the forest.
    
    Parameters
    ==========
    forest : 2-dimensional array.
    p : Probability for a tree to be generated in an empty cell.
    """
    
    Ni, Nj = forest.shape  # Dimensions of the forest.
    
    new_trees = np.random.rand(Ni, Nj) # Assign random values to each spot
    
    new_trees_indices = np.where(new_trees <= p)
    forest[new_trees_indices] = -1
    
    return forest

#%% Function to spread the disease.
def SpreadDisease(forest, i0, j0, pSpread):
    """
    Function to propagate the disease on a populated forest.
    
    Parameters
    ==========
    forest : 2-dimensional array.
    i0 : First index of the cell where the disease occurs.
    j0 : Second index of the cell where the disease occurs.
    """
    
    Ni, Nj = forest.shape  # Dimensions of the forest.

    if forest[i0, j0] == -1:
        active_i = [i0]  # Initialize the list.
        active_j = [j0]  # Tnitialize the list. 
        forest[i0, j0] = 1  # Infects the tree.
        
        while len(active_i) > 0:
            next_i = []
            next_j = []
            for n in np.arange(len(active_i)):
                # Coordinates of cell up.
                i = (active_i[n] + 1) % Ni
                j = active_j[n]
                # Check status
                if forest[i, j] == -1:
                    r = np.random.rand()
                    if r < pSpread:
                        next_i.append(i)  # Add to list.
                        next_j.append(j)  # Add to list.
                        forest[i, j] = 1  # Infects the current tree.

                # Coordinates of cell down.
                i = (active_i[n] - 1) % Ni
                j = active_j[n]
                # Check status
                if forest[i, j] == -1:
                    r = np.random.rand()
                    if r < pSpread:
                        next_i.append(i)  # Add to list.
                        next_j.append(j)  # Add to list.
                        forest[i, j] = 1  # Infects the current tree.

                # Coordinates of cell left.
                i = active_i[n]
                j = (active_j[n] - 1) % Nj
                # Check status
                if forest[i, j] == -1:
                    r = np.random.rand()
                    if r < pSpread:
                        next_i.append(i)  # Add to list.
                        next_j.append(j)  # Add to list.
                        forest[i, j] = 1  # Infects the current tree.

                # Coordinates of cell right.
                i = active_i[n]
                j = (active_j[n] + 1) % Nj
                # Check status
                if forest[i, j] == -1:
                    r = np.random.rand()
                    if r < pSpread:
                        next_i.append(i)  # Add to list.
                        next_j.append(j)  # Add to list.
                        forest[i, j] = 1  # Infects the current tree.

            active_i = next_i
            active_j = next_j        
            
    return forest

#%% Initialization
forestSize = 64  # Sides of the forest.
pGrowth = 0.005  # Growth probability.
pInfection = 0.1 # Infection probability.
pSpread = 0.4 # Spreading probability.
forest = np.zeros([forestSize, forestSize])  # Empty forest.
ageList = np.zeros([forestSize, forestSize]) # Initial ages.
infectionTime = 20 # Minimum number of steps an infection lasts.

#%% Simulation
import time
from tkinter import *

Ni, Nj = forest.shape  # Sets the variables describing the shape.

N_skip = 1 # Visualize status every N_skip steps. 

window_size = 600

tk = Tk()
tk.geometry(f'{window_size + 20}x{window_size + 20}')
tk.configure(background='#000000')

canvas = Canvas(tk, background='#ECECEC')  # Generate animation window.
tk.attributes('-topmost', 0)
canvas.place(x=10, y=10, height=window_size, width=window_size)

step = 0

def stop_loop(event):
    global running
    running = False
tk.bind("<Escape>", stop_loop)  # Bind the Escape key to stop the loop.
running = True  # Flag to control the loop.
while running:

    forest = GrowTrees(forest, pGrowth, ageList, infectionTime)  # Grow new trees.
    
    r = np.random.rand()
    if r < pInfection:  # Infection occurs.
        i0 = np.random.randint(Ni)
        j0 = np.random.randint(Nj)
        
        forest = SpreadDisease(forest, i0, j0, pSpread)
        
    # Update animation frame.
    if step % N_skip == 0:        
        canvas.delete('all')
        trees = []
        for i in range(Ni):
            for j in range(Nj):
                tree_color = '#00AA40' if forest[i, j] == -1 \
                else '#FF7F24' if forest[i, j] == 1 else '#FFFFFF'
                trees.append(
                    canvas.create_rectangle(
                        j / Nj * window_size, 
                        i / Ni * window_size,
                        (j + 1) / Nj * window_size, 
                        (i + 1) / Ni * window_size,
                        outline='', 
                        fill=tree_color,
                    )
                )
        
        tk.title(f'Iteration {step}')
        tk.update_idletasks()
        tk.update()
        time.sleep(0.001)  # Increase to slow down the simulation.

    step += 1
    
    #forest[np.where(forest == -1)] = 0

tk.update_idletasks()
tk.update()
tk.mainloop()  # Release animation handle (close window to finish).


