# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from .ISQLQuery import ISQLQuery
import random

class MediumSQLQuery(ISQLQuery):
    """
    Medium mySQL Query object and constructor. Implements the ISQLQuery interface. Generates a
    medium query on initialisation and stores the string, runnable query in the 'query' instance
    variable.
    """
    
    def __init__(self, database):
        """
        Sets the instance variables of the medium query, and creates the string query.
        """
        super().__init__(database)
        self.mediumBuilder()
        self.query = self.toQuery()
    
    def getRel(self, numeric=False, string=False, roundable=False):
        return super().getRel(numeric, string, roundable)
    
    def getAgg(self, numeric=False):
        return super().getAgg(numeric)
    
    def formatQueryAggs(self, attributes, aggregates):
        return super().formatQueryAggs(attributes, aggregates)
    
    def formatQueryConds(self, conds):
        return super().formatQueryConds(conds)
    
    def createSimple(self, relation, attribute=None):
        return super().createSimple(relation, attribute)
    
    def createAgg(self, relation=None, attribute=None, aggFn=None):  
        return super().createAgg(relation, attribute, aggFn)
    
    def createCond(self, relation, astOrAttr=None, condType=None, numeric=False):
        super().createCond(relation, astOrAttr, condType, numeric)
    
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
    
    def createRoundAgg(self, relation):
        """
        Creates a 'round' aggregate function.
        Selects a roundable (float or double) attribute to round, and selects a number of decimals
        to round to.
        """
        self.aggFns.append('round(')
        attr = relation.getAttribute(roundable=True) # select a random roundable attribute
        self.attrs.append(attr)
        self.roundTo = random.choice([',0',',1',',2']) # select the number of decimals to round to 
    
    def createOrCond(self, relation, string=False):
        """
        Creates the second part of an 'or' condition.
        Creates either a 'like' or 'where' condition to go ofter the keyword or in a query. 
        """
        self.orCond=True
        self.conds['or']={}
        
        like = random.choice([True, False]) # decide whether to do a like condition or a where condition
        if string and like:
            self.createLikeCond(relation, self.conds['or'])
            while self.conds['val2']==self.conds['or']['val2']: # make sure the two conditions are not the same
                self.createLikeCond(relation, self.conds['or'])
        else:
            self.createWhereCond(relation, self.conds['or'])
            while self.conds['val2']==self.conds['or']['val2']: # make sure the two conditions are not the same
                self.createWhereCond(relation, self.conds['or'])
        
        self.conds['or']['cond']='or'
    
    
    def easyBuilder(self, relation, attribute = None, aggOrCond=None, aggFn = None, condType = None):
        super().easyBuilder(relation, attribute, aggOrCond, aggFn, condType)
    
    def mediumBuilder(self, relation = None, attribute = None, components = None):
        super().mediumBuilder(relation, attribute, components)
    
    
    def toQuery(self):
        """
        Formats instance variable information into a string SQL command and returns it.
        """
        
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns) # format the attributes and aggregate functions
        q += ' FROM ' + self.rels['rel1'].name
        if self.conds: # formats the condition, if one exists
            q += self.formatQueryConds(self.conds) 
        if self.orCond: # formats the or condition, if one exists
            q += self.formatQueryConds(self.conds['or']) 
        
        return q
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()