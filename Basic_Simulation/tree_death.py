# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:33:48 2024

@author: Bryanz
"""

import numpy as np

def TreeDeath(forest, age_list, infectionTime, infectionTimeList):
    """
    Function to keep track of how long the trees remain infected.
    
    Parameters
    ==========
    forest : 2-dimensional array NxN of tree states
    infectionTime: maximum time a tree can remain infected before its cut down.
    infectionTimeList: 2-dimensional array NxN tracking infection duration.
    """
    
    # Cut down trees when infection time is exceeded
    mask = (forest == 1) & (infectionTimeList > infectionTime)
    forest[mask] = 0
    infectionTimeList[mask] = 0
    age_list[mask] = 0
    
    return forest, age_list, infectionTimeList
    
    