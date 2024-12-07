# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 06:11:00 2024

@author: zishan

All previous versions of the function. 
"""
#%%
import numpy as np

#%% Function to spread the disease.
def SpreadDisease(forest, infected_positions_i, infected_positions_j, pSpread):
    """
    Function to propagate the disease on a populated forest.
    
    Parameters
    ==========
    forest : 2-dimensional array. -1 for healthy trees, 1 for infected trees, 0 for empty cells.
    infected_positions_i & j : List of the coordinates of all infected trees.
    pSpread : Probability of spreading the disease.
    """
    
    Ni, Nj = forest.shape  # Dimensions of the forest.

    active_i = infected_positions_i
    active_j = infected_positions_j
        
    if len(active_i) > 0:
        for n in np.arange(len(active_i)):
            # Coordinates of cell up.
            i = (active_i[n] + 1) % Ni
            j = active_j[n]
            # Check status
            if forest[i, j] == -1:
                r = np.random.rand()
                if r < pSpread:
                    forest[i, j] = 1  # Infects the current tree.

            # Coordinates of cell down.
            i = (active_i[n] - 1) % Ni
            j = active_j[n]
            # Check status
            if forest[i, j] == -1:
                r = np.random.rand()
                if r < pSpread:
                    forest[i, j] = 1  # Infects the current tree.

            # Coordinates of cell left.
            i = active_i[n]
            j = (active_j[n] - 1) % Nj
            # Check status
            if forest[i, j] == -1:
                r = np.random.rand()
                if r < pSpread:
                    forest[i, j] = 1  # Infects the current tree.

            # Coordinates of cell right.
            i = active_i[n]
            j = (active_j[n] + 1) % Nj
            # Check status
            if forest[i, j] == -1:
                r = np.random.rand()
                if r < pSpread:
                    forest[i, j] = 1  # Infects the current tree.

    return forest


#%% Function to spread the disease.

'''
When encountering any issues with the new version of the function, 
please use the following stable version of the function.
'''

'''
import numpy as np
from scipy.signal import convolve2d

def SpreadDisease(forest, pSpread):
    """
    Function to propagate the disease on a populated forest.
    
    Parameters
    ==========
    forest : 2-dimensional array. -1 for healthy trees, 1 for infected trees, 0 for empty cells.
    pSpread : Probability of spreading the disease.
    """
    infected_index = np.where(forest == 1)
    infected_positions_i = infected_index[0]
    infected_positions_j = infected_index[1]


    # Changing value of infected_state and healthy_state might cause big problem!!!!!
    spread_scope = 1  # scope of spreading the disease
    infected_state = 1 # state of infected trees
    healthy_state = -1 # state of healthy trees
    empty_state = 0 # state of empty cells

    # bias to avoid log(0) problem
    bias = 1e-10

    # filter of infected trees
    infected_matrix = np.zeros(forest.shape)
    infected_matrix[infected_positions_i, infected_positions_j] = infected_state
    # add periodic boundary conditions to badding
    padded_infected_matrix = np.pad(infected_matrix, spread_scope , mode='wrap')
    # process to calculate the probability that the center tree get infected
    p_matrix = np.log(1 - padded_infected_matrix*pSpread + bias)
    kernel = np.ones((2*spread_scope+1, 2*spread_scope+1))
    p_matrix = convolve2d(p_matrix, kernel, mode='valid')
    p_matrix = 1 - np.exp(p_matrix)
    # generate random matrix to compare with the probability matrix
    random_matrix = np.random.rand( p_matrix.shape[0], p_matrix.shape[1])
    # determine the infected trees
    infected_matrix[random_matrix < p_matrix] = infected_state
    # intersection of infected trees and healthy trees
    infected_matrix = infected_matrix * (forest == healthy_state)
    # update the forest
    forest[infected_matrix == infected_state] = infected_state
    return forest
'''

#%%

'''
A brand-new partially completed disease spread function that fully utilizes matrix operations
and avoids the use of potentially risky log-plus-exp techniques. It supports infection time factors,
age factors, and distance factors. The function allows the use of convolution 
kernels of different sizes as needed (e.g., based on the age of the target healthy tree).
For now, it uses a predefined 5*5 convolution kernel. And the factors are all set to 1 until further notice.

If encontering any issues, please use the above stable version of the function.^
'''

'''
import numpy as np
from scipy.signal import convolve2d
import time
import torch
import torch.nn.functional as F


def SpreadDisease(forest_state, age_list, infection_time, p_spread):
    """
    Simulates disease spread in a forest.

    Parameters:
        forest_state (numpy.ndarray): N x N matrix representing the forest state.
        age_list (numpy.ndarray): N x N matrix representing the age of each tree.
        infection_time (numpy.ndarray): N x N matrix recording infection time.
        p_spread (float): Base probability of successful disease transmission.

    Returns:
        numpy.ndarray: Updated forest_state matrix.
    """

    start_time = time.time()

    # Define 5x5 convolution kernel
    kernel = np.array([
        [0.5, 0.5, 0.5, 0.5, 0.5],
        [0.5, 1.0, 1.0, 1.0, 0.5],
        [0.5, 1.0, 0.0, 1.0, 0.5],
        [0.5, 1.0, 1.0, 1.0, 0.5],
        [0.5, 0.5, 0.5, 0.5, 0.5]
    ])

    # Helper functions
    def infection_time_factor(duration):
        return np.ones_like(duration)
        

    def age_factor(age):
        return np.ones_like(age)
        

    # Convert input matrices to PyTorch tensors
    forest_state_tensor = torch.tensor(forest_state, dtype=torch.float32)
    infected_mask = (forest_state_tensor == 1).float().unsqueeze(0).unsqueeze(0)
    infected_mask = F.pad(infected_mask, (2, 2, 2, 2), mode='circular')

    # Perform unfolding using F.unfold
    N = forest_state.shape[0]
    infected_unfolded = F.unfold(infected_mask, kernel_size=(5, 5), padding=0).squeeze(0)

    # Map infection_time and age to corresponding factors and convert to PyTorch tensors
    duration_matrix = torch.tensor(infection_time_factor(infection_time), dtype=torch.float32).flatten()
    age_matrix = torch.tensor(age_factor(age_list), dtype=torch.float32).flatten()

    # Tile the factors to match unfolded dimensions
    duration_matrix = duration_matrix.repeat(25, 1)
    age_matrix = age_matrix.repeat(25, 1)

    # Transform kernel into PyTorch tensor and expand dimensions
    kernel_tensor = torch.tensor(kernel.flatten(), dtype=torch.float32).unsqueeze(1)
    #print("kernel_tensor:", kernel_tensor)
    # Compute final P_matrix
    P_matrix = infected_unfolded * p_spread* duration_matrix * age_matrix
    P_matrix = P_matrix * kernel_tensor
    #print("P_matrix:", P_matrix)

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

    print("Elapsed time:", time.time() - start_time)

    return forest_state
'''



# %%
N = 10000
# random forest with 10% of trees infected.
initial_forest = np.random.choice([-1, 0, 1], size=(N, N), p=[0.9, 0.09, 0.01])
# plot the forest
import matplotlib.pyplot as plt
plt.imshow(initial_forest, cmap='viridis')
plt.colorbar()
plt.show()


# %%
# Spread the disease
# index of infected trees
infected_index = np.where(initial_forest == 1)
initial_forest = SpreadDisease(initial_forest, infected_index[0], infected_index[1] , 0.7)
# plot the forest
plt.imshow(initial_forest, cmap='viridis')
plt.colorbar()
plt.show()

# %%
