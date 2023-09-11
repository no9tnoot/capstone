# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from ISQLQuery import ISQLQuery
import random

class EasySQLQuery(ISQLQuery):
    
    def __init__(self, database, seed):
        super().__init__(database, seed)
        self.easyBuilder()
        
    def getRel(self, numeric=False):
        return super().getRel(numeric)
    
    def getAttr(self, relation, numeric=False):
        return super().getAttr(relation, numeric)
    
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
    
    def createCond(self):
        return super().createCond()
    
    def createOrderByCond(self, relation):
        return super().createOrderByCond(relation)
    
    def createLimitCond(self, relation):
        return super().createLimitCond(relation)
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()
    
    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns)
        q += ' FROM ' + self.rels[0].name
        q += self.formatQueryConds(self.conds)
        return q
    
        
    def easyBuilder(self):
        # Randomly select either an aggregate fn or condition or neither
        aggOrCond = random.choice(['agg', 'cond', ''])

        match aggOrCond:
            # If the random selection is an aggregate fn
            case 'agg':
                self.createAgg()
            
            # If the random selection is a condition
            case 'cond':
                self.createCond()
        
            case '':
                self.createSimple()
                
        self.query = self.toQuery()
    
    
    # If this is a "where" condition
    def createWhereCond(self, relation):
        
        attr = self.getAttr(relation) # select a second random attribute 
        # (can be the same as attr_1)
        self.conds['val1'] = attr # add chosen attribute to conds array

        nullOrVal = random.choice(['null', 'val']) # Choose between ensuring the attribute value 
        # is not null and ensuring it has a given value
        # If null option chosen and attribute contains null values
        if nullOrVal == 'null' and self.conds['val1'].null == 'YES':
            operator = random.choice(self.nullOperators)
            self.conds['operator'] = operator
            self.conds['val2'] = 'NULL'
        #If value option chosen or attribute does not contain any nulls
        else:
            operator = random.choice(self.operators)
            self.conds['operator'] = operator
            # Select a required value for the attribute
            reqVal = self.selectAttrVal(relation, self.conds['val1'])
            self.conds['val2'] = str(reqVal) # add chosen required value to array instance variable

#temp for testing
# from Session import Session     
# d = Session.loadDatabase()
# s = EasySQLQuery(d, 'seed')
# print(s.getSqlQuery())