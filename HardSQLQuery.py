# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from EasySQLQuery import EasySQLQuery
from ISQLQuery import ISQLQuery
import random

class HardSQLQuery(ISQLQuery):
        
    def __init__(self, database, seed):
        super().__init__(database, seed)
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
    
    def createAgg(self, relation=None, attribute=None, aggFn=None):
        return super().createAgg(relation, attribute, aggFn)
    
    def createCond(self, relation, astOrAttr=None, condType=None, numeric=False):
        super().createCond(relation, astOrAttr, condType, numeric)
    
    def createSimple(self, relation):
        return super().createSimple(relation)
    
    def createOrderByCond(self, relation):
        return super().createOrderByCond(relation)
    
    def createLimitCond(self, relation):
        return super().createLimitCond(relation)
    
    def createWhereCond(self, relation, cond_details, numeric=False):
        return super().createWhereCond(relation, cond_details, numeric)
    
    def createLikeCond(self, relation, cond_details):
        super().createLikeCond(relation, cond_details)
        
    def insertPercentWildCard(self, value, ends_with_perc, num_char_to_remove, cond_details):
        super().insertPercentWildCard(value, ends_with_perc, num_char_to_remove, cond_details)
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()
    
    def easyBuilder(self, relation, attribute = None, aggOrCond=None):
        super().easyBuilder(relation, attribute, aggOrCond)
        
    def mediumBuilder(self, relation = None, attribute = None, components = None):
        super().mediumBuilder(relation, attribute, components)
    
    def hardBuilder(self):
        
        type = 'nested'
        
        match type:
            
            case 'nested':
                sqlQuery1 = EasySQLQuery(self.db, 'seed', aggOrCond = 'whereCond')
                # ensure not doing a null comparison
                while sqlQuery1.conds['operator'] not in ISQLQuery.operators:
                    sqlQuery1 = EasySQLQuery(self.db, 'seed', aggOrCond = 'whereCond')
                
                sqlQuery1.rels['rel1']=sqlQuery1.rels['rel1']
            
                sqlQuery2 = self.createNestedQuery(sqlQuery1.rels['rel1'], sqlQuery1.conds['val1'], sqlQuery1.conds['operator'])
                
                
                
                sqlQuery1.conds['val2']=sqlQuery2
                sqlQuery1.nested = True
                
                self.query =  sqlQuery1.toQuery()

            
    
    def createNestedQuery(self, relation, attribute, operator):

        match operator:
            case '=':
                if attribute.numeric:
                    aggFn=random.choice(['max(', 'min(', 'avg('])
            case _:
                aggFn = 'avg('
        
        nestedQuery = EasySQLQuery(self.db, 'seed', relation = relation, attribute = attribute, aggFn = aggFn)

        return nestedQuery
        
                
    
    def toQuery(self):
        q = '(SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns)
        q += ' FROM ' + self.rels['rel1'].name
        if self.conds:
            q += self.formatQueryConds(self.conds)
        if self.orCond:
            q += self.formatQueryConds(self.conds['or'])
        q += ')'
        return q
    
    
    # #temp for testing
# from Session import Session     
# d = Session.loadDatabase()
# s = HardSQLQuery(d, 'seed')
# print(s.getSqlQuery())
