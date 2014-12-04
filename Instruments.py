# -*- coding: utf-8 -*-
'''
Created on 2014年12月3日

@author: cheng.li
'''

class LeveragedFund:
    
    def __init__(self, 
                 levelAFrac,
                 levelBFrac,
                 settlementDays = 2,
                 adjustmentDates = []):
        
        self.levelAFrac = levelAFrac
        self.levelBFrac = levelBFrac
        self.settlementDays = settlementDays
        self.adjustmentDates = adjustmentDates

import unittest

class TestInstruments(unittest.TestCase):

    def testLeveragedFund(self):
        pass
