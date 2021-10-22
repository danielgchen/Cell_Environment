'''
create detection mechanisms for a piece of object
'''
from collections.abc import Sequence
from .template import *
import numpy as np

# calculate membrane to center distance
def membrane_to_center_distance(
    center1: Sequence,  # TODO: change to sequence of floats
    center2: Sequence):  # TODO: change to sequence of floats
    '''
    given two centers we return the distance
    '''
    # compute distance
    if(not isinstance(center1, np.ndarray)):
        center1 = np.array(center1)
    if(not isinstance(center2, np.ndarray)):
        center2 = np.array(center2)
    distance = np.linalg.norm(center1 - center2)
    # return the distance
    return distance


# detect via membrane to center overlap
def membrane_to_center_overlap(
    center1: Sequence,  # TODO: change to sequence of floats
    radius1: float,
    center2: Sequence,  # TODO: change to sequence of floats
    perc: float):
    '''
    given two centers and two radii we consider a center1 to membrane object
    if center2 is a certain percentage from center1 to membrane return True
    we consider perc == 1 to be at membrane and perc == 0 to be at center1
    '''
    # validate parameters
    if(perc < 0):
        raise ValueError(raise_value_error_badparam.format('perc', perc))
    # compute distance
    distance = membrane_to_center_distance(center1, center2)
    # test if center2 within perc * radius1 of center1
    overlap = (radius1 * perc) >= distance
    # return value
    return overlap


# get the detected centers from a list of centers
def membrane_to_center_objectlist(
    center1: Sequence,  # TODO: change to sequence of floats
    radius1: float,
    object2s: Sequence,  # TODO: change to sequence of tuple(object, tuple(float, float))
    perc: float):
    '''
    given list of objects formatted as a tuple of object, center return the objects
    and centers that overlap under a given percentage with the center1
    '''
    # define the objects to return that pass the filter
    valid_objects = []
    # loop through all of the objects
    for object2, center2 in object2s:
        if(membrane_to_center_overlap(center1, radius1, center2, perc)):
            valid_objects.append((object2, center2))
    # return the passing objects
    return valid_objects
