# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from .ISQLQuery import ISQLQuery

class EasySQLQuery(ISQLQuery):
    
    def __init__(self, database, relation=None, attribute=None, aggOrCond = None, aggFn=None):
        """
        Initialises the instance variables of the easy query
        """
        super().__init__(database)
        self.easyBuilder(relation = relation,  attribute=attribute, aggOrCond = aggOrCond, aggFn = aggFn)
        self.query = self.toQuery()
    
    def getRel(self, numeric=False, string=False, roundable=False):
        """
        Randomly selects and returns a relation from the loaded database.
        By default does not require relation to contain numeric, string, or roundable attributes.
        """
        return super().getRel(numeric, string, roundable)
    
    def getAgg(self, numeric=False):
        """
        Returns a random aggregate function
        """
        return super().getAgg(numeric)
    
    def formatQueryAggs(self, attributes, aggregates):
        """
        Formats attributes and aggregates into a readable string, 
        e.g. "max(customerNumber), customerName"
        """
        return super().formatQueryAggs(attributes, aggregates)
    
    def formatQueryConds(self, conds):
        """
        Formats conditions and attributes into a readable string.
        e.g. "where customerName = 'Greg'"
        """
        return super().formatQueryConds(conds)
    
    def createSimple(self, relation, attribute=None):
        """
        Create an attribute with neither a condition nor an aggregate function
        """
        return super().createSimple(relation, attribute)
    
    def createAgg(self, relation=None, attribute=None, aggFn=None):
        """
        Chooses an aggregate and a relation that fits that aggregate (i.e. numeric). 
        Aggregate put in aggFns[0]
        Relation put in rels['rel1']
        """
        return super().createAgg(relation, attribute, aggFn)
    
    def createCond(self, relation, astOrAttr=None, condType=None, numeric=False):
        """
        Chooses a condition  (e.g. 'where', 'limit by') and a relation.
        Puts the condition put in conds['cond']
        Relation put in rels['rel1']
        """  
        super().createCond(relation, astOrAttr, condType, numeric)
    
    def createOrderByCond(self, relation):
        """
        Creates an 'order by' condition.
        Adds an attribute by which to order the output, and either ASC to DESC, to the conds array.
        """  
        return super().createOrderByCond(relation)
    
    def createLimitCond(self, relation):
        """
        Creates a 'limit' condition.
        Adds a value by which to limit the output to the conds array.
        """  
        return super().createLimitCond(relation)
    
    def createWhereCond(self, relation, cond_details, numeric=False, whereAttr=None):
        """
        Creates a 'where' condition.
        Selects an attribute to impose a condition on, an operator to impose, and either NULL or 
        a possible value from the database to compare the attribute to.
        """
        return super().createWhereCond(relation, cond_details, numeric, whereAttr)
    
    def createLikeCond(self, relation, cond_details):
        """
        Creates a 'like' condition.
        Selects a string attribute to impose the like on, a comparison string, and inserts wildcard 
        operators into the comparison string.
        """
        super().createLikeCond(relation, cond_details)
    
    def insertPercentWildCard(self, value, ends_with_perc, num_char_to_remove, cond_details):
        """
        Insert a percentage wildcard at the given index in value (an array of characters),
        and remove a number of characters with before (startswith True) or after (startswith 
        False) the percentage wildcard.
        """
        super().insertPercentWildCard(self, value, ends_with_perc, num_char_to_remove, cond_details)
    
    def easyBuilder(self, relation, attribute = None, aggOrCond=None, aggFn = None, condType = None):
        """
        Sets the query instance variables with values for an easy SQL query. Can create queries
        of type 'aggregate' (i.e. selecting max(), avg(), etc. values), 'conditional' (i.e. doing a 
        limit by, where clause, order by etc.) and a simple type, which just generates a plain select query.
        """
        super().easyBuilder(relation, attribute, aggOrCond, aggFn, condType)
    
    def mediumBuilder(self, relation = None, attribute = None, components = None):
        """
        Sets the query instance variables with values for a medium SQL query. Can create queries
        of type 'distinct', 'like' (i.e. doing a string comparison), 'or' (two conditions), and 
        'round', which rounds off a float / double attribute.
        """
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
        return q
    
    def getSqlQuery(self):
        """
        Returns the string SQL query.
        """
        return super().getSqlQuery()
    
    def getDict(self):
        """
        Places instance variable information into a dictionary and returns it. Dictionary is used 
        to create the English queries.
        """
        return super().getDict()
    