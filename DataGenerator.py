# -*- coding: utf-8 -*-
'''
Created on 2014年12月4日

@author: cheng.li
'''

import pandas as pd

class DataGenerator:
    
    def __init__(self, path):
    
        res = pd.read_csv(path, encoding = 'gb2312', parse_dates  = [0])
        print res
        pass
        
import unittest

class TestDataGenerator(unittest.TestCase):


    def testDataGenerator(self):
        DataGenerator('data/161812.csv')
