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
    
    
    #cut down trees when infection time is exceeded
    for i in range(forest.shape[0]):
        for j in range(forest.shape[1]):
            if forest[i, j] == 1 and infectionTimeList[i, j] > infectionTime:
                forest[i, j] = 0
                
                #Reset infection time
                infectionTimeList[i, j] = 0
                age_list[i, j] = 0
            
    #forest[(forest == 1) & (infectionTimeList > infectionTime)] = 0
            
            
    return forest, age_list, infectionTimeList
    
    