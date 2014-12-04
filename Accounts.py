# -*- coding: utf-8 -*-
'''
Created on 2014年12月3日

@author: cheng.li
'''

class Transaction:  
    '''
    表示一笔完成的交易
    '''
    
    def __init__(self, codeName, amount, price):
        '''
        :param str codeName: 证券代码
        :param int amount: 数量
        :param float price: 成交价
        '''
        
        self.__codeName__ = codeName.upper()
        self.__amount__ = amount
        self.__price__ = price
        
    def __str__(self):
        
        return self.__codeName__ + ',' + str(self.__amount__) + ',' + str(self.__price__)
    
    def __repr__(self):
        
        return repr(self.__dict__)

class StockAccout:
    '''
    一只具体证券的账户管理(股票）
    '''
    
    def __init__(self, codeName):
        '''
        :param str codeName: 证券代码
        '''
        
        self.__codeName__ = codeName.upper()
        self.__volume__ = 0
        self.__averageCost__ = 0.0
        
    def volume(self):
        '''
        返回证券的数量
        '''
        return self.__volume__
    
    def clear(self):
        '''
        清空账户
        '''
        self.__volume__ = 0
        self.__averageCost__ = 0.0
        
    def totalCost(self):
        '''
        返回账户内证券总成本
        '''
        
        return self.__volume__ * self.__averageCost__
    
    def averageCost(self):
        '''
        返回账户内债券平均成本
        '''
        
        return self.__averageCost__
    
    def codeName(self):
        '''
        返回证券代码
        '''
        
        return self.__codeName__
        
        
    def accountChange(self, trans):
        '''
        根据交易记录调整账户
        '''
        
        if trans.__codeName__ <> self.__codeName__:
            raise Exception(u'该交易记录与账户证券名称不符合！')
        
        previousTotalCost = self.__volume__ * self.__averageCost__
        self.__volume__ += trans.__amount__
        totalCost = previousTotalCost + trans.__amount__ * trans.__price__
        
        self.__averageCost__ = self.__volume__ <> 0 and (totalCost / self.__volume__) or 0.0
        
    def __str__(self):
        
        return self.codeName() + ',' + str(self.volume()) + ',' + str(self.averageCost())
    
    
    def __repr__(self):
        
        return repr(self.__dict__)
    
# 单元测试部分
    
import unittest 
    
class TestAccount(unittest.TestCase):
    
    def testTransaction(self):
        trans = Transaction('000001', 100, 25.0)
        
        self.assertEqual(trans.__codeName__, '000001')
        self.assertEqual(trans.__amount__, 100)
        self.assertAlmostEqual(trans.__price__, 25.0, 15)
        self.assertEqual('000001,100,25.0', str(trans))
    
    def testStockAccount(self):
        account = StockAccout('000001')
        self.assertEqual('000001', account.codeName())
        
        trans = Transaction('000001', 100, 25.0)
        account.accountChange(trans)
        self.assertEqual(trans.__amount__, account.volume())
        self.assertAlmostEqual(trans.__price__, account.averageCost(), 16)
        self.assertAlmostEqual(trans.__price__*trans.__amount__, account.totalCost(), 16)
        
        trans = Transaction('000001', -50, 15.0)
        account.accountChange(trans)
        self.assertEqual(50, account.volume())
        self.assertAlmostEqual(35.0, account.averageCost(), 16)
        self.assertAlmostEqual(50 * 35.0, account.totalCost(), 16)
        self.assertEqual('000001,50,35.0', str(account))