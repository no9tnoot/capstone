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
    wildcard = ['%','_', ]
    
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
    def getRel(self, numeric = False):

        # select relation
        relation = random.randrange(0, self.db.numRelations()-1, 1)
        relation = self.db.getRelation(relation)
        if not numeric:
            return relation
        else:
            if relation.numNumeric():
                return relation
            else:
                return self.getRel(True)


    ''' For questions where 2+ attributes are chosen from one relation, must include logic to prevent the
        attribute being selected twice'''

    # Randomly selects an attribute from the chosen relation
    def getAttr(self, relation, numeric = False):

        if not numeric:
            # Randomly select attribute from relation -> doesn't have to be numeric
            i = random.randrange(0, relation.getNumAttributes()-1, 1)
            attribute = relation.getAttribute(i)
        
        else: # * should not be an option
            i = random.randrange(0, relation.numNumeric(), 1)
            attribute = relation.getAttribute(i, True)
        
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
    def formatQueryAggs(self, attributes, aggregates):
        aggs = ''
        if aggregates:
            aggs += aggregates[0] + attributes[0] + ')'
        else:
            aggs += attributes[0]
        
        #if we have more than one attribute/aggregate
        if len(attributes) > 1:
            for x in range(1,len(attributes)-1):
                if aggregates[x] != '':
                    aggs += ', ' + aggregates[x] + attributes[x] + ')'
                else:
                    aggs += ', ' + attributes[x]
        return aggs
    
    
    #conditions to query form. will add a few extra spaces in some cases but shouldn't matter too much 
    # still need to implement AND/OR for extra conditions   
    @abstractmethod
    def formatQueryConds(conds):
        cond = conds[0] + ' ' + conds[1] + ' ' + conds[2] + ' ' + conds[3]
        return cond
    
    """
        Create an attribute with neither a condition nor an aggregate function
    """
    def createSimple(self):
        relation = self.getRel() # get random relation
        self.rels.append(relation)
        
        numAttr = random.choice(1,2)  # will we ask for one or 2 relations
        self.attrs.append(self.getAttr(relation))
        
        # select and set the second relation if one is needed
        while numAttr==2:
            attr2 = self.getAttr(relation)
            if (attr2 != self.attrs[0]): # don't set the same relation as the first one
                self.attrs.append(attr2)
                numAttr = 0
    
    
        
    """
        Chooses an aggregate and a relation that fits that aggregate (i.e. numeric). 
        Aggregate put in aggFns[0]
        Relation put in rels[0]
    """    
    @abstractmethod
    def createAgg(self):
        self.aggFns.append(self.setAgg())  # get a random aggreegate func and storing it in aggFns
        
        # If doing a count agg, account for *
        if self.aggFns[0] == 'count(':
            relation = self.getRel(self) # select random relation from database
            self.rels.append(relation.name) # add relation to rels array
            
            # choose * or an attribute
            astOrAttr = random.choice(['*', self.getAttr(relation).name]) 
            self.attrs.append(astOrAttr) # add chosen attribute function / * to array instance variable
        
        # if not doing a count
        else:
            relation = self.getRel(numeric = True) # select relation that countains a numeric attribute from database
            self.rels.append(relation.name) # add chosen relation function to rels
            attr = self.getAttr(relation, numeric = True) # select numeric attribute from relation
            self.attrs.append(attr.name) # add chosen attribute function to array instance variable
        

        
    """
        Chooses a condition and a relation.
        Aggregate put in aggFns[0]
        Relation put in rels[0]
    """  
    @abstractmethod
    def createCond(self):
        condType = random.choice(self.condition) # select a random condition
        self.conds.append(condType) # add chosen condition to array instance variable

        relation = self.getRel() # select a random relation
        self.rels.append(relation.name) # add chosen relation to array instance variable

        # choose * or an attribute
        astOrAttr = random.choice(['*', self.getAttr(relation).name]) 
        self.attrs.append(astOrAttr) # add chosen attribute function / * to array instance variable
        
        match condType:
            
            # If this is an "order by" condition
            case 'order by':
                self.createOrderByCond(relation)
                
            case 'limit':
                self.createLimitCond(relation)
            
            case 'where':
                self.createWhereCond(relation)
            
            case _:
                print("Invalid condition")
                self.aggFns.append('')#placeholder
                self.asNames.append('')#placeholder
                

    """
        Append an extra attribute and either ASC to DESC to the conds array.
    """  
    @abstractmethod
    def createOrderByCond(self, relation):
        
        attr = self.getAttr(relation) # select a second random attribute 
        # (can be the same as attr_1)
        self.conds.append(attr.name) # add chosen attribute to array instance variable

        orderBy = random.choice(['ASC', 'DESC']) # choose between ascending or descending order
        self.conds.append(orderBy) # add chosen order to array instance variable


    # If this is a "limit" condition
    """
        Append an extra attribute and either ASC to DESC to the conds array.
    """  
    @abstractmethod
    def createLimitCond(self, relation):
        
        lim = random.randrange(1, min(10,relation.getNumRows()), 1) # choose a random value between 1 and 10 (if there are 10 rows)
        self.conds.append(str(lim)) # add chosen limit to array instance variable


    # If this is a "where" condition
    @abstractmethod
    def createWhereCond(self, relation):
        pass

    @abstractmethod
    def toQuery(self):
        pass
    
    
    
