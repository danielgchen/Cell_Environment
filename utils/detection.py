'''
create detection mechanisms for a piece of object
'''
from collections.abc import Sequence
from .template import *
import numpy as np

# calculate membrane to center distance
def center_to_center_distance(
    center1: Sequence,
    center2: Sequence):
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


# TODO: add testing mechanisms for exclusive
# detect via membrane to center overlap
def membrane_to_center_overlap(
    center1: Sequence,
    radius1: float,
    center2: Sequence,
    perc: float,
    exclusive: bool):
    '''
    given two centers and two radii we consider a center1 to membrane object
    if center2 is a certain percentage from center1 to membrane return True
    we consider perc == 1 to be at membrane and perc == 0 to be at center1
    '''
    # validate parameters
    if(perc < 0):
        raise ValueError(raise_value_error_badparam.format('perc', perc))
    # compute distance
    distance = center_to_center_distance(center1, center2)
    # test if center2 within perc * radius1 of center1
    if(exclusive):
        overlap = distance < (radius1 * perc)
    else:  # inclusive
        overlap = distance <= (radius1 * perc)
    # return value
    return overlap


# TODO: add testing mechanisms for exclusive
# get the detected centers from a list of centers
def membrane_to_center_objectlist(
    center1: Sequence,
    radius1: float,
    object2s: Sequence,
    perc: float,
    exclusive: bool):
    '''
    given list of objects formatted as a tuple of object, center return the objects
    and centers that overlap under a given percentage with the center1
    '''
    # define the objects to return that pass the filter
    valid_objects = []
    # loop through all of the objects
    for object2, center2 in object2s:
        if(membrane_to_center_overlap(center1, radius1, center2, perc, exclusive)):
            valid_objects.append((object2, center2))
    # return the passing objects
    return valid_objects

# TODO: add testing mechanisms for exclusive
# get the detected centers from a list of centers
def membrane_to_center_objectlist_nparray(
    center1: Sequence,
    radius1: float,
    object2s: Sequence,
    perc: float,
    exclusive: bool):
    '''
    given list of objects formatted as a tuple of object, center return the objects
    and centers that overlap under a given percentage with the center1
    '''
    # define the objects to return that pass the filter
    valid_objects = []
    # loop through all of the objects
    for row in object2s:
        if(membrane_to_center_overlap(center1, radius1, row[1:], perc, exclusive)):
            valid_objects.append((row[0], row[1:]))
    # return the passing objects
    return valid_objects
