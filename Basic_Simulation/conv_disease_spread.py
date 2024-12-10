# -*- coding: utf-8 -*-
"""
Created on Sat Dec 07 10:21:00 2024

@author: zishan

Attention:
    New interface is applied to the function SpreadDisease
    The function SpreadDisease now takes 4 parameters:
        forest_state: N x N matrix representing the forest state.
        age_list: N x N matrix representing the age of each tree.
        infection_time: N x N matrix recording infection time.
        p_spread: Base probability of successful disease transmission.


All infected trees execute disease spreading for one time 
Applying convolution operation to spread the disease

If encounter any problem, please use old version of the 
function SpreadDisease in the file disease_spread.py

"""


#%%

'''

Add the function to adjust the spread scope of disease based on the age of the infected tree.
trees with different ages have different spread scopes.
The children trees(0-1 years old) can not spread the disease even if they are infected.
The trees with age between 1 and 20 can spread the disease in a 3*3 scope.
The trees with age between 20 and 40 can spread the disease in a 5*5 scope.
...
The trees with age over 80 can spread the disease in a 11*11 scope.

'''

import numpy as np
from scipy.signal import convolve2d
import time
import torch
import torch.nn.functional as F


def SpreadDisease(forest_state, age_list, infection_time, p_spread, tree_species = None, spread_matrix = None):
    """
    Simulates disease spread in a forest.

    Parameters:
        forest_state (numpy.ndarray): N x N matrix representing the forest state.
        age_list (numpy.ndarray): N x N matrix representing the age of each tree.
        infection_time (numpy.ndarray): N x N matrix recording infection time.
        tree_species (numpy.ndarray): N x N matrix representing the species of each tree. Note that 0 denotes empty cells.
        spread_matrix (numpy.ndarray): m x n matrix representing the spread of disease, m denotes the amount of tree species,
          n denotes the amount of disease types. For now, we only consider one type of disease(n=1). spread_matrix[i, 0] denotes
          the probability that species i get infected by disease 0. spread_matrix[0, :] should be set to 0 corresponding to empty cells.
        p_spread (float): Base probability of successful disease transmission.


    Returns:
        numpy.ndarray: Updated forest_state matrix.
    """
    if spread_matrix is not None:
        if spread_matrix.shape[1] > 1:
            raise ValueError("Only one type of disease is supported for now.")


    
    # define a 11*11 kernel representing the distance, the center is 0, the first layer is 1, second layer is 2, and so on
    KERNEL_SIZE = 11
    distance_kernel = np.array([
        [ 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [ 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        [ 5, 4, 3, 3, 3, 3, 3, 3, 3, 4, 5],
        [ 5, 4, 3, 2, 2, 2, 2, 2, 3, 4, 5],
        [ 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5],
        [ 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5],
        [ 5, 4, 3, 2, 1, 1, 1, 2, 3, 4, 5],
        [ 5, 4, 3, 2, 2, 2, 2, 2, 3, 4, 5],
        [ 5, 4, 3, 3, 3, 3, 3, 3, 3, 4, 5],
        [ 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        [ 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    ])


    # Helper functions

    def AgeLevel(age_list):
        age_level = np.zeros_like(age_list)
        
        age_level[(age_list <= 2)] = 0
        age_level[(age_list >= 20) & (age_list < 2)] = 1
        age_level[(age_list < 20)] = 2
        
        return age_level

    def advanced_distance_coe(unfolded_distance_kernel, age_list):
        age_level = AgeLevel(age_list)
        age_level_tensor = torch.tensor(age_level, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        padded_age_level = F.pad(age_level_tensor, (5, 5, 5, 5), mode='circular')
        unfolded_age_level = F.unfold(padded_age_level, kernel_size=(11, 11), padding=0).squeeze(0)
        distance_coe = 1 / torch.pow(2, unfolded_distance_kernel - 1)
        result = distance_coe * (unfolded_age_level - unfolded_distance_kernel >= 0)
        return result
        
    def species_factor(tree_species, spread_matrix, squared_kernel_size=121):
        species_coe = spread_matrix[tree_species].reshape(1, tree_species.shape[0]**2)
        species_coe = np.repeat(species_coe, squared_kernel_size, axis=0)
        species_coe_tensor = torch.tensor(species_coe, dtype=torch.float32)
        return species_coe_tensor
        

    def infection_time_factor(duration):
        return np.ones_like(duration)
        

    def age_factor(age):
        return np.ones_like(age)
        

    # Convert input matrices to PyTorch tensors
    forest_state_tensor = torch.tensor(forest_state, dtype=torch.float32)
    infected_mask = (forest_state_tensor == 1).float().unsqueeze(0).unsqueeze(0)
    infected_mask = F.pad(infected_mask, (5, 5, 5, 5), mode='circular')

    # Perform unfolding using F.unfold
    N = forest_state.shape[0]
    infected_unfolded = F.unfold(infected_mask, kernel_size=(11, 11), padding=0).squeeze(0)

    # Transform kernel into PyTorch tensor and expand dimensions
    unfolded_distance_kernel = torch.tensor(distance_kernel.flatten(), dtype=torch.float32).unsqueeze(1)
    # Compute final P_matrix
    distance_coe = advanced_distance_coe(unfolded_distance_kernel, age_list)

    if tree_species is None or spread_matrix is None:
        species_coe = 1
        #print("Warning: lack of species information, set species_coe to 1.")
    else:
        species_coe = species_factor(tree_species, spread_matrix)

    P_matrix = distance_coe * infected_unfolded * p_spread 
    P_matrix = P_matrix * species_coe

    # Calculate the probability of each tree being infected
    one_minus_P_matrix = 1 - P_matrix
    column_product = torch.prod(one_minus_P_matrix, dim=0)
    infection_probabilities = 1 - column_product
    #print("infection_probabilities:", infection_probabilities)

    # Reshape infection probability array back into an (N x N) matrix
    P_center_infected = infection_probabilities.view(N, N)
    #print("P_center_infected:", P_center_infected)

    # Generate random matrix and update infection status
    random_matrix = torch.rand((N, N))
    new_infections = (random_matrix < P_center_infected) & (forest_state_tensor == -1)
    forest_state_tensor[new_infections] = 1
    forest_state = forest_state_tensor.numpy()

    return forest_state




# #%%
# N = 500
# # random forest with 10% of trees infected.
# initial_forest = np.random.choice([-1, 0, 1], size=(N, N), p=[0.99, 0.0, 0.01])
# # plot the forest
# import matplotlib.pyplot as plt
# plt.imshow(initial_forest, cmap='viridis')
# plt.colorbar()
# plt.show()


# # %%
# # Spread the disease
# # index of infected trees

# # age of trees
# test_age_list = np.random.randint(0, 100, (N, N))

# test_infection_time = np.random.rand(N, N)

# random_values = np.random.randint(1, 3, size=(N, N))
# test_tree_species = np.zeros((N, N))
# test_tree_species[(initial_forest != 0)] = random_values[(initial_forest != 0)]
# test_tree_species = test_tree_species.astype(int)
# test_spread_matrix = np.random.rand(3, 1)
# test_spread_matrix[0, 0] = 0

# while True:
#     initial_forest = SpreadDisease(initial_forest, test_age_list, test_infection_time, 0.01)
#     # plot the forest
#     plt.imshow(initial_forest, cmap='viridis')
#     plt.colorbar()
#     plt.show()
#     if np.sum(initial_forest == -1) == 0:
#         break

# # # %%

# # %%
