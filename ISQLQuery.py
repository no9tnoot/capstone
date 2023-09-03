# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from abc import ABC, abstractmethod
import mysql.connector
import random
import Database

class ISQLQuery(ABC):
    
    operators = ['=', '<', '>', '<=', '>=']
    nullOperators = ['is', 'is not']
    aggregateFunctions = ['count(', 'max(', 'min(', 'avg(', 'sum(']
    condition = ['where', 'limit', 'order by']
    
    @abstractmethod
    def __init__(self, database, seed):
        self.db = database
        self.seed = seed
        self.queryString = ""
        self.queryArray = []
        
         # Ordered list of aggregate functions used in the query
        self.aggFns = []

        # Ordered list of conditions used in the query
        self.conds = []

        # Ordered list of attributes used in the query
        self.attrs = []

        # Ordered list of relations used in the query
        self.rels = []

        
    
    # Randomly selects a relation from the loaded database
    # by default does not require relation to contain numeric attributes    @abstractmethod
    def setRel(self, numeric = False):

        # select relation
        relation = random.randrange(0, self.db.numRelations()-1, 1)
        relation = self.db.getRelation(relation)
        if not numeric:
            return relation
        else:
            if relation.numNumeric():
                return relation
            else:
                return self.setRel(True)


    ''' For questions where 2+ attributes are chosen from one relation, must include logic to prevent the
        attribute being selected twice'''
    
    
    # Randomly selects an attribute from the chosen relation
    @abstractmethod
    def setAttr(self, relation, attTypeNeeded, aggOrCondType, attNum):

        # if condition or count, include * as an option
        '''decided to include * in this way as it will allow it to appear with reasonable frequency'''
        if attTypeNeeded == 'cond' or aggOrCondType == 'count(' or aggOrCondType == '':

            # Randomly select attribute from relation -> doesn't have to be numeric
            attribute = random.randrange(0, relation.getNumAttributes()-1, 1)
            attribute = relation.getAttribute(attribute)
            
            # Choose between attribute and '*' if attNum is 1
            # (Ensures that 2nd attribute is never * -> select x where y='*' doesn't make sense)
            if attNum == 1:
                astOrAttr = random.choice(['*', 'attribute'])
                if astOrAttr == '*':
                    attribute = Database.Attribute('*', 'varchar(50)' , 'NO', '')
        
        else: # * should not be an option
            attribute = random.randrange(0, len(relation.numericAttributes)-1, 1)
            attribute = relation.numericAttributes[attribute]
        
        return attribute
    
    """
        Selects a possible value from an attribute.
    """
    @abstractmethod
    def selectAttrVal(self, relation, attribute):

        # Connect to database
        database = mysql.connector.connect(
            host=self.db.host,
            user=self.db.user,
            password=self.db.pword,
            database=self.db.db_name
        )
        
        cursor = database.cursor()  # Create a cursor to interact with the database
        
        reqVal = random.randrange(0, relation.getNumRows()-1, 1) #Select a random value between 0 and the total number of values -1

        cursor.execute("SELECT " + attribute.name + " FROM " + relation.name + "limit 1 offset " + reqVal + ";")   # SQL: print the table names
        
        return cursor.fetchall()[0]       # return the 

    """
        Returns a random aggregate function
    """
    @abstractmethod
    def setAgg(self):
        aggType = random.choice(self.aggregateFunctions) # select the type of aggregate function
        return aggType # add chosen aggregate function to array instance variable
    
    """
        Formats attributes and aggregates into a readable string, 
        e.g. "max(customerNumber), customerName"
    """
    @abstractmethod
    def queryAggs(attributes, aggregates, asNames = ['']):
        aggs = ''
        if aggregates[0] != '':
            aggs += aggregates[0] + attributes[0] + ')' + asNames[0]
        else:
            aggs += attributes[0]
        
        #if we have more than one attribute/aggregate
        if len(attributes) > 1:
            for x in range(1,len(attributes)-1):
                if aggregates[x] != '':
                    aggs += ', ' + aggregates[x] + attributes[x] + ')' + asNames[x]
                else:
                    aggs += ', ' + attributes[x]
        return aggs
    
    

    #conditions to query form. will add a few extra spaces in some cases but shouldn't matter too much 
    # still need to implement AND/OR for extra conditions  
    @abstractmethod 
    def queryConds(conds):
        cond = conds[0] + ' ' + conds[1] + ' ' + conds[2] + ' ' + conds[3]
        return cond
    
    """
        relation/s to query form. including joins
    """
    @abstractmethod 
    def queryRels(rel1, rel2, join):
        if rel2 == '':
            return rel1
        else:
            return rel1 + join + rel2
    
    #conditions to query form. will add a few extra spaces in some cases but shouldn't matter too much 
    # still need to implement AND/OR for extra conditions   
    @abstractmethod
    def queryConds(conds):
        cond = conds[0] + ' ' + conds[1] + ' ' + conds[2] + ' ' + conds[3]
        return cond

    @abstractmethod
    def toQuery(self):
        q = 'SELECT '
        q += self.queryAggs(self.attrs, self.aggFns, self.asNames)
        q += 'FROM' + self.queryRels(self.rels[0], self.rels[1], self.rels[2])
        q += self.queryConds(self.conds)
        return q
    
