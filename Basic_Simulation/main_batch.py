# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 11:45:05 2024

@author: herman
"""

#%%
import numpy as np
import matplotlib.pyplot as plt
from conv_grow_trees_TS import GrowTrees
from conv_disease_spread import SpreadDisease
from harvest_forest import HarvestForest
from update_age import AgeCounter
from initialize_forest import InitializeForest
from tree_death import TreeDeath
from sustainability_check import SustainabilityCheck
from plots import plotForestData

# Simulation parameters
forest_size = 100  # Sides of the forest
p_growth = 0.005  # Growth probability
p_infection = 1/(forest_size ** 2 * 20) # Infection probability
p_spread = 0.01 # Spreading probability
p_tree_1_growth = np.array([1.0, 1.0, 1.0]) # Probability of tree 1 growth for each forest
p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
infection_time = 10 # Number of steps an infection lasts
iterations = 1000 # Amount of simulation loops
relative_growth = 0.1 # Relative growth of tree 2 to tree 1 for harvest
min_age_agriculture = 45 # Minimum age of tree 1 until harvest
min_age_immune = 80 # Minimum age of tree 2 tree until harvest

# Choose which functions should be included in the simulation.
grow_trees = True
infect_trees = True
spread_disease = True
harvest_forest = True

# Initialize forests.
forest_amount = 3 # Amount of forests that should be intialized
initial_forest_value = [-1, -2, -1] # The initial value of the forest before added patches or random placements

use_patches =         [False, True, False]
patch_offset_x =      [0,     0,     0]
patch_offset_y =      [0,     0,     0]
patch_width =         [5,     10,    5]
patch_height =        [5,     10,    5]
patch_hspacing =      [1,     5,     1]
patch_vspacing =      [1,     5,     1]
patch_value =         [-1,   -1,    -1]

use_random_placements = [False, False, True]
tree_1_probability =    [0.00, 0.00, 0.00]
tree_2_probability =    [0.2, 0.7, 0.25]
use_distribution_of_forest = [-1, -1, 1]

# Decide what should be plotted.
plot_forest = True
iterations_to_plots = 100
plot_wood_outcome = True
plot_infected_amount = True
plot_sustainability = True
plot_tree_amount = True
plot_empty_areas = True

# Initialize data lists.
wood_outcome = np.zeros((forest_amount, iterations))
infected_amount = np.zeros((forest_amount, iterations))
sustainability = np.zeros((forest_amount, iterations))
amount_tree_agriculture = np.zeros((forest_amount, iterations))
amount_tree_immune = np.zeros((forest_amount, iterations))
amount_empty_areas = np.zeros((forest_amount, iterations))

forests = np.zeros((forest_amount, forest_size, forest_size))

for i in range(forest_amount):
    if ((not use_random_placements) or (use_distribution_of_forest[i] == -1)):
        forests[i] = InitializeForest(forest_size, initial_forest_value[i], use_patches[i], patch_offset_x[i], patch_offset_y[i], patch_width[i], \
                                  patch_height[i], patch_hspacing[i], patch_vspacing[i], patch_value[i], use_random_placements[i],
                                  tree_1_probability[i], tree_2_probability[i])

for i in range(forest_amount):
    if (use_random_placements and (use_distribution_of_forest[i] > -1)):
        index = use_distribution_of_forest[i]
        tree_2_prob = np.sum(forests[index] == -2) / np.sum(forests[index] < 0)
        forests[i] = InitializeForest(forest_size, initial_forest_value[i], use_patches[i], patch_offset_x[i], patch_offset_y[i], patch_width[i], \
                                  patch_height[i], patch_hspacing[i], patch_vspacing[i], patch_value[i], use_random_placements[i],
                                  0, tree_2_prob)

for i in range(forest_amount):
    forest = np.copy(forests[i])
    age_list = np.zeros([forest_size, forest_size]) # Initial ages
    infection_time_list = np.zeros([forest_size, forest_size]) # Initial infection times
    
    print("Forest", i, "initializes with", np.sum(forest == -1), "type 1 trees and", np.sum(forest == -2), "type 2 trees.", np.sum(forest == -2) / (forest_size ** 2))
    
    
    for j in range(iterations):
        
        # Plot the forest
        if (plot_forest):
            if (iterations_to_plots > 0):
                if (j % iterations_to_plots == 0):
                    plt.matshow(forest, vmin=-2, vmax=1)
                    plt.show()
        
        amount_tree_agriculture[i, j] = np.sum(forest == -1)
        amount_tree_immune[i, j] = np.sum(forest == -2)
        amount_empty_areas[i, j] = np.sum(forest == 0) / np.sum(forests[i] == -1)
        infected_amount[i, j] = np.sum(forest == 1) / np.sum(forests[i] == -1)
        
        forest, age_list, infection_time_list = TreeDeath(forest, age_list, infection_time, infection_time_list)
        
        # Grow trees at empty areas
        if (grow_trees):
            forest = GrowTrees(forest, p_tree_1_growth[i], p_tree_2_growth[i])
        
        # Infect trees at random with given probability
        if (infect_trees):
            forest[(np.random.rand(forest_size, forest_size) < p_infection) & (forest == -1)] = 1
        
        # Spread disease from already infected trees
        if (spread_disease):
            forest = SpreadDisease(forest, age_list, infection_time, p_spread)
        
        
        
        # Get wood outcome from harvest
        if (harvest_forest):
            wood_outcome[i, j] = HarvestForest(forest, age_list, min_age_agriculture, min_age_immune, relative_growth)
            sustainability[i, j] = SustainabilityCheck(forest, age_list, min_age_agriculture, min_age_immune)
        
        # Update age
        age_list, infection_time_list = AgeCounter(age_list, infection_time_list, forest)

if (plot_wood_outcome):
    plotForestData(wood_outcome, "Iterations", "Wood outcome", [min_age_agriculture, min_age_immune], None, ["Min age agriculture", "Min age immune"])

if (plot_infected_amount):
    plotForestData(infected_amount, "Iterations", "Amount of infected trees")

if (plot_empty_areas):
    plotForestData(amount_empty_areas, "Iterations", "Amount of empty areas")

if (plot_sustainability):
    plotForestData(sustainability, "Iterations", "Non harvestable trees / total amount of trees")

if (plot_tree_amount):
    plotForestData(amount_tree_agriculture, "Iterations", "Amount of agricultural trees")
    plotForestData(amount_tree_immune, "Iterations", "Amount of immune trees")
