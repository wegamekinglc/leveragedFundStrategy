# -*- coding: utf-8 -*-
'''
Created on 2014年12月3日

@author: cheng.li
'''
from Accounts import StockAccout, Transaction
from collections import OrderedDict

class AccountManager:
    
    def __init__(self):
        
        self.__accounts__ = OrderedDict()
        
    def isExist(self, codeName):
        '''
        返回账户管理中是否有某只具体证券
        '''
        codeName = codeName.upper()
        return self.__accounts__.has_key(codeName)
    
    def fetch(self, codeName):
        '''
        返回账户管理中所有某只证券的所有存账
        '''
        
        if self.isExist(codeName):
            return self.__accounts__[codeName.upper()]
        else:
            return OrderedDict()
    
    def insertTrade(self, date, trans):
        '''
        按照日期插入一笔具体的交易
        '''
        
        newTrade = StockAccout(trans.__codeName__)
        newTrade.accountChange(trans)
        
        if self.isExist(newTrade.codeName()):
            existingTrades = self.__accounts__[newTrade.codeName()]
            if existingTrades.has_key(date):
                existingTrades[date].accountChange(trans)
            else:
                existingTrades[date] = newTrade
        else:
            self.__accounts__[newTrade.codeName()] = OrderedDict()
            self.__accounts__[newTrade.codeName()][date] = newTrade
    
    def cleanExistTrade(self, date, codeName):
        '''
        清除已经存在的某个证券在某天的交易
        '''
        
        rtnAccount = StockAccout(codeName)
        if self.__accounts__.has_key(codeName) and self.__accounts__[codeName].has_key(date):
            rtnAccount = self.__accounts__[codeName][date]
            self.__accounts__[codeName].pop(date)
            if len(self.__accounts__[codeName]) == 0:
                self.__accounts__.pop(codeName)
                
        return rtnAccount
    
    def clearOnAccount(self, tradeDate, codeName, tradingVolume):
        '''
        交易某只证券
        '''
        
        if not self.__accounts__.has_key(codeName):
            return 0
        
        remainingVolume = tradingVolume
        tradedVolume = 0
        
        for trade in self.__accounts__[codeName].items():
            date = trade[0]
            account = trade[1]
            
            availableVolume = account.volume()
            if remainingVolume <> 0 and date <= tradeDate and (availableVolume * remainingVolume) < 0:
                if abs(availableVolume) <= abs(remainingVolume):
                    remainingVolume += availableVolume
                    tradedVolume -= availableVolume
                    self.__accounts__[codeName].pop(date)
                else:
                    tradedVolume += remainingVolume
                    trans = Transaction(codeName, remainingVolume, self.__accounts__[codeName][date].averageCost())
                    self.__accounts__[codeName][date].accountChange(trans)
                    remainingVolume = 0
                    break
                
        if len(self.__accounts__[codeName]) == 0:
            self.__accounts__.pop(codeName)
        return tradedVolume
    
    def __repr__(self):
        
        return repr(self.__dict__)

# 单元测试部分
   
import unittest
from CAL.DateUtilities.Dates import Date

class TestAccountManager(unittest.TestCase):

    def testAccountManager(self):
        
        accountManager = AccountManager()
        
        trans = Transaction('000001', 100, 25.0)
        tradeDate = Date(2014, 11, 23)
        accountManager.insertTrade(tradeDate, trans)
        self.assertEqual('000001,100,25.0', str(accountManager.fetch('000001')[tradeDate])) 
        
        trans = Transaction('000001', 40, 15.0)
        tradeDate = Date(2014, 11, 24)
        accountManager.insertTrade(tradeDate, trans)
        self.assertEqual('000001,40,15.0', str(accountManager.fetch('000001')[tradeDate])) 
        
        trans = Transaction('000001', 150, 15.0)
        tradeDate = Date(2014, 11, 23)
        accountManager.insertTrade(tradeDate, trans)
        self.assertEqual('000001,250,19.0', str(accountManager.fetch('000001')[tradeDate])) 
        
        trans = Transaction('000001', 120, 12.0)
        tradeDate = Date(2014, 11, 25)
        accountManager.insertTrade(tradeDate, trans)
        self.assertEqual('000001,120,12.0', str(accountManager.fetch('000001')[tradeDate])) 
        
        tradeDate = Date(2014, 11, 25)
        rtn = accountManager.cleanExistTrade(tradeDate, '000001')
        self.assertEqual('000001,120,12.0', str(rtn)) 
        
        tradeDate = Date(2014, 11, 26)
        tradedVolume = accountManager.clearOnAccount(tradeDate, '000001', -20)
        self.assertEqual(-20, tradedVolume)
        self.assertEqual('000001,40,15.0', str(accountManager.fetch('000001')[Date(2014, 11, 24)]))
        self.assertEqual('000001,230,19.0', str(accountManager.fetch('000001')[Date(2014, 11, 23)]))
        
        tradedVolume = accountManager.clearOnAccount(tradeDate, '000001', -240)
        self.assertEqual(-240, tradedVolume)
        self.assertEqual('000001,30,15.0', str(accountManager.fetch('000001')[Date(2014, 11, 24)]))