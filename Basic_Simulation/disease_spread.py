# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 06:11:00 2024

@author: zishan

All infected trees execute disease spreading for one time
"""
#%%
import numpy as np

#%% Function to spread the disease.
def SpreadDisease(forest, infected_positions_i, infected_positions_j, pSpread):
    """
    Function to propagate the disease on a populated forest.
    
    Parameters
    ==========
    forest : 2-dimensional array. -1 for healthy trees, 1 for infected trees, 0 for empty cells.
    infected_positions_i & j : List of the coordinates of all infected trees.
    pSpread : Probability of spreading the disease.
    """
    
    Ni, Nj = forest.shape  # Dimensions of the forest.

    active_i = infected_positions_i
    active_j = infected_positions_j
        
    if len(active_i) > 0:
        for n in np.arange(len(active_i)):
            # Coordinates of cell up.
            i = (active_i[n] + 1) % Ni
            j = active_j[n]
            # Check status
            if forest[i, j] == -1:
                r = np.random.rand()
                if r < pSpread:
                    forest[i, j] = 1  # Infects the current tree.

            # Coordinates of cell down.
            i = (active_i[n] - 1) % Ni
            j = active_j[n]
            # Check status
            if forest[i, j] == -1:
                r = np.random.rand()
                if r < pSpread:
                    forest[i, j] = 1  # Infects the current tree.

            # Coordinates of cell left.
            i = active_i[n]
            j = (active_j[n] - 1) % Nj
            # Check status
            if forest[i, j] == -1:
                r = np.random.rand()
                if r < pSpread:
                    forest[i, j] = 1  # Infects the current tree.

            # Coordinates of cell right.
            i = active_i[n]
            j = (active_j[n] + 1) % Nj
            # Check status
            if forest[i, j] == -1:
                r = np.random.rand()
                if r < pSpread:
                    forest[i, j] = 1  # Infects the current tree.

    return forest
# %%
N = 10000
# random forest with 10% of trees infected.
initial_forest = np.random.choice([-1, 0, 1], size=(N, N), p=[0.9, 0.09, 0.01])
# plot the forest
import matplotlib.pyplot as plt
plt.imshow(initial_forest, cmap='viridis')
plt.colorbar()
plt.show()


# %%
# Spread the disease
# index of infected trees
infected_index = np.where(initial_forest == 1)
initial_forest = SpreadDisease(initial_forest, infected_index[0], infected_index[1] , 0.7)
# plot the forest
plt.imshow(initial_forest, cmap='viridis')
plt.colorbar()
plt.show()

# %%
