# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from abc import ABC, abstractmethod
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
    
    """
        Initialises the instance variables of the Query
    """
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
        Selects an attribute to impose a condition on, an operator to impose, and either NULL or 
        a possible value from the database to compare the attribute to.
    """
    @abstractmethod
    def createWhereCond(self, relation, cond_details, numeric=False, whereAttr=None):  
         
        if whereAttr is None: whereAttr = relation.getAttribute(numeric) # select a second random attribute 
        # (can be the same as attr_1)
        
        cond_details['val1'] = whereAttr # add chosen attribute to conds array

        nullOrVal = random.choice(['null', 'val']) # Choose between ensuring the attribute value 
                                                   # is not null and ensuring it has a given value
        
        # If null option chosen and attribute contains null values, do a null comparison
        if nullOrVal == 'null' and cond_details['val1'].null == 'YES':
            operator = random.choice(self.nullOperators) # select a null operator
            cond_details['operator'] = operator
            cond_details['val2'] = 'NULL'
            
        #If value option chosen or attribute does not contain any nulls, compare to an actual value 
        else:
            if whereAttr.numeric: # if attribute is numeric, can use any operator
                operator = random.choice(self.operators)
            
            else: # if attribute is not numeric, can only use '='
                operator = '='
            
            cond_details['operator'] = operator
            
            # Select a value from the database to compare the attribute to
            reqVal = self.db.selectAttrVal(relation, cond_details['val1'])
            cond_details['val2'] = str(reqVal) # add chosen required value to array instance variable
        
        return cond_details
    
    
    """
        Creates a 'like' condition.
        Selects a string attribute to impose the like on, a comparison string, and inserts wildcard 
        operators into the comparison string.
    """
    @abstractmethod
    def createLikeCond(self, relation, cond_details):
        # initialise the like dictionary
        cond_details['likeDict']={}
        cond_details['cond']='where'
        cond_details['operator']='like'
        
        attr = relation.getAttribute(string = True) # select a second random attribute, must be a string type
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
            if len(val)>3:
                likeType = random.choice(['%', '%%', '_%'])
            else:
                likeType = random.choice(['%', '_%'])
            match likeType:
                
                # Either 'starts with' or 'ends with' a string
                case '%':
                    ends_with_perc = random.choice([True,False])
                    num_char_to_remove = random.randint(min(max(2, len(val)-10), len(val)-2), len(val)-1) # how many char to remove where the wildcard is inserted 
                    val = self.insertPercentWildCard(val, ends_with_perc, num_char_to_remove, cond_details)

                # 'Contains' a string
                case '%%': 
                    ends_with_perc=False # this both ends and starts with perc, doesn't matter
                    num_char_to_remove = random.randint(min(max(2, len(val)-10), len(val)-2), len(val)-1) # how many char to remove
                    left_remove = random.randint(0, num_char_to_remove-1) # how many char to remove from left 
                    right_remove = num_char_to_remove - left_remove # how many char to remove from right 
                    val = self.insertPercentWildCard(val, True, left_remove, cond_details)
                    val = self.insertPercentWildCard(val, False, right_remove, cond_details)
                    cond_details['likeDict']['wildcard_free_string'] = ''.join(val[1:-1]) # remove the starting and trailing '%' to get wildcard free string
                
                # First/Second/Third/Fourth etc letter is x 
                case '_%':
                    ends_with_perc = random.choice([True,False]) 
                    num_underscore = random.randint(1, min(4, len(val)-1)) # number of char to replace with underscores
                    cond_details['likeDict']['num_underscore'] = num_underscore
                    val = self.insertPercentWildCard(val, ends_with_perc, len(val)-num_underscore-1, cond_details) # insert percent wildcard on the opposite side from the underscore
                    
                    match ends_with_perc:
                        case True: # if ends with perc, replace char(s) at start with underscore(s)
                            val = val[num_underscore:]
                            cond_details['likeDict']['wildcard_free_string'] = ''.join(val[:-1])
                            for i in range(0,num_underscore):
                                val.insert(0, '_')
                        case False: # if starts with perc, replace char(s) at end with underscore(s)
                            val = val[:-num_underscore]
                            cond_details['likeDict']['wildcard_free_string'] = ''.join(val[1:])
                            for i in range(0,num_underscore):
                                val.append('_')

                case _:
                    print('Invalid like type')
                            
        cond_details['val2']=''.join(val) # join the array of char into the comparison string 
        cond_details['likeDict']['type']=likeType
        cond_details['likeDict']['starts_with_string']=ends_with_perc
        
        
    """
        Insert a percentage wildcard at the given index in value (an array of characters),
        and remove a number of characters with before (startswith True) or after (startswith 
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


    """
        Sets the query instance variables with values for an easy SQL query. Can create queries
        of type 'aggregate' (i.e. selecting max(), avg(), etc. values), 'conditional' (i.e. doing a 
        limit by, where clause, order by etc.) and a simple type, which just generates a plain select query.
    """
    @abstractmethod
    def easyBuilder(self, relation, attribute=None, aggOrCond = None, aggFn=None, condType = None):
        # Randomly select either an aggregate fn or condition or neither
        if aggOrCond is None: aggOrCond = random.choice(['agg', 'cond', ''])

        match aggOrCond:
            # Generate an aggregate function
            case 'agg':
                if relation is None: relation = self.getRel(numeric=True) # get a random numeric relation
                self.createAgg(relation, attribute, aggFn)
            
            # Generate a condition 
            case 'cond':
                if relation is None: relation = self.getRel() # get a random relation of any type
                self.createCond(relation, attribute, condType)
            
            # Generate a where condition to be nested in a hard query
            case 'nestedWhereCond': 
                if relation is None: relation = self.getRel(numeric=True) # get a random numeric relatoin
                self.createCond(relation, attribute, 'where', numeric=True) # do a where comparison with a numeric attribute
            
            # Generate a where condition or a group by hard query
            case 'groupByWhereCond': # used to construct hard queries
                whereAttr = random.choice(relation.groupByAttributes) # get a random attribute that can be used to group by
                while whereAttr.isEqual(attribute): # make sure the whereAttr is not the same as the group by attr
                    whereAttr = random.choice(relation.groupByAttributes)
                self.createCond(relation, attribute, 'where', whereAttr = whereAttr)

            # Generate a simple query with no condition or aggregate
            case '':
                if relation is None: relation = self.getRel()
                self.createSimple(relation, attribute)
                
        self.rels['rel1']=relation # add the relation to the rels dictionary
    
    
    """
        Sets the query instance variables with values for a medium SQL query. Can create queries
        of type 'distinct', 'like' (i.e. doing a string comparison), 'or' (two conditions), and 
        'round', which rounds off a float / double attribute.
    """
    @abstractmethod
    def mediumBuilder(self, relation = None, attribute = None, components = None):
        # Randomly select the type of medium query to build
        if components is None: components = random.choice(['distinct', 'like', 'or', 'round']) # distinct, as

        match components:
            # Generate a distinct query, which selects distinct values for either a simple or a count() aggregate query
            case 'distinct':
                self.distinct = True
                count = random.choice([True, False]) # decide if doing a count() function
                if relation is None: relation = self.getRel() # get a random relation (if relation unspecified)
                if count:
                    # select an attribute, and make sure it is not the asterisk (*)
                    while attribute is None or attribute.isEqual(ISQLQuery.asterisk):
                        attribute = relation.getAttribute()
                    self.createAgg(relation=relation,attribute=attribute, aggFn = 'count(')
                else:
                    self.createSimple(relation, attribute)
            
            # Generate a 'like' query, comparing an attribute to a possible string with wildcards
            case 'like':
                if relation is None: relation = self.getRel(string=True) # select random relation from database
                self.easyBuilder(relation, attribute) # create an aggregate, conditional or simple query
                self.createLikeCond(relation, self.conds) # ass a like condition component
                
            # Generate an 'or' query (two conditions - either like or where)
            case 'or':
                choice = random.choice(['like', 'where'])
                match choice:
                    case 'where':
                        relation = self.getRel() # select random relation from database
                        self.conds['cond'] = 'where'
                        astOrAttr = random.choice([ISQLQuery.asterisk, relation.getAttribute()]) 
                        self.attrs.append(astOrAttr) # add chosen attribute function / * to array instance variable
                        self.createWhereCond(relation, self.conds) # create a where condition
                        self.createOrCond(relation) # create the or condition
                    case 'like':
                        relation = self.getRel(string=True) # select random relation from database
                        self.easyBuilder(relation)
                        self.createLikeCond(relation, self.conds) # create a like condition
                        self.createOrCond(relation, string=True) # create an or cond
            
            # Generate a rounding query 
            case 'round':
                relation = self.getRel(roundable=True) # select random relation from database that can be rounded (float or double)
                self.createRoundAgg(relation)
                

            case _:
                print('Invalid component')
            
                
    """
        Formats instance variable information into a string SQL command and returns it.
    """
    @abstractmethod
    def toQuery(self):
        pass

    """
        Returns the string SQL query.
    """
    @abstractmethod
    def getSqlQuery(self):
        return self.query
    
    """
        Places instance variable information into a dictionary and returns it. Dictionary is used 
        to create the English queries.
    """
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
    
    
    
