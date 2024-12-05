# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 06:11:00 2024

@author: zishan

All infected trees execute disease spreading for one time 
Applying convolution operation to spread the disease
"""
#%%
import numpy as np
from scipy.signal import convolve2d

#%% Function to spread the disease.
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


# %%
import numpy as np
from scipy.signal import convolve2d
# for spread_scope = 2, nearest neighbors distance_coefficient = 1, second nearest neighbors distance_coefficient = 0.5
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
    spread_scope = 2  # scope of spreading the disease          !!! for spread_scope = 2!!!
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
    # change the kernel to distance_coefficient, 1 for nearest neighbors, 0.5 for second nearest neighbors
    # need to be modified by hand for different spread_scope #
    kernel[0, :] = 0.5
    kernel[-1, :] = 0.5
    kernel[:, 0] = 0.5
    kernel[:, -1] = 0.5
    kernel[spread_scope, spread_scope] = 0
    print(kernel)
    # need to be modified by hand for different spread_scope #

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




# %%
import numpy as np
from scipy.signal import convolve2d
# for customised spread_scope, nearest neighbors distance_coefficient = 2^0, second nearest neighbors distance_coefficient = 2^-1...
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
    spread_scope = 3  # scope of spreading the disease          !!! for spread_scope = 2!!!
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
    # change the kernel to distance_coefficient, 1 for nearest neighbors, 0.5 for second nearest neighbors
    for kernel_layer in range(spread_scope):
        kernel[0+kernel_layer, 0+kernel_layer: 2*spread_scope + 1 - kernel_layer] = 2**(kernel_layer-spread_scope)
        kernel[-1-kernel_layer, 0+kernel_layer: 2*spread_scope + 1 - kernel_layer] = 2**(kernel_layer-spread_scope)
        kernel[0+kernel_layer: 2*spread_scope + 1 - kernel_layer, 0+kernel_layer] = 2**(kernel_layer-spread_scope)
        kernel[0+kernel_layer: 2*spread_scope + 1 - kernel_layer, -1 - kernel_layer] = 2**(kernel_layer-spread_scope)
        # kernel[-1-kernel_layer, 0+kernel_layer: -1 - kernel_layer] = 2**(kernel_layer-spread_scope)
        # kernel[0+kernel_layer: -1 - kernel_layer, 0+kernel_layer] = 2**(kernel_layer-spread_scope)
        # kernel[0+kernel_layer: -1 - kernel_layer, -1 - kernel_layer] = 2**(kernel_layer-spread_scope)
        # kernel[-1-kernel_layer, :] = 2**(kernel_layer-spread_scope)
        # kernel[:, 0+kernel_layer] = 2**(kernel_layer-spread_scope)
        # kernel[:, -1-kernel_layer] = 2**(kernel_layer-spread_scope)
    kernel[spread_scope, spread_scope] = 0

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


#%%
N = 10
# random forest with 10% of trees infected.
initial_forest = np.random.choice([-1, 0, 1], size=(N, N), p=[0.99, 0.0, 0.01])
# plot the forest
import matplotlib.pyplot as plt
plt.imshow(initial_forest, cmap='viridis')
plt.colorbar()
plt.show()


# %%
# Spread the disease
# index of infected trees
while True:
    initial_forest = SpreadDisease(initial_forest, 1)
    # plot the forest
    plt.imshow(initial_forest, cmap='viridis')
    plt.colorbar()
    plt.show()
    if np.sum(initial_forest == -1) == 0:
        break

# %%
