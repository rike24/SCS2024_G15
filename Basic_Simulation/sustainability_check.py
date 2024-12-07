# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:26:42 2024

@author: herman
"""

import numpy as np

def SustainabilityCheck(forest, age_list, mean_age):
    
    remaining_trees = np.sum(age_list <= mean_age)
    empty_spots = np.sum(forest == 0)
    total_number_of_trees = np.size(age_list) - empty_spots
    percentage = remaining_trees/total_number_of_trees
    
    return percentage

#%%

# forest_size = 64

# age_list = np.random.randint(0,100,[forest_size, forest_size])
# mean_age = 50

# remainingTreesPercent = SustainabilityCheck(age_list, mean_age)

# print(remainingTreesPercent)

