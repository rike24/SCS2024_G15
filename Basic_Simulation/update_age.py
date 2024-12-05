import numpy as np


def AgeCounter(age_list, infection_time_list, forest):
    """
    Function to update tree age and time of infection

    Parameters
    ----------
    ageList : NxN array, recording ages of trees (=0 if no tree in that position)
    infectionTimeList : NxN array, recording how long each tree has been infected
    forest : NxN array of forest state

    """

    healthy = np.where(forest < 0)  # in case of new species: species A = -1, species B = -2, etc
    age_list[healthy] += 1

    infected = np.where(forest == 1)
    infection_time_list[infected] += 1

    return age_list, infection_time_list
