# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from ISQLQuery import ISQLQuery
import random
import math

class MediumSQLQuery(ISQLQuery):
    
    """
        Initialises the instance variables of the medium query
    """
    def __init__(self, database):
        super().__init__(database)
        self.asNames = [] #names for AS aggregates
        self.mediumBuilder()
        self.query = self.toQuery()
    
    """
        Randomly selects and returns a relation from the loaded database.
        By default does not require relation to contain numeric, string, or roundable attributes.
    """
    def getRel(self, numeric=False, string=False, roundable=False):
        return super().getRel(numeric, string, roundable)
    
    """
        Returns a random aggregate function
    """
    def getAgg(self, numeric=False):
        return super().getAgg(numeric)
    
    """
        Formats attributes and aggregates into a readable string, 
        e.g. "max(customerNumber), customerName"
    """
    def formatQueryAggs(self, attributes, aggregates):
        return super().formatQueryAggs(attributes, aggregates)
    
    """
        Formats conditions and attributes into a readable string.
        e.g. "where customerName = 'Greg'"
    """
    def formatQueryConds(self, conds):
        return super().formatQueryConds(conds)
    
    """
        Create an attribute with neither a condition nor an aggregate function
    """
    def createSimple(self, relation, attribute=None):
        return super().createSimple(relation, attribute)
    
    """
        Chooses an aggregate and a relation that fits that aggregate (i.e. numeric). 
        Aggregate put in aggFns[0]
        Relation put in rels['rel1']
    """   
    def createAgg(self, relation=None, attribute=None, aggFn=None):
        return super().createAgg(relation, attribute, aggFn)
    
    """
        Chooses a condition  (e.g. 'where', 'limit by') and a relation.
        Puts the condition put in conds['cond']
        Relation put in rels['rel1']
    """  
    def createCond(self, relation, astOrAttr=None, condType=None, numeric=False):
        super().createCond(relation, astOrAttr, condType, numeric)
    
    """
        Creates an 'order by' condition.
        Adds an attribute by which to order the output, and either ASC to DESC, to the conds array.
    """  
    def createOrderByCond(self, relation):
        return super().createOrderByCond(relation)
    
    """
        Creates a 'limit' condition.
        Adds a value by which to limit the output to the conds array.
    """  
    def createLimitCond(self, relation):
        return super().createLimitCond(relation)
    
    """
        Creates a 'where' condition.
        Selects an attribute to impose a condition on, an operator to impose, and either NULL or 
        a possible value from the database to compare the attribute to.
    """
    def createWhereCond(self, relation, cond_details, numeric=False, whereAttr=None):
        return super().createWhereCond(relation, cond_details, numeric, whereAttr)
    
    """
        Creates a 'like' condition.
        Selects a string attribute to impose the like on, a comparison string, and inserts wildcard 
        operators into the comparison string.
    """
    def createLikeCond(self, relation, cond_details):
        super().createLikeCond(relation, cond_details)
    
    """
        Insert a percentage wildcard at the given index in value (an array of characters),
        and remove a number of characters with before (startswith True) or after (startswith 
        False) the percentage wildcard.
    """    
    def insertPercentWildCard(self, value, ends_with_perc, num_char_to_remove, cond_details):
        return super().insertPercentWildCard(value, ends_with_perc, num_char_to_remove, cond_details)
    
    """
        Creates a 'round' aggregate function.
        Selects a roundable (float or double) attribute to round, and selects a number of decimals
        to round to.
    """
    def createRoundAgg(self, relation):
        self.aggFns.append('round(')
        attr = relation.getAttribute(roundable=True) # select a random roundable attribute
        self.attrs.append(attr)
        self.roundTo = random.choice([',0',',1',',2']) # select the number of decimals to round to 
    
    """
        Creates the second part of an 'or' condition.
        Creates either a 'like' or 'where' condition to go ofter the keyword or in a query. 
    """
    def createOrCond(self, relation, string=False):
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
    
    
    """
        Sets the query instance variables with values for an easy SQL query. Can create queries
        of type 'aggregate' (i.e. selecting max(), avg(), etc. values), 'conditional' (i.e. doing a 
        limit by, where clause, order by etc.) and a simple type, which just generates a plain select query.
    """
    def easyBuilder(self, relation, attribute = None, aggOrCond=None, aggFn = None, condType = None):
        super().easyBuilder(relation, attribute, aggOrCond, aggFn, condType)
    
    """
        Sets the query instance variables with values for a medium SQL query. Can create queries
        of type 'distinct', 'like' (i.e. doing a string comparison), 'or' (two conditions), and 
        'round', which rounds off a float / double attribute.
    """
    def mediumBuilder(self, relation = None, attribute = None, components = None):
        super().mediumBuilder(relation, attribute, components)
    
    
    """
        Formats instance variable information into a string SQL command and returns it.
    """
    def toQuery(self):
        
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns) # format the attributes and aggregate functions
        q += ' FROM ' + self.rels['rel1'].name
        if self.conds: # formats the condition, if one exists
            q += self.formatQueryConds(self.conds) 
        if self.orCond: # formats the or condition, if one exists
            q += self.formatQueryConds(self.conds['or']) 
        
        return q
    
    """
        Returns the string SQL query.
    """
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    """
        Places instance variable information into a dictionary and returns it. Dictionary is used 
        to create the English queries.
    """
    def getDict(self):
        return super().getDict()