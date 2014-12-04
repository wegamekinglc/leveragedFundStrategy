# -*- coding: utf-8 -*-
'''
Created on 2014年12月3日

@author: cheng.li
'''

class MinutesQuote:
    
    def __init__(self,
                 name,
                 quteDuration,
                 date,
                 time,
                 openPrice,
                 highPrice,
                 lowPrice,
                 closePrice,
                 volume,
                 amount):
        
        self.name = name
        self.quoteDuration = quteDuration
        self.date = date
        self.time = time
        self.open = openPrice
        self.high = highPrice
        self.low = lowPrice
        self.close = closePrice
        self.volume = volume
        self.amount = amount


import unittest

class TestQuotes(unittest.TestCase):


    def testMinutesQuote(self):
        pass

