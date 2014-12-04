# -*- coding: utf-8 -*-
'''
Created on 2014年12月3日

@author: cheng.li
'''

from math import sqrt
from collections import deque

class MovingAverage:
    
    def __init__(self, window):
        
        self.__result__  = 0.0
        self.__window__  = window
        self.__samples__ = 0
        self.__sampleList__ = deque()
        self.__isFull__ = False
        
    def dumpSample(self, sample):
        
        lastSum = self.__result__ * self.__samples__
        self.__sampleList__.append(sample)
        self.__samples__ += 1
        
        if not self.__isFull__:
            self.__result__ = (lastSum + sample) / len(self.__sampleList__)
            if len(self.__sampleList__) == self.__window__:
                self.__isFull__ = True
        else:
            eraseDate = self.__sampleList__.popleft()
            lastSum -= eraseDate
            self.__samples__ -= 1
            self.__result__ = (lastSum + sample) / self.__window__
            
    def getResult(self):
        
        return self.__result__
    
class MovingVariance:
    
    def __init__(self, window):
        
        self.__window__ = window
        self.__sum__ = 0.0
        self.__sumsq__ = 0.0
        self.__samples__ = 0
        self.__sampleList__ = deque()
        self.__isFull__ = False
        
    def dumpSample(self, sample):
        
        self.__sum__ += sample
        self.__sumsq__ += sample * sample
        self.__sampleList__.append(sample)
        self.__samples__ += 1
        
        if not self.__isFull__:
            if len(self.__sampleList__) == self.__window__:
                self.__isFull__ = True
        else:
            eraseDate = self.__sampleList__.popleft()
            self.__sum__ -= eraseDate
            self.__sumsq__ -= eraseDate * eraseDate
            self.__samples__ -= 1
            
    def getResult(self):
        
        return self.__sumsq__ / (self.__samples__ - 1) - self.__sum__ * self.__sum__ / self.__samples__ / (self.__samples__ - 1.0)
    
class MovingCorrelation:
    
    def __init__(self, window):
        
        self.__window__ = window
        self.__sumLeft__ = 0.0
        self.__sumRight__ = 0.0
        self.__sumLeftRight__ = 0.0
        self.__sumsqLeft__ = 0.0
        self.__sumsqRight__ = 0.0
        self.__samples__ = 0
        self.__sampleList__ = deque()
        self.__isFull__ = False
    
    def dumpSample(self, sample):
        
        leftData = sample[0]
        rightData = sample[1]
        
        self.__sumLeft__ += leftData
        self.__sumRight__ += rightData
        self.__sumsqLeft__ += leftData * leftData
        self.__sumsqRight__ += rightData * rightData
        self.__sumLeftRight__ += leftData * rightData
        self.__sampleList__.append(sample)
        self.__samples__ += 1
        
        if not self.__isFull__:
            if len(self.__sampleList__) == self.__window__:
                self.__isFull__ = True
        else:
            eraseDate = self.__sampleList__.popleft()
            leftData = eraseDate[0]
            rightData = eraseDate[1]
            self.__sumLeft__ -= leftData
            self.__sumRight__ -= rightData
            self.__sumsqLeft__ -= leftData * leftData
            self.__sumsqRight__ -= rightData * rightData
            self.__sumLeftRight__ -= leftData * rightData
            self.__samples__ -= 1
            
    def getResult(self):
        
        tmp = self.__sumLeftRight__ - self.__sumLeft__ * self.__sumRight__ / self.__samples__
        tmp /= sqrt((self.__sumsqLeft__ - self.__sumLeft__ * self.__sumLeft__ / self.__samples__) * (self.__sumsqRight__ - self.__sumRight__ * self.__sumRight__ / self.__samples__))
        return tmp

