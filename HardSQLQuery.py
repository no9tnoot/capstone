# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from EasyEnglishQuery import EasyEnglishQuery
from EasySQLQuery import EasySQLQuery
import ISQLQuery
import random

from QuestionFactory import QuestionFactory

class HardSQLQuery(ISQLQuery):
        
    def __init__(self, database, seed):
        super().__init__(database, seed)
        self.asNames = [] #names for AS aggregates
        self.hardBuilder()
        
    def getRel(self, numeric=False, string=False):
        return super().getRel(numeric, string)
    
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
    
    def createSimple(self, relation):
        return super().createSimple(relation)
    
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
    
    def easyBuilder(self, relation):
        return super().easyBuilder(relation)
    
    def hardBuilder(self):
        
        type = 'nested'
        
        match type:
            
            case 'nested':
                sqlQuery1 = EasySQLQuery(self.database, 'seed')
                sqlQuery2 = EasySQLQuery(self.database, 'seed', relation = sqlQuery1.rels['rel1'])
                
        
    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns, self.asNames)
        q += 'FROM' + self.queryRels(self.rels[0], self.rels[1], self.rels[2])
        q += self.formatQueryConds(self.conds)
        return q