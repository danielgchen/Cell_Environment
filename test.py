from utils import *
import unittest

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
