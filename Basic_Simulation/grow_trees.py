# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 11:49:22 2024

@author: herman
"""

import numpy as np

def GrowTrees(forest, p, p_tree_1_growth, p_tree_2_growth):
    """
    Function to grow new trees in the forest.
    
    Parameters
    ==========
    forest : 2-dimensional array.
    p : Probability for a tree to be generated in an empty cell.
    """
    
    Ni, Nj = forest.shape  # Dimensions of the forest.
    
    new_trees = np.random.rand(Ni, Nj) # Assign random values to each spot
    
    # Plant new trees in empty spots with probability p.
    new_trees_indices = np.where((new_trees <= p) & (forest == 0))
    forest[new_trees_indices] = \
        np.random.choice([-1, -2], \
                          replace=True, p=[p_tree_1_growth, p_tree_2_growth])
    
    return forest