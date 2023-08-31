# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from abc import ABC, abstractmethod
import mysql.connector
import random
import Database

class ISQLQuery(ABC):
    
    @abstractmethod
    def __init__(self, database, seed):
        self.opperators = ['=', '<', '>', '<=', '>=', 'is', 'is not']
        self.aggregateFunctions = ['count(', 'max(', 'min(', 'avg(', '']
        self.condition = ['where', 'limit', 'order by', '']
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

        #names for AS aggregates
        self.asNames = []
    
    # Randomly selects a relation from the loaded database
    @abstractmethod
    def setRel(self, attTypeNeeded, aggOrCondType):

        # select relation
        relation = random.randrange(0, self.db.numRelations()-1, 1)
        relation = self.db.getRelation(relation)

        # if the chosen relation contains numeric attributes, return it
        # if the chosen action is a condition, a count, or nothing, just return the relation
        if relation.numNumeric() or attTypeNeeded == 'cond' or aggOrCondType == 'count(' or aggOrCondType == '':
            return relation

        # if the chosen relation is not appropriate, select a new relation
        else:
            relation = self.setRel(attTypeNeeded, aggOrCondType)
            return relation

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
        
        return cursor.fetchall()       # return the 

    """
        Returns a random aggregate function
    """
    @abstractmethod
    def setAgg(self):
        aggType = random.choice(self.aggregateFunctions) # select the type of aggregate function
        return aggType # add chosen aggregate function to array instance variable
    
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
    
    # relation/s to query form. including joins
    @abstractmethod
    def queryRels(rel1, rel2, join):
        if rel2 == '':
            return rel1
        else:
            return rel1 + join + rel2

    #conditions to query form. will add a few extra spaces in some cases but shouldn't matter too much 
    # still need to implement AND/OR for extra conditions   
    def queryConds(conds):
        cond = conds[0] + ' ' + conds[1] + ' ' + conds[2] + ' ' + conds[3]
        return cond
    
    @abstractmethod
    def toQuery(self):
        q = 'SELECT '
        q += Question.queryAggs(self.attrs, self.aggFns, self.asNames)
        q += 'FROM' + Question.queryRels(self.rels[0], self.rels[1], self.rels[2])
        q += Question.queryConds(self.conds)
        return q
