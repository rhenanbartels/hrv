# coding: utf-8
import unittest

import numpy as np

from hrv import classical


class ClassicalIndexesTestCase(unittest.TestCase):
    def setUp(self):
        self.fake_rri = [800, 810, 815, 790]

    def test_right_function_call(self):
        response = classical.time_domain(self.fake_rri)
        expected = np.mean(self.fake_rri)
        self.assertEqual(response, expected)

