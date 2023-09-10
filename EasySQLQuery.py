# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from ISQLQuery import ISQLQuery
import random
from Session import Session #temp for testing

class EasySQLQuery(ISQLQuery):
    
    def __init__(self, database, seed):
        super().__init__(database, seed)
        
    def getRel(self, numeric=False):
        return super().getRel(numeric)
    
    def getAttr(self, relation, attTypeNeeded, aggOrCondType, attNum):
        return super().getAttr(relation, attTypeNeeded, aggOrCondType, attNum)
    
    def selectAttrVal(self, relation, attribute):
        return super().selectAttrVal(relation, attribute)
    
    def setAgg(self):
        return super().setAgg()
    
    def formatQueryAggs(attributes, aggregates):
        return super().formatQueryAggs(attributes, aggregates)
    
    def formatQueryConds(conds):
        return super().formatQueryConds()
    
    def createAgg(self):
        return super().createAgg()
    
    def createCond(self):
        return super().createCond()
    
    def createOrderByCond(self, relation):
        return super().createOrderByCond(relation)
    
    def createLimitCond(self, relation):
        return super().createLimitCond(relation)
    
    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns)
        q += 'FROM' + self.rels[0]
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
                

        self.rels += ['','']
        self.query = self.toQuery()
    
    
    # If this is a "where" condition
    def createWhereCond(self, relation):
        
        attr = self.setAttr(relation) # select a second random attribute 
        # (can be the same as attr_1)
        self.conds.append(attr.name) # add chosen attribute to conds array

        nullOrVal = random.choice(['null', 'val']) # Choose between ensuring the attribute value 
        # is not null and ensuring it has a given value
        # If null option chosen and attribute contains null values
        if nullOrVal == 'null' and self.conds[1].null == 'YES':
            operator = random.choice(self.nullOperators)
            self.conds.append(operator)
            self.conds.append('NULL')
        #If value option chosen or attribute does not contain any nulls
        else:
            operator = random.choice(self.operators)
            self.conds.append(operator)
            # Select a required value for the attribute
            reqVal = self.selectAttrVal(relation, self.conds[1])
            self.conds.append(str(reqVal)) # add chosen required value to array instance variable
    
d = Session.loadDatabase()
s = EasySQLQuery(d, 'seed')
print(s.toQuery())