# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from abc import ABC, abstractmethod
import mysql.connector
import random
import Database
import math

class ISQLQuery(ABC):
    
    operators = ['=', '<', '>', '<=', '>=']
    nullOperators = ['is', 'is not']
    aggregateFunctions = ['count(', 'max(', 'min(', 'avg(', 'sum(']
    condition = ['where', 'limit', 'order by']
    wildcard = ['%','_', ]
    asterisk = Database.Attribute('*')
    
    @abstractmethod
    def __init__(self, database, seed):
        self.db = database
        self.seed = seed
        self.queryString = ""
        self.queryArray = []
        
         # Ordered list of aggregate functions used in the query
        self.aggFns = []

        # Ordered list of conditions used in the query
        self.conds = {}

        # Ordered list of attributes used in the query
        self.attrs = []

        # Ordered list of relations used in the query
        self.rels = {}
        
        # Flags
        self.distinct = False
        self.orCond = False
        self.nested=False
        self.join = False
        
        self.roundTo = ''
  

        
    
    # Randomly selects a relation from the loaded database
    # by default does not require relation to contain numeric attributes    @abstractmethod
    def getRel(self, numeric = False, string = False, roundable = False):
        # select relation
        relation = random.randrange(0, self.db.numRelations()-1, 1)
        relation = self.db.getRelation(relation)
        if numeric:
            if relation.hasNumeric():
                self.rels['rel1'] = relation
                return relation
            else:
                return self.getRel(numeric=True)
        elif string:
            if relation.hasString():
                self.rels['rel1'] = relation
                return relation
            else:
                return self.getRel(string=True)
        elif roundable:
            if relation.hasRoundable():
                self.rels['rel1'] = relation
                return relation
            else:
                return self.getRel(roundable=True)
        else:
            self.rels['rel1'] = relation
            return relation


    ''' For questions where 2+ attributes are chosen from one relation, must include logic to prevent the
        attribute being selected twice'''

    
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
        
        reqVal = str( random.randint(0, relation.getNumRows()-1) ) #Select a random value between 0 and the total number of values -1

        cursor.execute("SELECT " + attribute.name + " FROM " + relation.name + " limit 1 offset " + reqVal + ";")   # SQL: print the table names
        
        val = cursor.fetchall()[0][0]
        
        if val is not None: # hopefully this works
            return val
        
        else: 
            return self.selectAttrVal(relation, attribute)
            # return the 

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
        d=''
        if self.distinct: d='distinct '
        if aggregates and attributes:
            aggs += aggregates[0] + d + attributes[0].name + self.roundTo + ')'
            # if still some attributes to do
            if len(attributes)>1:
                for att in attributes[1:]:
                    aggs += ", " + att.name
        elif attributes:
            for att in attributes[:-1]:
                aggs += att.name + ", "
            aggs += d + attributes[-1].name
            
        return aggs
    
    
    #conditions to query form. will add a few extra spaces in some cases but shouldn't matter too much 
    # still need to implement AND/OR for extra conditions   
    @abstractmethod
    def formatQueryConds(self, conds):
        cond = ''
        match conds['cond'].lower():
            case 'where':
                if self.nested:
                     cond = ' ' + conds['cond'] + ' ' + conds['val1'].name + ' ' + conds['operator'] + ' (' + conds['val2'].toQuery() +')'
                else:
                    cond = ' ' + conds['cond'] + ' ' + conds['val1'].name + ' ' + conds['operator'] + ' ' + conds['val2']
            case 'limit':
                cond = ' ' + conds['cond'] + ' ' + conds['val2']
            case 'order by':
                cond = ' ' + conds['cond'] + ' ' + conds['val1'].name + ' ' + conds['operator']
            case 'or':
                cond = ' ' + conds['cond'] + ' ' + conds['val1'].name + ' ' + conds['operator'] + ' ' + conds['val2']
            case _:
                print('Invalid condition')    
        return cond
    
    """
        Create an attribute with neither a condition nor an aggregate function
    """
    @abstractmethod
    def createSimple(self, relation, attribute = None):
        
        if attribute is None:
            numAttr = random.choice([1,2])  # will we ask for one or 2 relations
            self.attrs.append(relation.getAttribute())
             # select and set the second relation if one is needed
            while numAttr==2:
                attr2 = relation.getAttribute()
                if (attr2 != self.attrs[0]): # don't set the same relation as the first one
                    self.attrs.append(attr2)
                    numAttr = 0
        
        else: self.attrs.append(attribute)
        
       
    
    
        
    """
        Chooses an aggregate and a relation that fits that aggregate (i.e. numeric). 
        Aggregate put in aggFns[0]
        Relation put in rels[0]
    """    
    @abstractmethod
    def createAgg(self, relation=None, astOrAttr=None, aggFn=None):
        
        if aggFn is None: aggFn = self.setAgg() # get a random aggreegate func 
        
        self.aggFns.append(aggFn)  # store it in aggFns
        
        # If doing a count agg, account for *
        if self.aggFns[0] == 'count(':
            if relation is None: relation = self.getRel(self) # select random relation from database
            
            # choose * or an attribute
            if astOrAttr is None:
                astOrAttr = random.choice([ISQLQuery.asterisk, relation.getAttribute()]) 
            self.attrs.append(astOrAttr) # add chosen attribute function / * to array instance variable
        
        # if not doing a count
        else:
            if relation is None: relation = self.getRel(numeric = True) # select relation that countains a numeric attribute from database
            if astOrAttr is None: astOrAttr = relation.getAttribute(numeric=True) # select numeric attribute from relation
            self.attrs.append(astOrAttr) # add chosen attribute function to array instance variable
        

        
    """
        Chooses a condition and a relation.
        Aggregate put in aggFns[0]
        Relation put in rels[0]
    """  
    @abstractmethod
    def createCond(self, relation, astOrAttr = None, condType=None, numeric=False):
        
        if condType is None: condType = random.choice(self.condition) # select a random condition
        self.conds['cond'] = condType # add chosen condition to array instance variable

        # choose * or an attribute
        if astOrAttr is None: astOrAttr = random.choice([ISQLQuery.asterisk, relation.getAttribute()]) 
        self.attrs.append(astOrAttr) # add chosen attribute function / * to array instance variable
        
        match condType:
            
            # If this is an "order by" condition
            case 'order by':
                self.createOrderByCond(relation)
                
            case 'limit':
                self.createLimitCond(relation)
            
            case 'where':
                self.cond = self.createWhereCond(relation, self.conds, numeric=numeric)
                self.conds['cond'] = condType
            
            case _:
                print("Invalid condition")
                

    """
        Append an extra attribute and either ASC to DESC to the conds array.
    """  
    @abstractmethod
    def createOrderByCond(self, relation):
        

        attr = relation.getAttribute() # select a second random attribute 
        # (can be the same as attr_1)
        self.conds['val1'] = attr # add chosen attribute to array instance variable

        orderBy = random.choice(['ASC', 'DESC']) # choose between ascending or descending order
        self.conds['operator'] = orderBy # add chosen order to array instance variable


    # If this is a "limit" condition
    """
        Append an extra attribute and either ASC to DESC to the conds array.
    """  
    @abstractmethod
    def createLimitCond(self, relation):
        
        
        lim = random.randrange(1, min(10,relation.getNumRows()), 1) # choose a random value between 1 and 10 (if there are 10 rows)
        self.conds['val2'] = str(lim) # add chosen limit to array instance variable


    # If this is a "where" condition
    @abstractmethod
    def createWhereCond(self, relation, cond_details, numeric=False):        
        attr = relation.getAttribute(numeric) # select a second random attribute 
        # (can be the same as attr_1)
        cond_details['val1'] = attr # add chosen attribute to conds array

        nullOrVal = random.choice(['null', 'val']) # Choose between ensuring the attribute value 
        # is not null and ensuring it has a given value
        # If null option chosen and attribute contains null values
        if nullOrVal == 'null' and cond_details['val1'].null == 'YES':
            operator = random.choice(self.nullOperators)
            cond_details['operator'] = operator
            cond_details['val2'] = 'NULL'
        #If value option chosen or attribute does not contain any nulls
        else:
            
            if attr.numeric:
                operator = random.choice(self.operators)
            
            else:
                operator = '='
            
            cond_details['operator'] = operator
            # Select a required value for the attribute
            reqVal = self.selectAttrVal(relation, cond_details['val1'])
            cond_details['val2'] = str(reqVal) # add chosen required value to array instance variable
        return cond_details
    
    @abstractmethod
    def createLikeCond(self, relation, cond_details):
        cond_details['likeDict']={}
        cond_details['cond']='where'
        cond_details['operator']='like'
        
        attr = relation.getAttribute(string = True) # select a second random attribute 
        # (can be the same as attr_1)
        cond_details['val1'] = attr # add chosen attribute to conds array

        
        val = self.selectAttrVal(relation, attr)  #select an attribute from the relation
        val = [char for char in val]  # turn string into an array of characters
                
        # if val is only 1 character long, don't remove any characters
        if len(val)==1:
            likeType = '%'
            ends_with_perc = random.choice([True,False])
            num_char_to_remove = 0
            val = self.insertPercentWildCard(val, ends_with_perc, num_char_to_remove, cond_details)
        
        # if val is longer than 1 character long
        else:
            likeType = random.choice(['%', '%%', '_%'])
            
            match likeType:
                
                #Either 'starts with' or 'ends with' a string
                case '%':
                    ends_with_perc = random.choice([True,False])
                    num_char_to_remove = random.randint(1, len(val)-1)
                    val = self.insertPercentWildCard(val, ends_with_perc, num_char_to_remove, cond_details)

                # 'Contains' a string
                case '%%': 
                    ends_with_perc=False # this both ends and starts with perc, doesn't matter
                    num_char_to_remove = random.randint(1, math.floor(0.5*len(val)))
                    val = self.insertPercentWildCard(val, True, num_char_to_remove, cond_details)
                    num_char_to_remove = random.randint(1, math.floor(0.5*len(val)))
                    val = self.insertPercentWildCard(val, False, num_char_to_remove, cond_details)
                    cond_details['likeDict']['wildcard_free_string'] = ''.join(val[1:-1])
                
                # First/Second/Third/Fourth etc letter is x USE NUM_CHAR_TO_REMOVE AS INDEX TO ARRAY OF STRINGS ['FIRST',SECOND'...]
                case '_%':
                    ends_with_perc = random.choice([True,False]) 
                    num_underscore = random.randint(1, min(4, len(val)-1))
                    cond_details['likeDict']['num_underscore'] = num_underscore
                    val = self.insertPercentWildCard(val, ends_with_perc, len(val)-num_underscore-1, cond_details)
                    match ends_with_perc:
                        case True:
                            val = val[num_underscore:]
                            cond_details['likeDict']['wildcard_free_string'] = ''.join(val[:-1])
                            for i in range(0,num_underscore):
                                val.insert(0, '_')
                        case False:
                            val = val[:-num_underscore]
                            cond_details['likeDict']['wildcard_free_string'] = ''.join(val[1:])
                            for i in range(0,num_underscore):
                                val.append('_')

                case _:
                    print('Invalid like type')
                            
        cond_details['val2']=''.join(val)
        cond_details['likeDict']['type']=likeType
        cond_details['likeDict']['starts_with_string']=ends_with_perc
        
        
    """
        Insert a percentage wildcard at the given index in value (an array of characters),
        and remove a number of characters wither before (startswith True) or after (startswith 
        False) the percentage wildcard.
    """
    @abstractmethod
    def insertPercentWildCard(self, value, ends_with_perc, num_char_to_remove, cond_details):
        
        match ends_with_perc: 
            
            case False: # insert percentage at start ('ends with string')
                #remove the first n characters
                for i in range(0, num_char_to_remove):
                    value.pop(0)
                cond_details['likeDict']['wildcard_free_string'] = ''.join(value)
                value.insert(0, '%') # insert % at beginning
                
            case True: # insert percentage at end ('starts with string')
                #remove the last n characters
                for i in range(len(value)-num_char_to_remove,len(value)):
                    value.pop(-1)
                cond_details['likeDict']['wildcard_free_string'] = ''.join(value)
                value.append('%') # insert % at end
                
        return value

    @abstractmethod
    def easyBuilder(self, relation, attribute=None, aggOrCond = None, aggFn=None):
        # Randomly select either an aggregate fn or condition or neither
        if aggOrCond is None: aggOrCond = random.choice(['agg', 'cond', ''])

        match aggOrCond:
            # If the random selection is an aggregate fn
            case 'agg':
                if relation is None: relation = self.getRel(numeric=True)
                self.createAgg(relation, attribute, aggFn)
            
            # If the random selection is a condition
            case 'cond':
                if relation is None: relation = self.getRel()
                self.createCond(relation, attribute)
            
            case 'nestedWhereCond':
                if relation is None: relation = self.getRel(numeric=True)
                self.createCond(relation, attribute, 'where', numeric=True)
        
            case '':
                if relation is None: relation = self.getRel()
                self.createSimple(relation, attribute)
                
        self.rels['rel1']=relation
        #self.query = self.toQuery()
    
    @abstractmethod
    def mediumBuilder(self, relation = None, attribute = None, components = None):
        # Randomly select either an aggregate fn or conds or neither
        if components is None: components = random.choice(['distinct', 'like', 'or', 'round']) # distinct, as
        components='distinct'
        match components:
            case 'distinct':
                self.distinct = True
                count = random.choice([True, False])
                if count:
                    self.createAgg(aggFn = 'count(')
                else:
                    relation = self.getRel() # select random relation from database
                    self.createSimple(relation, attribute)
            
            case 'like':
                if relation is None: relation = self.getRel(string=True) # select random relation from database
                self.easyBuilder(relation, attribute)
                self.createLikeCond(relation, self.conds)
                
            case 'or':
                choice = random.choice(['like', 'where'])
                match choice:
                    case 'where':
                        relation = self.getRel() # select random relation from database
                        self.conds['cond'] = 'where'
                        astOrAttr = random.choice([ISQLQuery.asterisk, relation.getAttribute()]) 
                        self.attrs.append(astOrAttr) # add chosen attribute function / * to array instance variable
                        self.createWhereCond(relation, self.conds)
                        self.createOrCond(relation)
                    case 'like':
                        relation = self.getRel(string=True) # select random relation from database
                        self.easyBuilder(relation)
                        self.createLikeCond(relation, self.conds)
                        self.createOrCond(relation, string=True)
            
            case 'round':
                relation = self.getRel(roundable=True) # select random relation from database
                self.createRoundAgg(relation)
                

            case _:
                print('Invalid component')
            
                
        #self.query = self.toQuery()
    
    @abstractmethod
    def toQuery(self):
        pass

    @abstractmethod
    def getSqlQuery(self):
        return self.query
    
    @abstractmethod
    def getDict(self):
        dict = {'attributes': self.attrs, 
                'aggregates': self.aggFns,
                'relation': self.rels,
                'condition': self.conds,
                'distinct': self.distinct,
                'orCond': self.orCond,
                'roundTo': self.roundTo,
                'nested': self.nested}
        
        return dict
    
    
    
