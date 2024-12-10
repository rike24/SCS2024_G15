# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:26:42 2024

@author: herman
"""

import numpy as np

def SustainabilityCheck(forest, age_list, min_age_agriculture, min_age_immune):
    
    remaining_trees_1 = np.sum(age_list[forest == -1] <= min_age_agriculture)
    remaining_trees_2 = np.sum(age_list[forest == -2] <= min_age_immune)
    total_number_of_trees = np.sum(forest < 0)
    percentage = (remaining_trees_1 + remaining_trees_2)/total_number_of_trees
    
    return percentage

#%%

# forest_size = 64

# age_list = np.random.randint(0,100,[forest_size, forest_size])
# mean_age = 50

# remainingTreesPercent = SustainabilityCheck(age_list, mean_age)

# print(remainingTreesPercent)

