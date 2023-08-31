# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

import ISQLQuery
import random

class EasySQLQuery(ISQLQuery):
    
    def __init__(database, seed):
        super().__init__(database, seed)
    
    # Randomly selects a relation from the loaded database
    def setRel(self, attTypeNeeded, aggOrCondType):
        super.setRel(self, attTypeNeeded, aggOrCondType)
    
    
    # Randomly selects an attribute from the chosen relation
    def setAttr(self, relation, attTypeNeeded, aggOrCondType, attNum):
        super.setAttr(self, relation, attTypeNeeded, aggOrCondType, attNum)
    
    
    def selectAttrVal(self, relation, attribute):
        super.selectAttrVal(self, relation, attribute)
        
        
    def setAgg(self):
        super.setAgg(self)
        
        
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
                relation = self.setRel()
                self.rels.append(relation)
                self.attrs.append(self.setAttr(relation))

        self.rels += ['','']
        self.query = self.toQuery()
        
        # Send the relevant array to the English Question function
        self.question = Question.englishQuestion([self.aggFns, self.attrs, self.rels, self.conds])
        
        
    def createAgg(self):
        self.setAgg()
        if self.aggFns[0] == 'count(':
            relation = self.setRel(self) # select relation from database
            self.rels.append(relation.name) # add chosen aggregate function to array instance variable
            astOrAttr = random.choice(['*', 'attribute'])
            if astOrAttr == '*':
                self.attrs.append('*')
            else:
                attr = self.setAttr(relation) # select attribute from relation
                self.attrs.append(attr.name) # add chosen attribute function to array instance variable
        else:
            relation = self.setRel(self, True) # select relation that countains a numeric attribute from database
            self.rels.append(relation.name) # add chosen aggregate function to array instance variable
            attr = self.setAttr(relation, True) # select numeric attribute from relation
            self.attrs.append(attr.name) # add chosen attribute function to array instance variable
        self.asNames.append('')#placeholder

            
        self.conds = ['','','','']#placeholder
        
        
    def createCond(self):
        condType = random.choice(self.condition) # select a random condition
        self.conds.append(condType) # add chosen condition to array instance variable

        relation = self.setRel() # select a random relation
        self.rels.append(relation.name) # add chosen relation to array instance variable

        astOrAttr = random.choice(['*', 'attribute'])
        if astOrAttr == '*':
            self.attrs.append('*')
            self.aggFns.append('')
        else:
            attr = self.setAttr(relation) # select attribute from relation
            self.attrs.append(attr.name) # add chosen attribute function to array instance variable
            self.aggFns.append('')

        #placeholder array for aggs
        #self.aggFns.append('')

        # If this is an "order by" condition
        if condType == 'order by':
            attr = self.setAttr(relation) # select a second random attribute 
            # (can be the same as attr_1)
            self.conds.append(attr.name) # add chosen attribute to array instance variable

            orderBy = random.choice(['ASC', 'DESC']) # choose between ascending or descending order
            self.conds.append(orderBy) # add chosen order to array instance variable


        # If this is a "limit" condition
        elif condType == 'limit':
            
            lim = random.randrange(1, relation.getNumRows(), 1) # choose a random value between 1 
            # and the total number of rows in the relation
            
            ''' ^ Should we limit this more? Possibly so that it's easily countable and the student
                can see if they're right'''

            self.conds.append('')
            self.conds.append(str(lim)) # add chosen limit to array instance variable

        # If this is a "where" condition
        elif condType == 'where':
            
            attr = self.setAttr(relation) # select a second random attribute 
            # (can be the same as attr_1)
            self.conds.append(attr.name) # add chosen attribute to array instance variable

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
        else:
            print("Invalid condition")
        self.aggFns.append('')#placeholder
        self.asNames.append('')#placeholder