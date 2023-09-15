# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from ISQLQuery import ISQLQuery
import random

class EasySQLQuery(ISQLQuery):
    
    operators = ['=']
    
    def __init__(self, database, seed, relation = None):
        super().__init__(database, seed)
        if relation is None:
            relation = self.getRel() # select random relation from database
        self.easyBuilder(relation)
        
    def getRel(self, numeric=False, string=False, roundable=False):
        return super().getRel(numeric, string, roundable)
    
    def selectAttrVal(self, relation, attribute):
        return super().selectAttrVal(relation, attribute)
    
    def setAgg(self):
        return super().setAgg()
    
    def formatQueryAggs(self, attributes, aggregates):
        return super().formatQueryAggs(attributes, aggregates)
    
    def formatQueryConds(self, conds):
        return super().formatQueryConds(conds)
    
    def createAgg(self):
        return super().createAgg()
    
    def createCond(self, relation):
        return super().createCond(relation)
    
    def createOrderByCond(self, relation):
        return super().createOrderByCond(relation)
    
    def createLimitCond(self, relation):
        return super().createLimitCond(relation)
    
    def createWhereCond(self, relation, cond_details):
        return super().createWhereCond(relation, cond_details)
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()
    
    def createSimple(self, relation):
        return super().createSimple(relation)
    
    def easyBuilder(self, relation):
        super().easyBuilder(relation)
    
    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns)
        q += ' FROM ' + self.rels['rel1'].name
        if self.conds:
            q += self.formatQueryConds(self.conds)
        return q
    
        
    
    
    

#temp for testing
# from Session import Session     
# d = Session.loadDatabase()
# s = EasySQLQuery(d, 'seed')
# print(s.getSqlQuery())