# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:21:52 2024

@author: marike
"""

import numpy as np

def HarvestForest(forest, ageList, meanAge):
    """
    Function to simulate the harvest of the forest.
    
    Parameters
    ==========
    forest : 2-dimensional array NxN of tree states
    foresr_counter: 2-dimensional array NxN of time counter for states
    """

    wood_outcome = 0
    healthy_trees = np.argwhere(forest==-1)
    #age_of_healthy_trees = np.mean(forest[healthy_trees[:,0], -healthy_trees[:,1]])
    age_of_healthy_trees = np.mean(ageList[forest==-1])

    if age_of_healthy_trees>=meanAge:

        # calculate amount of healthy wood

        if not healthy_trees.any():
            wood_outcome = 0
        
        else:
            wood_outcome = np.sum(ageList[healthy_trees[:,0], -healthy_trees[:,1]])

    else:
        wood_outcome = -1

    return wood_outcome

# inittialize variables for testing
forestSize = 64  # Sides of the forest.
pGrowth = 0.005  # Growth probability.
pInfection = 0.1 # Infection probability.
pSpread = 0.4 # Spreading probability.
meanAge = 25
forest = np.random.randint(-2,2,(forestSize,forestSize))
ageList = np.random.randint(0,100,(forestSize,forestSize))
infectionTime = 20 # Minimum number of steps an infection lasts.

wood_outcome = HarvestForest(forest, ageList, meanAge)
print(wood_outcome)
