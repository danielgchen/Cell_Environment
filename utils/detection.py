'''
create detection mechanisms for a piece of object
'''
from collections.abc import Sequence
from .template import *
import numpy as np

# detect via membrane to center overlap
def membrane_to_center_overlap(
    center1: Sequence,
    radius1: float,
    center2: Sequence,
    perc: float):
    '''
    given two centers and two radii we consider a center1 to membrane object
    if center2 is a certain percentage from center1 to membrane return True
    we consider perc == 1 to be at membrane and perc == 0 to be at center1
    '''
    # validate parameters
    if(perc > 1 or perc < 0):
        raise ValueError(raise_value_error_badparam.format('perc'))
    # compute distance
    if(not isinstance(center1, np.ndarray)):
        center1 = np.array(center1)
    if(not isinstance(center2, np.ndarray)):
        center2 = np.array(center2)
    distance = np.linalg.norm(center1 - center2)
    # test if center2 within perc * radius1 of center1
    overlap = (radius1 * perc) >= distance
    # return value
    return overlap
