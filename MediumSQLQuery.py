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
        
    def getRel(self, numeric=False, string=False):
        return super().getRel(numeric, string)
    
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
    
    def createSimple(self, relation):
        return super().createSimple(relation)
    
    def createOrderByCond(self, relation):
        return super().createOrderByCond(relation)
    
    def createLimitCond(self, relation):
        return super().createLimitCond(relation)
    
    def createWhereCond(self, relation, cond_details):
        return super().createWhereCond(relation, cond_details)
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()
        
    def mediumBuilder(self):
        # Randomly select either an aggregate fn or conds or neither
        components = random.choice(['distinct', 'like', 'or']) # distinct, as
        match components:
            case 'distinct':
                self.distinct = True
                relation = self.getRel() # select random relation from database
                self.createSimple(relation)
            
            case 'like':
                relation = self.getRel(string=True) # select random relation from database
                self.createSimple(relation)
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
                        self.createSimple(relation)
                        self.createLikeCond(relation, self.conds)
                        self.createOrCond(relation, string=True)

            case _:
                print('Invalid component')
                
                
        self.query = self.toQuery()
    
    def createOrCond(self, relation, string=False):
        self.orCond=True
        self.conds['or']={}
        like = random.choice([True, False])
        if string and like:
            while self.conds['val2']!=self.conds['or']['val2']:
                self.createLikeCond(relation, self.conds['or'])
        else:
            while self.conds['val2']!=self.conds['or']['val2']:
                self.createWhereCond(relation, self.conds['or'])
        self.conds['or']['cond']='or'
        
        
    
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
    

    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns)
        q += ' FROM ' + self.rels['rel1'].name
        if self.conds:
            q += self.formatQueryConds(self.conds)
        if self.orCond:
            q += self.formatQueryConds(self.conds['or'])
        return q
    
    
    """
        Insert a percentage wildcard at the given index in value (an array of characters),
        and remove a number of characters wither before (startswith True) or after (startswith 
        False) the percentage wildcard.
    """
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


# #temp for testing
# from Session import Session     
# d = Session.loadDatabase()
# s = MediumSQLQuery(d, 'seed')
# print(s.getSqlQuery())