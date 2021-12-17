import os
import hashlib
import unittest
import numpy as np
from tkinter import *
from tkinter import ttk
from tqdm import tqdm
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
    # create the cell
    test_cell = Cell(canvas)
    # create the food
    test_food = Food(canvas)
    # return the environment objects
    return canvas, test_cell, test_food


# test suites
class TestDetectionMethods(unittest.TestCase):
    # test `center_to_center_distance`
    def test_center_to_center_distance(self):
        # check that it computes the output properly
        predicted = center_to_center_distance([0,0], [3,4])
        expected = 5
        self.assertEqual(predicted, expected)

    # test `membrane_to_center_overlap`
    def test_membrane_to_center_overlap(self):
        # check that it identifies the output properly
        predicted = membrane_to_center_overlap([0,0], 10, [1,1], 1, False)
        expected = True
        self.assertEqual(predicted, expected)
        # check that it fails properly
        expected = 'PARAMETER \[perc\] OF VALUE \[-1\] IS NOT VALID'
        with self.assertRaisesRegex(ValueError, expected):
            membrane_to_center_overlap([0,0], 10, [1,1], -1, False)

    # test `membrane_to_center_overlap`
    def test_membrane_to_center_objectlist(self):
        # check that it returns the output properly
        predicted = membrane_to_center_objectlist([0,0], 10, [[1,[1,1]],[2,[3,4]]], 1, False)
        expected = [(1, [1, 1]), (2, [3, 4])]
        self.assertEqual(predicted, expected)


class TestTemplateMethods(unittest.TestCase):
    # test that the template for the raise error bad parameter is correct
    def test_raise_value_error_badparam(self):
        # check that it returns the output correctly
        predicted = raise_value_error_badparam.format('PARAM',1)
        expected = 'PARAMETER [PARAM] OF VALUE [1] IS NOT VALID'
        self.assertEqual(predicted, expected)


class TestReportingMethods(unittest.TestCase):
    # test that we write data correctly to the given tracking name
    def test_record_population_givenfname(self):
        # check that it writes the values correctly
        canvas, test_cell, test_food = generate_environment()  # get pieces
        # check that the file we will be writing to is okay
        tmp_track_filename = 'testtrack'
        if(os.path.exists(f'outputs/{tmp_track_filename}.txt')):
            os.system(f'rm -rf outputs/{tmp_track_filename}.txt')
        # define parameters and test function
        total_rounds, cell_color, count = 1, test_cell.cell_color, 5
        record_population([test_cell] * count, total_rounds, tmp_track_filename)  # call the method
        # check 1) the content 2) the sha512
        # > checking content
        with open(f'outputs/{tmp_track_filename}.txt', 'rt') as f:
            predicted_msg = f.read()
        expected_msg = f'{total_rounds},{cell_color},{count}\n'
        self.assertEqual(predicted_msg, expected_msg)
        os.system(f'rm -rf outputs/{tmp_track_filename}.txt')
        # > checking sha512
        predicted_hex = hashlib.sha512(predicted_msg.encode()).hexdigest()
        expected_hex = hashlib.sha512(expected_msg.encode()).hexdigest()
        self.assertEqual(predicted_hex, expected_hex)

    # test that we write data correctly to the default tracking name
    def test_record_population_defaultfname(self):
        # check that it writes the values correctly
        canvas, test_cell, test_food = generate_environment()  # get pieces
        # move the original track filename if it exists
        tmp_track_filename = 'switchtrack'
        if(os.path.exists(f'outputs/{track_filename}.txt')):
            os.system(f'mv outputs/{track_filename}.txt outputs/{tmp_track_filename}.txt')
        # define parameters and test function
        total_rounds, cell_color, count = 1, test_cell.cell_color, 5
        record_population([test_cell] * count, total_rounds)  # call the method
        # check 1) the content 2) the sha512
        # > checking content
        with open(f'outputs/{track_filename}.txt', 'rt') as f:
            predicted_msg = f.read()
        expected_msg = f'{total_rounds},{cell_color},{count}\n'
        self.assertEqual(predicted_msg, expected_msg)
        os.system(f'rm -rf outputs/{track_filename}.txt')
        if(os.path.exists(f'outputs/{tmp_track_filename}.txt')):
            os.system(f'mv outputs/{tmp_track_filename}.txt outputs/{track_filename}.txt')
        # > checking sha512
        predicted_hex = hashlib.sha512(predicted_msg.encode()).hexdigest()
        expected_hex = hashlib.sha512(expected_msg.encode()).hexdigest()
        self.assertEqual(predicted_hex, expected_hex)


class TestCoreMethods(unittest.TestCase):
    # test `get_rand_angle`
    def test_get_rand_angle(self):
        # check that it calculates the value correctly
        rng = np.random.default_rng(0)
        test_rng = np.random.default_rng(0)
        for _ in tqdm(range(int(1e5))):  # accuracte with five zeroes
            predicted = get_rand_angle(rng=rng)
            expected = test_rng.uniform(0, 2*np.pi)
            self.assertEqual(predicted, expected)

    # test `get_rand_color`
    def test_get_rand_color(self):
        # check that it calculates the value correctly
        rng = np.random.default_rng(0)
        test_rng = np.random.default_rng(0)
        for _ in tqdm(range(int(1e5))):  # accuracte with five zeroes
            predicted = get_rand_color(rng=rng)
            expected = '#%02X%02X%02X' % tuple([test_rng.integers(0, 256) for _ in range(3)])
            self.assertEqual(predicted, expected)

    # test `spin`
    def test_spin(self):
        # check that it calculates the value correctly
        rng = np.random.default_rng(0)
        test_rng = np.random.default_rng(0)
        for _ in tqdm(range(int(1e5))):  # accuracte with five zeroes
            chance = rng.uniform(0, 1)  # grab a number
            predicted = spin(chance, rng=rng)  # confirm 10^-12 accuracy
            _ = test_rng.uniform(0, 1)  # replicate the grab action
            expected = test_rng.uniform(0, 1) < chance
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
