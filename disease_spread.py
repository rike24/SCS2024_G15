# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 06:11:00 2024

@author: zishan
"""

import numpy as np

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