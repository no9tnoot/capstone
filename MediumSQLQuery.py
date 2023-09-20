# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from ISQLQuery import ISQLQuery
import random
import math

class MediumSQLQuery(ISQLQuery):
    
    
    def __init__(self, database):
        super().__init__(database)
        self.asNames = [] #names for AS aggregates
        self.mediumBuilder()
        self.query = self.toQuery()
        
    def getRel(self, numeric=False, string=False, roundable=False):
        return super().getRel(numeric, string, roundable)
    
    def selectAttrVal(self, relation, attribute):
        return super().selectAttrVal(relation, attribute)
    
    def getAgg(self, numeric=False):
        return super().getAgg(numeric)
    
    def formatQueryAggs(self, attributes, aggregates):
        return super().formatQueryAggs(attributes, aggregates)
    
    def formatQueryConds(self, conds):
        return super().formatQueryConds(conds)
    
    def createAgg(self, relation=None, attribute=None, aggFn=None):
        return super().createAgg(relation, attribute, aggFn)
    
    def createCond(self, relation, astOrAttr=None, condType=None, numeric=False):
        super().createCond(relation, astOrAttr, condType, numeric)
    
    def createSimple(self, relation, attribute=None):
        return super().createSimple(relation, attribute)
    
    def createOrderByCond(self, relation):
        return super().createOrderByCond(relation)
    
    def createLimitCond(self, relation):
        return super().createLimitCond(relation)
    
    def createWhereCond(self, relation, cond_details, numeric=False, whereAttr=None):
        return super().createWhereCond(relation, cond_details, numeric, whereAttr)
    
    def createLikeCond(self, relation, cond_details):
        super().createLikeCond(relation, cond_details)
        
    def insertPercentWildCard(self, value, ends_with_perc, num_char_to_remove, cond_details):
        return super().insertPercentWildCard(value, ends_with_perc, num_char_to_remove, cond_details)
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()
    
    def easyBuilder(self, relation, attribute=None, aggOrCond=None, aggFn=None, condType = None):
        return super().easyBuilder(relation, attribute, aggOrCond, aggFn, condType)
        
    def mediumBuilder(self, components=None):
        super().mediumBuilder(components)
        
    
    def createRoundAgg(self, relation):
        self.aggFns.append('round(')
        attr = relation.getAttribute(roundable=True)
        self.attrs.append(attr)
        self.roundTo = random.choice([',0',',1',',2'])
    
    
    def createOrCond(self, relation, string=False):
        self.orCond=True
        self.conds['or']={}
        like = random.choice([True, False])
        if string and like:
            self.createLikeCond(relation, self.conds['or'])
            while self.conds['val2']==self.conds['or']['val2']:
                self.createLikeCond(relation, self.conds['or'])
        else:
            self.createWhereCond(relation, self.conds['or'])
            while self.conds['val2']==self.conds['or']['val2']:
                self.createWhereCond(relation, self.conds['or'])
        self.conds['or']['cond']='or'
        
        
    
    
    

    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns)
        q += ' FROM ' + self.rels['rel1'].name
        if self.conds:
            q += self.formatQueryConds(self.conds)
        if self.orCond:
            q += self.formatQueryConds(self.conds['or'])
        return q
    


# #temp for testing
# from Session import Session     
# d = Session.loadDatabase()
# s = MediumSQLQuery(d)
# print(s.getSqlQuery())