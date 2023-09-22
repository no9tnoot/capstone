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
    def __init__(self, database):
        self.db = database
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
        
        self.groupBy = {}
        
        # Flags
        self.distinct = False
        self.orCond = False
        self.nested=False
        self.join = False
        
        self.roundTo = ''
  
  
    
    """
        Randomly selects and returns a relation from the loaded database.
        By default does not require relation to contain numeric, string, or roundable attributes.
    """
    @abstractmethod
    def getRel(self, numeric = False, string = False, roundable = False):

        relation = random.randrange(0, self.db.numRelations()-1, 1) # select a random relation index to get from database
        relation = self.db.getRelation(relation) # get relation from database
        
        # if the relation needs to be numeric, ensure it has at least 1 numeric attribute
        if numeric:
            if relation.hasNumeric():
                self.rels['rel1'] = relation
                return relation
            else:
                return self.getRel(numeric=True) # recurse until a numeric relation is selected
        
        # if the relation needs to be a string, ensure it has at least 1 string attribute
        elif string:
            if relation.hasString():
                self.rels['rel1'] = relation
                return relation
            else:
                return self.getRel(string=True) # recurse until a string relation is selected
            
        # if the relation needs to be roundable, ensure it has at least 1 numeric roundable
        elif roundable:
            if relation.hasRoundable():
                self.rels['rel1'] = relation
                return relation
            else:
                return self.getRel(roundable=True) # recurse until a roundable relation is selected
        
        # if there are no special requirements, just select a random relation
        else:
            self.rels['rel1'] = relation
            return relation

    """
        Returns a random aggregate function
    """
    @abstractmethod
    def getAgg(self, numeric=False):
        if numeric: aggType = random.choice(self.aggregateFunctions) # select the type of aggregate function
        else: aggType = random.choice(['count(', 'max(', 'min('])
        return aggType # add chosen aggregate function to array instance variable


    """
        Formats attributes and aggregates into a readable string, 
        e.g. "max(customerNumber), customerName"
    """
    @abstractmethod
    def formatQueryAggs(self, attributes, aggregates):
        aggs = '' # initialise the string to empty
        
        # add keyword distinct if doing a distinct query
        d='' # not distinct
        if self.distinct: d='DISTINCT '  # distinct
        
        # if there is an aggregate function
        if aggregates and attributes:
            aggs += aggregates[0] + d + attributes[0].name + self.roundTo + ')' # concatenate the aggregate and attribute to aggs
            # if still some attributes to do
            if len(attributes)>1:
                for att in attributes[1:]:
                    if not att.isEqual(ISQLQuery.asterisk): aggs += ", " + att.name
        
        # if there is no aggregate function
        elif attributes:
            aggs += d
            if attributes[0].isEqual(ISQLQuery.asterisk): 
                aggs += attributes[0].name
            else:
                for att in attributes[:-1]:
                    aggs += att.name + ", "
                aggs += attributes[-1].name
        return aggs # return the string of aggregate function and attributes
    
    
    """
        Formats conditions and attributes into a readable string.
        e.g. "where customerName = 'Greg'"
    """
    @abstractmethod
    def formatQueryConds(self, conds):
        cond = '' # initialise empty string
        
        condType = conds['cond'].lower()
        if condType == 'or': condType = 'where'
        
        # format depends on type of conditional
        match condType:
            
            case 'where':
                if self.nested: # if doing a nested conditional, add brackets and turn the nested query (conds['val2']) into a string
                     cond = ' ' + conds['cond'] + ' ' + conds['val1'].name + ' ' + conds['operator'] + ' (' + conds['val2'].toQuery() +')'
                else:
                    apostrophes = True # add ' ' around string value to compare (e.g. 'Greg')
                    if conds['val1'].numeric or conds['val2']=='NULL': apostrophes = False
                    if apostrophes:  
                        cond = ' ' + conds['cond'] + ' ' + conds['val1'].name + ' ' + conds['operator'] + ' \'' + conds['val2'] + '\''
                    else: cond = ' ' + conds['cond'] + ' ' + conds['val1'].name + ' ' + conds['operator'] + ' ' + conds['val2']
                
            
            case 'limit':
                cond = ' ' + conds['cond'] + ' ' + conds['val2']
            
            case 'order by':
                cond = ' ' + conds['cond'] + ' ' + conds['val1'].name + ' ' + conds['operator']
            
            # case 'or':
            #     cond = ' ' + conds['cond'] + ' ' + conds['val1'].name + ' ' + conds['operator'] + ' ' + conds['val2']
            
            case _:
                print('Invalid condition')    
        
        return cond
    
    
    """
        Create an attribute with neither a condition nor an aggregate function
    """
    @abstractmethod
    def createSimple(self, relation, attribute = None):
        # if the attribute has not been specified
        if attribute is None:
            attr1 = relation.getAttribute()
            self.attrs.append(attr1) # get a random attribute and append it to attrs
            # select and set the second relation if one is needed
            if len(relation.attributes)>2: numAttr = random.choice([1,2])  # will we ask for 1 or 2 attributes
            else: numAttr = 1
            while numAttr==2: # loop until second attr different to first
                attr2 = relation.getAttribute()
                if (attr2 != self.attrs[0]): 
                    self.attrs.append(attr2)
                    numAttr = 0
        
        # if the attribute has been specified, simply append it to attrs
        else: self.attrs.append(attribute) 
        
        
    """
        Chooses an aggregate and a relation that fits that aggregate (i.e. numeric). 
        Aggregate put in aggFns[0]
        Relation put in rels['rel1']
    """    
    @abstractmethod
    def createAgg(self, relation=None, attribute=None, aggFn=None):
        if relation is None: relation = self.getRel() # if relation not specified, select random relation from database
                
        if aggFn is None: aggFn = self.getAgg(numeric = relation.hasNumeric()) # if aggregate function not specified, get a random aggreegate func 
        self.aggFns.append(aggFn)  # store the aggregate function in aggFns
        
        # If doing a count agg, allow for the chosen attribute to be *
        if self.aggFns[0] == 'count(':
            # choose * or an attribute
            if attribute is None:
                attribute = random.choice([ISQLQuery.asterisk, relation.getAttribute()]) 
            self.attrs.append(attribute) # add chosen attribute function / * to array instance variable
        
        # if not doing a count (cannot have *)
        else:
            if attribute is None: attribute = relation.getAttribute(relation.hasNumeric()) # select numeric attribute from relation
            self.attrs.append(attribute) # add chosen attribute function to array instance variable
        

        
    """
        Chooses a condition  (e.g. 'where', 'limit by') and a relation.
        Puts the condition put in conds['cond']
        Relation put in rels['rel1']
    """  
    @abstractmethod
    def createCond(self, relation, astOrAttr = None, condType=None, numeric=False, whereAttr = None):
        if condType is None: condType = random.choice(self.condition) # select a random condition if no condition specified
        self.conds['cond'] = condType # add chosen condition to dictionary instance variable

        # choose * or an attribute (if not specified)
        if astOrAttr is None: 
            if self.attrs: astOrAttr = relation.getAttribute()
            else: astOrAttr = random.choice([ISQLQuery.asterisk, relation.getAttribute()]) 
        self.attrs.append(astOrAttr) # add chosen attribute function / * to attrs array instance variable
        
        # creation depends on the type of condition
        match condType:
            
            # If this is an "order by" condition
            case 'order by':
                self.createOrderByCond(relation)
            
            # If this is a "limit by" condition
            case 'limit':
                self.createLimitCond(relation)
            
            # If this is a "where" condition
            case 'where':
                self.cond = self.createWhereCond(relation, self.conds, numeric=numeric, whereAttr=whereAttr)
                self.conds['cond'] = condType
            
            case _:
                print("Invalid condition")
                

    """
        Creates an 'order by' condition.
        Adds an attribute by which to order the output, and either ASC to DESC, to the conds array.
    """  
    @abstractmethod
    def createOrderByCond(self, relation):
        attr = relation.getAttribute() # select a second random attribute to order by (can be the same as attr_1)
        self.conds['val1'] = attr # add chosen attribute to conditions dictionary

        orderBy = random.choice(['ASC', 'DESC']) # choose between ascending or descending order
        self.conds['operator'] = orderBy # add chosen order to conditions dictionary


    """
        Creates a 'limit' condition.
        Adds a value by which to limit the output to the conds array.
    """  
    @abstractmethod
    def createLimitCond(self, relation):
        lim = random.randrange(1, min(10,relation.getNumRows()), 1) # choose a random value between 1 and 10 (if there are 10 rows)
        self.conds['val2'] = str(lim) # add chosen limit to array instance variable


    """
        Creates a 'where' condition.
        
    """
    @abstractmethod
    def createWhereCond(self, relation, cond_details, numeric=False, whereAttr=None):   
        if whereAttr is None: whereAttr = relation.getAttribute(numeric) # select a second random attribute 
        # (can be the same as attr_1)
        cond_details['val1'] = whereAttr # add chosen attribute to conds array

        nullOrVal = random.choice(['null', 'val']) # Choose between ensuring the attribute value 
        # is not null and ensuring it has a given value
        # If null option chosen and attribute contains null values
        if nullOrVal == 'null' and cond_details['val1'].null == 'YES':
            operator = random.choice(self.nullOperators)
            cond_details['operator'] = operator
            cond_details['val2'] = 'NULL'
        #If value option chosen or attribute does not contain any nulls
        else:
            
            if whereAttr.numeric:
                operator = random.choice(self.operators)
            
            else:
                operator = '='
            
            cond_details['operator'] = operator
            # Select a required value for the attribute
            reqVal = self.db.selectAttrVal(relation, cond_details['val1'])
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

        
        val = self.db.selectAttrVal(relation, attr)  #select an attribute from the relation
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
    def easyBuilder(self, relation, attribute=None, aggOrCond = None, aggFn=None, condType = None):
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
                self.createCond(relation, attribute, condType)
            
            case 'nestedWhereCond':
                if relation is None: relation = self.getRel(numeric=True)
                self.createCond(relation, attribute, 'where', numeric=True)
            
            case 'groupByWhereCond':
                whereAttr = random.choice(relation.groupByAttributes)
                while whereAttr.isEqual(attribute): 
                    whereAttr = random.choice(relation.groupByAttributes)
                self.createCond(relation, attribute, 'where', whereAttr = whereAttr)
        
            case '':
                if relation is None: relation = self.getRel()
                self.createSimple(relation, attribute)
                
        self.rels['rel1']=relation
    
    @abstractmethod
    def mediumBuilder(self, relation = None, attribute = None, components = None):
        # Randomly select either an aggregate fn or conds or neither
        if components is None: components = random.choice(['distinct', 'like', 'or', 'round']) # distinct, as
        match components:
            case 'distinct':
                self.distinct = True
                count = random.choice([True, False])
                if relation is None: relation = self.getRel()
                if count:
                    while attribute is None or attribute.isEqual(ISQLQuery.asterisk):
                        attribute = relation.getAttribute()
                    self.createAgg(relation=relation,attribute=attribute, aggFn = 'count(')
                else:
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
                'nested': self.nested,
                'join': self.join,
                'groupBy': self.groupBy}
        
        return dict
    
    
    
