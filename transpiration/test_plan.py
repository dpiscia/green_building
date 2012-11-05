# -*- coding: utf-8 -*-
"""
Created on Mon Nov 05 13:12:50 2012

@author: dpiscia
"""

import model_functions
import unittest

class Test_model_functions(unittest.TestCase):
    def test_saturation(self):
        element = model_functions.saturated_pressure(280)
        self.assertTrue(element in [991.6921822308622])

if __name__== '__main__':
    unittest.main()