# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

import ISQLQuery
import random

class EasySQLQuery(ISQLQuery):
    
    def __init__(database, seed):
        super().__init__(database, seed)
        
    def easyBuilder(self):
        # Randomly select either an aggregate fn or condition or neither
        aggOrCond = random.choice(['agg', 'cond', ''])

        match aggOrCond:
            # If the random selection is an aggregate fn
            case 'agg':
                self.createAgg()
            
            # If the random selection is a condition
            case 'cond':
                self.createCond()
        
            case '':
                self.createSimple()
                

        self.rels += ['','']
        self.query = self.toQuery()
    
    
    # If this is a "where" condition
    def createWhereCond(self, relation):
        
        attr = self.setAttr(relation) # select a second random attribute 
        # (can be the same as attr_1)
        self.conds.append(attr.name) # add chosen attribute to conds array

        nullOrVal = random.choice(['null', 'val']) # Choose between ensuring the attribute value 
        # is not null and ensuring it has a given value
        # If null option chosen and attribute contains null values
        if nullOrVal == 'null' and self.conds[1].null == 'YES':
            operator = random.choice(self.nullOperators)
            self.conds.append(operator)
            self.conds.append('NULL')
        #If value option chosen or attribute does not contain any nulls
        else:
            operator = random.choice(self.operators)
            self.conds.append(operator)
            # Select a required value for the attribute
            reqVal = self.selectAttrVal(relation, self.conds[1])
            self.conds.append(str(reqVal)) # add chosen required value to array instance variable
    
