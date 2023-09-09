# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

import ISQLQuery
import random

class MediumSQLQuery(ISQLQuery):
    
    
    def __init__(self):
        super.__init__(self)
        self.asNames = [] #names for AS aggregates
    
    # If this is a "where" condition
    def createWhereCond(self, relation):
        
        attr = self.setAttr(relation) # select a second random attribute 
        # (can be the same as attr_1)
        self.conds.append(attr.name) # add chosen attribute to conds array

        whereCond = random.choice(['null', 'val', 'like']) # Choose between ensuring the attribute value 
        # is not null, ensuring it has a given value, or string comparison (like)
        # If null option chosen and attribute contains null values
        
        match whereCond:
            case 'like':
                self.conds.append('like')
                val = self.selectAttrVal(self, relation, attr)
                val = [char for char in val]  # turn string into an array of characters
                
                x = random.choice(0,1)   # if 1: at least 1 _ , if 0: at least 1 %
                
                match type:
                    case 'simple':
                        # do a 'begins with' / ;ends with'
                        pass
                    case 'hard':
                        numUnderscore = random.randint(x,min(0.5*len(val), 8))
                        numPercentage = random.randint(1-x,3)
                
                        for p in range(1,numPercentage):
                            i = random.randint(0,len(val)-1)
                            val[i] = '%'
                            y=random.choice(-1,1)
                            decreasing = random.choice(True,False)
                            if decreasing:
                                char_to_remove = range(0,-random.randint(1,numUnderscore/p),-1)
                            else:
                                char_to_remove = range(random.randint(numUnderscore/p),0,-1)
                            for char in char_to_remove:
                                val.pop(i+char_to_remove)
                    
                
                
                        
                        
                        
                    
                
                # unfinished I'm trying
                
                
                
            case 'null':        
                if self.conds[1].null == 'YES':
                    operator = random.choice(self.nullOperators)
                    self.conds.append(operator)
                    self.conds.append('NULL')

            case _:
                operator = random.choice(self.operators)
                self.conds.append(operator)
                # Select a required value for the attribute
                reqVal = self.selectAttrVal(relation, self.conds[1])
                self.conds.append(str(reqVal)) # add chosen required value to array instance variable
    
    
    
    def toQuery(self):
        q = 'SELECT '
        q += self.queryAggs(self.attrs, self.aggFns, self.asNames)
        q += 'FROM' + self.queryRels(self.rels[0], self.rels[1], self.rels[2])
        q += self.queryConds(self.conds)
        return q