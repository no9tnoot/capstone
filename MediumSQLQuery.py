# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from ISQLQuery import ISQLQuery
import random
import math

class MediumSQLQuery(ISQLQuery):
    
    
    def __init__(self, database, seed):
        super().__init__(database, seed)
        self.asNames = [] #names for AS aggregates
        self.mediumBuilder()
        
    def getRel(self, numeric=False):
        return super().getRel(numeric)
    
    def getAttr(self, relation, numeric=False):
        return super().getAttr(relation, numeric)
    
    def selectAttrVal(self, relation, attribute):
        return super().selectAttrVal(relation, attribute)
    
    def setAgg(self):
        return super().setAgg()
    
    def formatQueryAggs(self, attributes, aggregates):
        return super().formatQueryAggs(attributes, aggregates)
    
    def formatQueryConds(self, conds):
        return super().formatQueryConds(conds)
    
    def createAgg(self):
        return super().createAgg()
    
    def createCond(self, relation):
        return super().createCond(relation)
    
    def createOrderByCond(self, relation):
        return super().createOrderByCond(relation)
    
    def createLimitCond(self, relation):
        return super().createLimitCond(relation)
    
    def createWhereCond(self, relation):
        return super().createWhereCond(relation)
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()
        
    def mediumBuilder(self):
        # Randomly select either an aggregate fn or condition or neither
        components = random.choice(['agg&cond', 'like']) # distinct, as

        match components:
            # If the random selection is an aggregate fn
            case 'agg&cond':
                self.createAgg() # create the agg component, and return the chosen relation
                self.createCond(self.rels[0]) #create the cond component using the chosen relation
            
            case 'like':
                relation = self.getRel(self) # select random relation from database
                self.createLikeCond(relation)
                
        self.query = self.toQuery()
    

    def createLikeCond(self, relation):
        
        self.conds['opperator']='like'
        
        attr = self.getAttr(relation) # select a second random attribute 
        # (can be the same as attr_1)
        self.conds['val1'] = attr # add chosen attribute to conds array

        
        val = self.selectAttrVal(relation, attr)  #select an attribute from the relation
        val = [char for char in val]  # turn string into an array of characters
        
        print(val) #for testing
        
        # if val is only 1 character long, don't remove any characters
        if len(val)==1:
            startswith = random.choice([True,False])
            num_char_to_remove = 0
            self.insertPercentWildCard(val, startswith, num_char_to_remove)
        
        # if val is longer than 1 character long
        else:
            likeType = random.choice(['%', '%%', '_%', 'x%'])
            
            match likeType:
                
                #Either 'starts with' or 'ends with' a string
                case '%':
                    startswith = random.choice([True,False])
                    num_char_to_remove = random.randint(math.ceil(0.5*len(val)), len(val)-1)
                    self.insertPercentWildCard(val, startswith, num_char_to_remove)

                # 'Contains' a string
                case '%%':
                    num_char_to_remove = random.randint(math.ceil(0.25*len(val)), math.floor(0.5*len(val)-1))
                    self.insertPercentWildCard(val, True, num_char_to_remove)
                    num_char_to_remove = random.randint(math.ceil(0.25*len(val)), math.floor(0.5*len(val)-1))
                    self.insertPercentWildCard(val, False, num_char_to_remove)
                
                # First/Second/Third/Fourth etc letter is x
                case '_%':
                    startswith = random.choice(True,False)
                    num_char_to_remove = random.randint(0, min(10, len(val)-1))
                    self.insertPercentWildCard(val, startswith, num_char_to_remove)
                    match startswith:
                        case True:
                            for i in range(0,num_char_to_remove):
                                val.insert(0, '_')
                        case False:
                            for i in range(0,num_char_to_remove):
                                val.append('_')
                            
        self.conds['val2']=val 
    

    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns)
        q += ' FROM ' + self.rels[0].name
        q += self.formatQueryConds(self.conds)
        return q
    
    
    """
        Insert a percentage wildcard at the given index in value (an array of characters),
        and remove a number of characters wither before (startswith True) or after (startswith 
        False) the percentage wildcard.
    """
    def insertPercentWildCard(self, value, startswith, num_char_to_remove):
        
        match startswith:
            
            case True:
                #remove the first n characters
                for i in range(0, num_char_to_remove):
                    value.pop(i)
                value.insert(0, '%') # insert % at beginning
                
            case False:
                #remove the last n characters
                for i in range(num_char_to_remove-1,len(value)-1):
                    value.pop(i)
                value.append('%') # insert % at end


# #temp for testing
from Session import Session     
d = Session.loadDatabase()
s = MediumSQLQuery(d, 'seed')
print(s.getSqlQuery())