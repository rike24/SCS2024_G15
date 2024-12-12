# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:21:19 2024

@author: Bryanz
"""
import numpy as np
from phase_diagram import PhaseDiagram
from initialize_forest import generate_forest
from plots import plotPhaseDiagram


forest_size = 50  #100 Sides of the forest
p_growth = 0.005  # Growth probability
p_infection = 1/(forest_size ** 2 * 20) # Infection probability
p_spread = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06] # Spreading probability
p_tree_1_growth = 1.0 # Probability of tree 1 growth for each forest
p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
p_tree_1_conv_growth = 0.005
p_tree_2_conv_growth = 0.01 - p_tree_1_conv_growth
infection_time = [0, 10, 20, 30, 40, 50, 60] # Number of steps an infection lasts
iterations = 30 #300 Amount of simulation loops
relative_growth = 2 # Relative growth of tree 2 to tree 1 for harvest
min_age_agriculture = 0 # 45 # Minimum age of tree 1 until harvest
min_age_immune = 0 #80 # Minimum age of tree 2 tree until harvest

forest_0 = generate_forest(0, forest_size)
forest_1 = generate_forest(1, forest_size)
forest_2 = generate_forest(2, forest_size)

wood_outcome_0 = PhaseDiagram(forest_0, iterations, infection_time, 
                  p_growth, p_tree_1_growth , p_tree_2_growth,
                 p_tree_1_conv_growth, p_tree_2_conv_growth, p_infection, p_spread, min_age_agriculture, min_age_immune, relative_growth )
wood_outcome_1 = PhaseDiagram(forest_1, iterations, infection_time, 
                  p_growth, p_tree_1_growth , p_tree_2_growth,
                 p_tree_1_conv_growth, p_tree_2_conv_growth, p_infection, p_spread, min_age_agriculture, min_age_immune, relative_growth )
    
wood_outcome_2 = PhaseDiagram(forest_2, iterations, infection_time, 
                  p_growth, p_tree_1_growth , p_tree_2_growth,
                 p_tree_1_conv_growth, p_tree_2_conv_growth, p_infection, p_spread, min_age_agriculture, min_age_immune, relative_growth )
    
wood_outcome_combined = np.zeros((wood_outcome_0.shape[0], wood_outcome_0.shape[1], 3)) 
wood_outcome_combined[:,:,0] = wood_outcome_0 
wood_outcome_combined[:,:,1] = wood_outcome_1
wood_outcome_combined[:,:,2] = wood_outcome_2
wood_outcome_combined /= np.max(wood_outcome_combined)
plotPhaseDiagram(wood_outcome_combined, "p_spread", "infection_time")
print(wood_outcome_0)
print(wood_outcome_2)
print(wood_outcome_1)