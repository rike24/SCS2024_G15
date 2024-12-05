import numpy as np
import matplotlib.pyplot as plt
from grow_trees import GrowTrees
from conv_disease_spread import SpreadDisease
from harvest_forest import HarvestForest
from update_age import AgeCounter
from initialize_forest import InitializeForest
from tree_death import TreeDeath

# Simulation parameters
forest_size = 64  # Sides of the forest
p_growth = 0.005  # Growth probability
p_infection = 0.0001 # Infection probability
p_spread = 0.04 # Spreading probability
p_tree_1_growth = 0.7 # Probability of tree 1 growth
p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth
infection_time = 20 # Minimum number of steps an infection lasts
iterations = 300 # Amount of simulation loops
mean_age = 50 # Mean age of forest until harvest

grow_trees = True
infect_trees = True
spread_disease = True
harvest_forest = True

forest_amount = 2 # Amount of forests that should be intialized
initial_forest_value = [-1, -2] # The initial value of the forest before added patches or random placements

use_patches =         [False, True]
patch_offset_x =      [0,     0]
patch_offset_y =      [0,     0]
patch_width =         [5,     5]
patch_height =        [5,     5]
patch_hspacing =      [1,     1]
patch_vspacing =      [1,     1]
patch_value =         [-1,   -1]

use_random_placements = [False, False]
tree_1_probability =    [0.00, 0.00]
tree_2_probability =    [0.02, 0.02]

plot_forest = True
iterations_to_plots = 10
plot_wood_outcome = True
plot_infected_amount = True

wood_outcome = np.zeros((forest_amount, iterations))
infected_amount = np.zeros((forest_amount, iterations))

for i in range(forest_amount):
    forest = InitializeForest(forest_size, initial_forest_value[i], use_patches[i], patch_offset_x[i], patch_offset_y[i], patch_width[i], \
                              patch_height[i], patch_hspacing[i], patch_vspacing[i], patch_value[i], use_random_placements[i],
                              tree_1_probability[i], tree_2_probability[i])
    
    age_list = np.zeros([forest_size, forest_size]) # Initial ages
    infection_time_list = np.zeros([forest_size, forest_size]) # Initial infection times
    
    for j in range(iterations):
        
        # Plot the forest
        if (plot_forest):
            if (iterations_to_plots > 0):
                if (j % iterations_to_plots == 0):
                    plt.matshow(forest, vmin=-2, vmax=1)
                    plt.show()
        
        forest, age_list, infection_time_list = TreeDeath(forest, age_list, 10, infection_time_list)
        
        # Grow trees at empty areas
        if (grow_trees):
            forest = GrowTrees(forest, p_growth, p_tree_1_growth, p_tree_2_growth)
        
        # Infect trees at random with given probability
        if (infect_trees):
            forest[(np.random.rand(forest_size, forest_size) < p_infection) & (forest == -1)] = 1
        
        # Spread disease from already infected trees
        if (spread_disease):
            forest = SpreadDisease(forest, p_spread)
        
        # Get the current wood outcome
        wood_outcome[i, j] = np.sum(age_list[forest < 0])
        
        # Get the current amount of infected trees
        infected_amount[i, j] = np.sum(forest == 1)
        
        # Get wood outcome from harvest
        if (harvest_forest):
            harvest_wood_outcome = HarvestForest(forest, age_list, mean_age)
            
            # Check if forest is harvested, if so exit loop
            if harvest_wood_outcome > -1:
                print("Forest has been harvested with wood outcome: ", harvest_wood_outcome)
                # Plot the forest
                if (plot_forest):
                    plt.matshow(forest, vmin=-2, vmax=1)
                    plt.show()
                break
        
        
        
        # Update age
        age_list, infection_time_list = AgeCounter(age_list, infection_time_list, forest)
        
        

        
# Plot the wood outcome
if (plot_wood_outcome):
    for i in range(forest_amount):
        plt.plot(range(mean_age), wood_outcome[i, :mean_age])
    plt.xlabel("Time")
    plt.ylabel("Wood outcome")
    if (forest_amount > 1):
        plt.legend([str(i) for i in range(forest_amount)])
    plt.show()

# Plot the amount of infected trees
if (plot_infected_amount):
    for i in range(forest_amount):
        plt.plot(range(mean_age), infected_amount[i, :mean_age])
    plt.xlabel("Time")
    plt.ylabel("Amount of infected trees")
    if (forest_amount > 1):
        plt.legend([str(i) for i in range(forest_amount)])
    plt.show()