class CorrelationHolder:
    
    def __init__(self):
        
        self.__sumLeft__ = 0.0
        self.__sumRight__ = 0.0
        self.__sumLeftRight__ = 0.0
        self.__sumsqLeft__ = 0.0
        self.__sumsqRight__ = 0.0
        self.__samples__ = 0
    
    def dumpSample(self, sample):
        leftData = sample[0]
        rightData = sample[1]
        
        self.__sumLeft__ += leftData
        self.__sumRight__ += rightData
        self.__sumsqLeft__ += leftData * leftData
        self.__sumsqRight__ += rightData * rightData
        self.__sumLeftRight__ += leftData * rightData
        self.__samples__ += 1
    
    def getResult(self):
        
        tmp = self.__sumLeftRight__ - self.__sumLeft__ * self.__sumRight__ / self.__samples__
        tmp /= sqrt((self.__sumsqLeft__ - self.__sumLeft__ * self.__sumLeft__ / self.__samples__) * (self.__sumsqRight__ - self.__sumRight__ * self.__sumRight__ / self.__samples__))
        return tmp
    
class MovingRegression:
    
    def __init__(self, window, includeConstant = True):
        
        self.__window__ = window
        self.__includeConstant__ = includeConstant
        self.__sumLeft__ = 0.0
        self.__sumRight__ = 0.0
        self.__sumLeftRight__ = 0.0
        self.__sumsqLeft__ = 0.0
        self.__sumsqRight__ = 0.0
        self.__samples__ = 0
        self.__sampleList__ = deque()
        self.__isFull__ = False
        
    def dumpSample(self, sample):
        leftData = sample[0]
        rightData = sample[1]
        
        self.__sumLeft__ += leftData
        self.__sumRight__ += rightData
        self.__sumsqLeft__ += leftData * leftData
        self.__sumsqRight__ += rightData * rightData
        self.__sumLeftRight__ += leftData * rightData
        self.__sampleList__.append(sample)
        self.__samples__ += 1
        
        if not self.__isFull__:
            if len(self.__sampleList__) == self.__window__:
                self.__isFull__ = True
        else:
            eraseDate = self.__sampleList__.popleft()
            leftData = eraseDate[0]
            rightData = eraseDate[1]
            self.__sumLeft__ -= leftData
            self.__sumRight__ -= rightData
            self.__sumsqLeft__ -= leftData * leftData
            self.__sumsqRight__ -= rightData * rightData
            self.__sumLeftRight__ -= leftData * rightData
            self.__samples__ -= 1
        
    def getResult(self):
        
        a = 0.0
        b = 0.0
        
        if not self.__includeConstant__:
            a = self.__sumLeftRight__ / self.__sumsqRight__
            b = 0.0
        else:
            a = (self.__sumLeftRight__ - self.__sumLeft__ * self.__sumRight__ / self.__samples__) / (self.__sumsqRight__ - self.__sumRight__ * self.__sumRight__ / self.__samples__)
            b = (self.__sumLeft__ - a * self.__sumRight__) / self.__samples__
        
        return a, b

import unittest

class TestStatistics(unittest.TestCase):


    def testCorrelationHolder(self):
        
        holder = CorrelationHolder()
        left = xrange(1,50000)
        right = xrange(1,50000)
        
        for i, (x, y) in enumerate(zip(left, right)):
            holder.dumpSample((x,y))
            if i >1:
                self.assertAlmostEqual(1.0, holder.getResult(), 15)
                
    def testMovingAverage(self):
        
        mv = MovingAverage(50)
        
        for i, x in enumerate(xrange(50000)):
            mv.dumpSample(x)
            if i >= 100: 
                self.assertAlmostEqual((2.0*i-49)/2.0, mv.getResult(), 15)
                     
    def testMovingCorrelation(self):
        mv = MovingCorrelation(50)
        left = xrange(1,50000)
        right = xrange(50000,1, -1)
        for i, (x, y) in enumerate(zip(left, right)):
            mv.dumpSample((x,y))
            if i >= 100: 
                self.assertAlmostEqual(-1.0, mv.getResult(), 15)
                    
    def testMovingVariance(self):
        
        mv = MovingVariance(50)
        
        for i, x in enumerate(xrange(50000)):
            mv.dumpSample(1.0)
            if i >= 100: 
                self.assertAlmostEqual(0.0, mv.getResult(), 15)
                
    def testMovingRegression(self):
        
        holder = MovingRegression(50)
        left = xrange(1,50000)
        right = xrange(1,50000)
        
        for i, (x, y) in enumerate(zip(left, right)):
            holder.dumpSample((2.0*x+1.0,y))
            if i >= 100:
                self.assertAlmostEqual((2.0, 1.0), holder.getResult(), 15)
                