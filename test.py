import unittest
import numpy as np
from tkinter import *
from tkinter import ttk
from utils import *
from cell import *
from food import *


# helper methods
# > create the base cell and food for the tests
def generate_environment():
    '''
    creates a canvas and food and cell object
    '''
    # create the environment
    canvas = Canvas(Tk())
    np.random.seed(0)  # ensure consistency
    # create the cell
    test_cell = Cell(canvas)
    # create the food
    test_food = Food(canvas)
    # return the environment objects
    return canvas, test_cell, test_food


# test suites
class TestDetectionMethods(unittest.TestCase):
    # test `membrane_to_center_distance`
    def test_membrane_to_center_distance(self):
        # check that it computes the output properly
        predicted = membrane_to_center_distance([0,0], [3,4])
        expected = 5
        self.assertEqual(predicted, expected)

    # test `membrane_to_center_overlap`
    def test_membrane_to_center_overlap(self):
        # check that it identifies the output properly
        predicted = membrane_to_center_overlap([0,0], 10, [1,1], 1)
        expected = True
        self.assertEqual(predicted, expected)
        # check that it fails properly
        expected = 'PARAMETER \[perc\] OF VALUE \[-1\] IS NOT VALID'
        with self.assertRaisesRegex(ValueError, expected):
            membrane_to_center_overlap([0,0], 10, [1,1], -1)

    # test `membrane_to_center_overlap`
    def test_membrane_to_center_objectlist(self):
        # check that it returns the output properly
        predicted = membrane_to_center_objectlist([0,0], 10, [[1,[1,1]],[2,[3,4]]], 1)
        expected = [(1, [1, 1]), (2, [3, 4])]
        self.assertEqual(predicted, expected)


class TestTemplateMethods(unittest.TestCase):
    # test that the template for the raise error bad parameter is correct
    def test_raise_value_error_badparam(self):
        # check that it returns the output correctly
        predicted = raise_value_error_badparam.format('PARAM',1)
        expected = 'PARAMETER [PARAM] OF VALUE [1] IS NOT VALID'
        self.assertEqual(predicted, expected)


class TestCoreMethods(unittest.TestCase):
    # test `get_rand_angle`
    def test_get_rand_angle(self):
        # check that it calculates the value correctly
        np.random.seed(0)
        predicted = get_rand_angle()
        np.random.seed(0)
        expected = np.random.uniform(0, 2*np.pi)
        self.assertEqual(predicted, expected)

    # test `get_rand_color`
    def test_get_rand_color(self):
        # check that it calculates the value correctly
        np.random.seed(0)
        predicted = get_rand_color()
        expected = '#AC2F75'
        self.assertEqual(predicted, expected)

    # test `spin`
    def test_spin(self):
        # check that it calculates the value correctly
        np.random.seed(0)
        predicted = spin(0.548813503928)  # confirm 10^-12 accuracy
        expected = True
        self.assertEqual(predicted, expected)

    # test `adjust`
    def test_adjust(self):
        # check that it adjusts itself correctly given a non-continous value
        predicted = adjust(50, 0, 1, False)
        expected = 1
        self.assertEqual(predicted, expected)
        # check that it adjusts itself correctly given a continous value
        predicted = adjust(5.5, 0, 1, True)
        expected = 0.5
        self.assertEqual(predicted, expected)















    #


class TestFoodObject(unittest.TestCase):
    # test the food detection mechanism
    # > single food decision making
    def test_get_seen_singlefood(self):
        canvas, test_cell, test_food = generate_environment()  # get pieces
        test_cell.cell_center = (0,0)  # at the origin
        test_cell.genetics['cell_vision_scale'] = 10  # assume ultra-vision
        test_cell.genetics['cell_vision_nconsidered'] = 1  # assume single-food decision
        test_food.add_food_custom((5,5))  # add a food within it's vision
        diffs = test_food.get_seen(test_cell)  # get the considered movement
        predicted = np.sqrt(np.power(diffs, 2).sum())
        expected = test_cell.cell_step
        del canvas, test_cell, test_food
        self.assertEqual(predicted, expected)

    # > multiple food decision making
    def test_get_seen_multiplefood(self):
        canvas, test_cell, test_food = generate_environment()  # get pieces
        test_cell.cell_center = (0,0)  # at the origin
        test_cell.genetics['cell_vision_scale'] = 10  # assume ultra-vision
        test_cell.genetics['cell_vision_nconsidered'] = 2  # assume single-food decision
        test_food.add_food_custom((5,5))  # add a food within it's vision
        test_food.add_food_custom((-5,-5))  # add a food within it's vision
        diffs = test_food.get_seen(test_cell)  # get the considered movement
        predicted = np.sqrt(np.power(diffs, 2).sum())
        expected = 0
        self.assertEqual(predicted, expected)

    # > single food decision making
    def test_get_seen_withinboundary(self):
        canvas, test_cell, test_food = generate_environment()  # get pieces
        test_cell.cell_center = (0,0)  # at the origin
        test_cell.cell_radius = 2  # to get a designed boundary
        test_cell.genetics['cell_vision_scale'] = 5  # assume vision total of 1
        test_cell.genetics['cell_vision_nconsidered'] = 1  # assume single-food decision
        test_food.add_food_custom((0,10))  # add a food within it's vision
        diffs = test_food.get_seen(test_cell)  # get the considered movement
        predicted = np.sqrt(np.power(diffs, 2).sum())
        expected = test_cell.cell_step
        del canvas, test_cell, test_food
        self.assertEqual(predicted, expected)


class TestCellObject(unittest.TestCase):
    # test the cell movement mechanism
    # > given movement instructions
    def test_move_singlefood(self):
        canvas, test_cell, test_food = generate_environment()  # get pieces
        test_cell.cell_center = (0,0)  # at the origin
        test_cell.genetics['cell_vision_scale'] = 10  # assume ultra-vision
        test_cell.genetics['cell_vision_nconsidered'] = 1  # assume single-food decision
        test_food.add_food_custom((5,5))  # add a food within it's vision
        diffs = test_food.get_seen(test_cell)  # get the considered movement
        test_cell.move(diffs)
        predicteds = test_cell.cell_center
        expecteds = diffs
        for idx, predicted in enumerate(predicteds):
            self.assertEqual(predicted, expecteds[idx])
