# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 09:53:39 2012

@author: dpiscia
"""


import unittest
import zone


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.prova = zone.zone('.\green_test_no_vent')

    def test_temperature_closed(self):
        # make sure the shuffled sequence does not lose any elements
        self.prova = zone.zone('.\green_test_no_vent')
        self.prova.T[8,9]
        self.assertEqual(self.prova.T[8,8], 278.93615489353033)

    def test_temperature_40_degree_u_2(self):
        # make sure the shuffled sequence does not lose any elements
        self.prova = zone.zone('.\green_test_40_vent')
        self.prova.T[8,9]
        self.assertEqual(self.prova.T[8,8], 276.10736259459225)


if __name__ == '__main__':
    unittest.main()