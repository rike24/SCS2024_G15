import numpy as np

def InitializeForest(forest_size, initial_forest_value, use_patches, patch_offset_x, patch_offset_y, patch_width, patch_height, \
                     patch_hspacing, patch_vspacing, patch_value, use_random_placements, tree_1_probability, tree_2_probability):
    forest = np.zeros((forest_size, forest_size)) + initial_forest_value
    if (use_patches):
        forest = AddPatches(forest, patch_offset_x, patch_offset_y, \
                            patch_width, patch_height, patch_hspacing, patch_vspacing, patch_value)
    if (use_random_placements):
        forest = AddRandomPlacements(forest, -1, tree_1_probability)
        forest = AddRandomPlacements(forest, -2, tree_2_probability)
    return forest

def AddPatches(forest, offset_x, offset_y, width, height, hspacing, vspacing, value):
    forest_patch = np.pad(np.ones((height, width)), ((0, vspacing), (0, hspacing)))
    temp_forest = np.tile(forest_patch, np.array(forest.shape) // np.array(forest_patch.shape) + [1, 1])
    temp_forest = np.pad(temp_forest, ((offset_x, 0), (offset_y, 0)))
    temp_forest = temp_forest[:forest.shape[0], :forest.shape[1]]
    forest[temp_forest == 1] = value
    return forest

def AddRandomPlacements(forest, value, probability):
    r = np.random.rand(forest.shape[0], forest.shape[1])
    forest[r < probability] = value
    return forest