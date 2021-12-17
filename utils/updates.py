from .core import *

# TODO: add a testing function
# defines a method to add a new object
def add_to_env(object, objects, objects_attrs):
    '''
    given a new object it adds it to the environment
    '''
    # add to the list of tkinter objects
    objects.append(object)
    # add to the list of attributes
    objects_attrs = np.append(objects_attrs, [np.append(object.radius, object.center)], axis=0)
    return objects, objects_attrs


# TODO: add a testing function
# defines a method to remove an old object
def remove_from_env(object, idx, objects, objects_attrs):
    '''
    given an old object it removes it from the enviroment
    '''
    # remove it from the list of tkinter objects
    objects = objects.remove(object)
    # remove it from the list of attributes
    objects_attrs = np.delete(objects_attrs, idx)
