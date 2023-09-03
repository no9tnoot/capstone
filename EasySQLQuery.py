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
    
    """
        Create an attribute with neither a condition nor an aggregate function
    """
    def createSimple(self):
        relation = self.setRel() # get random relation
        self.rels.append(relation)
        
        numAttr = random.choice(1,2)  # will we ask for one or 2 relations
        self.attrs.append(self.setAttr(relation))
        
        # select and set the second relation if one is needed
        while numAttr==2:
            attr2 = self.setAttr(relation)
            if (attr2 != self.attrs[0]): # don't set the same relation as the first one
                self.attrs.append(attr2)
                numAttr = 0
    
    
        
    """
        Chooses an aggregate and a relation that fits that aggregate (i.e. numeric). 
        Aggregate put in aggFns[0]
        Relation put in rels[0]
    """    
    def createAgg(self):
        self.aggFns.append(self.setAgg())  # get a random aggreegate func and storing it in aggFns
        
        # If doing a count agg, account for *
        if self.aggFns[0] == 'count(':
            relation = self.setRel(self) # select random relation from database
            self.rels.append(relation.name) # add relation to rels array
            
            # choose * or an attribute
            astOrAttr = random.choice(['*', self.setAttr(relation).name]) 
            self.attrs.append(astOrAttr) # add chosen attribute function / * to array instance variable
        
        # if not doing a count
        else:
            relation = self.setRel(self, numeric = True) # select relation that countains a numeric attribute from database
            self.rels.append(relation.name) # add chosen relation function to rels
            attr = self.setAttr(relation, numeric = True) # select numeric attribute from relation
            self.attrs.append(attr.name) # add chosen attribute function to array instance variable
        
        ####PLEASE MAKE ME IRRELEVENT    
        self.conds = ['','','','']#placeholder
        
    """
        Chooses a condition and a relation.
        Aggregate put in aggFns[0]
        Relation put in rels[0]
    """  
    def createCond(self):
        condType = random.choice(self.condition) # select a random condition
        self.conds.append(condType) # add chosen condition to array instance variable

        relation = self.setRel() # select a random relation
        self.rels.append(relation.name) # add chosen relation to array instance variable

        # choose * or an attribute
        astOrAttr = random.choice(['*', self.setAttr(relation).name]) 
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
    def createOrderByCond(self, relation):
        
        attr = self.setAttr(relation) # select a second random attribute 
        # (can be the same as attr_1)
        self.conds.append(attr.name) # add chosen attribute to array instance variable

        orderBy = random.choice(['ASC', 'DESC']) # choose between ascending or descending order
        self.conds.append(orderBy) # add chosen order to array instance variable


    # If this is a "limit" condition
    """
        Append an extra attribute and either ASC to DESC to the conds array.
    """  
    def createLimitCond(self, relation):
        
        lim = random.randrange(1, min(10,relation.getNumRows()), 1) # choose a random value between 1 and 10 (if there are 10 rows)
        self.conds.append(str(lim)) # add chosen limit to array instance variable


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
    
