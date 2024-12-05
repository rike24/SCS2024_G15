# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:33:48 2024

@author: Bryanz
"""

import numpy as np

def TreeDeath(forest, infectionTime, infectionTimeList):
    """
    Function to keep track of how long the trees remain infected.
    
    Parameters
    ==========
    forest : 2-dimensional array NxN of tree states
    infectionTime: maximum time a tree can remain infected before its cut down.
    infectionTimeList: 2-dimensional array NxN tracking infection duration.
    """
    
    #increament the infection time for the infected trees
    infectionTimeList[forest == 1] += 1
    
    #for the healthy trees, set to zero
    infectionTimeList[forest == -1] = 0
    
    #cut down trees when infection time is exceeded
    for i, j in np.ndindex(forest.shape):
        if forest[i, j] == 1 and infectionTimeList[i, j] > infectionTime:
            forest[i, j] = 0
            
    #forest[(forest == 1) & (infectionTimeList > infectionTime)] = 0
            
            
            
    return forest, infectionTimeList
    
    