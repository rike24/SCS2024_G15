import numpy as np
import matplotlib.pyplot as plt
from grow_trees import GrowTrees
from conv_disease_spread import SpreadDisease
from harvest_forest import HarvestForest
from update_age import AgeCounter
from initialize_forest import InitializeForest
from tree_death import TreeDeath
from sustainability_check import SustainabilityCheck

# Simulation parameters
forest_size = 100  # Sides of the forest
p_growth = 0.005  # Growth probability
p_infection = 0.0001 # Infection probability
p_spread = 0.02 # Spreading probability
p_tree_1_growth = np.array([1.0, 0.5, 0.5]) # Probability of tree 1 growth for each forest
p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
infection_time = 20 # Number of steps an infection lasts
iterations = 300 # Amount of simulation loops
relative_growth = 0.4 # Relative growth of tree 2 to tree 1 for harvest
min_age_agriculture = 25 # Minimum age of tree 1 until harvest
min_age_immune = 50 # Minimum age of tree 2 tree until harvest

grow_trees = True
infect_trees = True
spread_disease = True
harvest_forest = True

forest_amount = 3 # Amount of forests that should be intialized
initial_forest_value = [-1, -2, -2] # The initial value of the forest before added patches or random placements

use_patches =         [False, True, True]
patch_offset_x =      [0,     0,     0]
patch_offset_y =      [0,     0,     0]
patch_width =         [5,     10,    3]
patch_height =        [5,     10,    3]
patch_hspacing =      [1,     1,     1]
patch_vspacing =      [1,     1,     1]
patch_value =         [-1,   -1,    -1]

use_random_placements = [False, False, False]
tree_1_probability =    [0.00, 0.00, 0.00]
tree_2_probability =    [0.02, 0.7, 0.02]

plot_forest = True
iterations_to_plots = 100
plot_wood_outcome = True
plot_infected_amount = True
plot_sustainability = True

wood_outcome = np.zeros((forest_amount, iterations))
infected_amount = np.zeros((forest_amount, iterations))
sustainability = np.zeros((forest_amount, iterations))

for i in range(forest_amount):
    forest = InitializeForest(forest_size, initial_forest_value[i], use_patches[i], patch_offset_x[i], patch_offset_y[i], patch_width[i], \
                              patch_height[i], patch_hspacing[i], patch_vspacing[i], patch_value[i], use_random_placements[i],
                              tree_1_probability[i], tree_2_probability[i])
    
    age_list = np.zeros([forest_size, forest_size]) # Initial ages
    infection_time_list = np.zeros([forest_size, forest_size]) # Initial infection times
    
    print("Forest", i, "initializes with", np.sum(forest == -1), "type 1 trees and", np.sum(forest == -2), "type 2 trees.")
    
    
    for j in range(iterations):
        
        # Plot the forest
        if (plot_forest):
            if (iterations_to_plots > 0):
                if (j % iterations_to_plots == 0):
                    plt.matshow(forest, vmin=-2, vmax=1)
                    plt.show()
        
        forest, age_list, infection_time_list = TreeDeath(forest, age_list, infection_time, infection_time_list)
        
        # Grow trees at empty areas
        if (grow_trees):
            forest = GrowTrees(forest, p_growth, p_tree_1_growth[i], p_tree_2_growth[i])
        
        # Infect trees at random with given probability
        if (infect_trees):
            forest[(np.random.rand(forest_size, forest_size) < p_infection) & (forest == -1)] = 1
        
        # Spread disease from already infected trees
        if (spread_disease):
            forest = SpreadDisease(forest, age_list, infection_time, p_spread)
        
        # Get the current amount of infected trees
        infected_amount[i, j] = np.sum(forest == 1)
        
        # Get wood outcome from harvest
        if (harvest_forest):
            wood_outcome[i, j] = HarvestForest(forest, age_list, min_age_agriculture, min_age_immune, relative_growth)
            sustainability[i, j] = SustainabilityCheck(forest, age_list, min_age_agriculture, min_age_immune)
        
        # Update age
        age_list, infection_time_list = AgeCounter(age_list, infection_time_list, forest)

# Plot the wood outcome
if (plot_wood_outcome):
    for i in range(forest_amount):
        plt.plot(range(iterations), wood_outcome[i, :iterations])
    plt.xlabel("Iterations")
    plt.ylabel("Wood outcome")
    plt.axvline(min_age_agriculture, linestyle="dashed")
    plt.axvline(min_age_immune, linestyle="dashed")
    if (forest_amount > 1):
        plt.legend(["Forest " + str(i) for i in range(forest_amount)] + ["Min age agriculture", "Min age immune"])
    plt.show()

# Plot the amount of infected trees
if (plot_infected_amount):
    for i in range(forest_amount):
        plt.plot(range(iterations), infected_amount[i, :iterations])
    plt.xlabel("Iterations")
    plt.ylabel("Amount of infected trees")
    if (forest_amount > 1):
        plt.legend(["Forest " + str(i) for i in range(forest_amount)])
    plt.show()

# Plot the non harvestable trees / total amount of trees
if (plot_sustainability):
    for i in range(forest_amount):
        plt.plot(range(iterations), sustainability[i, :iterations])
    plt.xlabel("Iterations")
    plt.ylabel("non harvestable trees / total amount of trees")
    if (forest_amount > 1):
        plt.legend(["Forest " + str(i) for i in range(forest_amount)])
    plt.show()
