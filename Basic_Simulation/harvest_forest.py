# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:21:52 2024

@author: marike
"""

import numpy as np

def HarvestForest(forest, ageList, minAgeAgriculture, minAgeImmune=100, relativeGrowing=0):
    """
    Function to simulate the harvest of the forest.
    
    Parameters
    ==========
    forest : 2-dimensional array NxN of tree states
    ageList: 2-dimensional array NxN of time counter for states
    minAgeAgriculture: minimum age for harvest of agricultur species -1 
    minAgeImmune: minimum age for harvest of immune species -1 
    relativeGrowing: assume wood value of agriculture tree as 1 per age of tree
                     and set value of immune tree as relative growing
    """
    
    age_of_healthy_trees = ageList[forest==-1]
    age_of_immune_trees  = ageList[forest==-2]

    wood_agriculture = np.sum(age_of_healthy_trees[age_of_healthy_trees>minAgeAgriculture])

    if relativeGrowing!=0:
        wood_immune_tree = relativeGrowing * np.sum(age_of_immune_trees[age_of_immune_trees>minAgeImmune])
        wood_outcome = wood_agriculture + wood_immune_tree
    else:
        wood_outcome = wood_agriculture

    return wood_outcome

# inittialize variables for testing
forestSize = 64  # Sides of the forest.
relativeGrowth = 0.4 # Spreading probability.
minAgeAgriculture = 25
minAgeImmune = 50
forest = np.random.randint(-2,2,(forestSize,forestSize))
ageList = np.random.randint(0,100,(forestSize,forestSize))

wood_outcome = HarvestForest(forest, ageList, minAgeAgriculture, minAgeImmune, relativeGrowth)
print(wood_outcome)
