# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from ISQLQuery import ISQLQuery
import random

class EasySQLQuery(ISQLQuery):
    
    operators = ['=']
    
    def __init__(self, database, seed):
        super().__init__(database, seed)
        self.easyBuilder()
        
    def getRel(self, numeric=False):
        return super().getRel(numeric)
    
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
    
    def createWhereCond(self, relation):
        return super().createWhereCond(relation)
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()
    
    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns)
        q += ' FROM ' + self.rels['rel1'].name
        if self.conds:
            q += self.formatQueryConds(self.conds)
        return q
    
        
    def easyBuilder(self):
        # Randomly select either an aggregate fn or condition or neither
        aggOrCond = random.choice(['agg', 'cond', ''])
        #aggOrCond='cond'  # for testing

        match aggOrCond:
            # If the random selection is an aggregate fn
            case 'agg':
                self.createAgg()
            
            # If the random selection is a condition
            case 'cond':
                relation = self.getRel(self) # select random relation from database
                self.createCond(relation)
        
            case '':
                relation = self.getRel() # get random relation
                self.createSimple(relation)
                
        self.query = self.toQuery()
    
    

#temp for testing
# from Session import Session     
# d = Session.loadDatabase()
# s = EasySQLQuery(d, 'seed')
# print(s.getSqlQuery())