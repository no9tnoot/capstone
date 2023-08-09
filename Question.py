# Molly Ryan
# 7 August 2023
# Question Class

import Database
import random
#val = random.random()
#print(val)

class Question:
    
    def __init__(self, database, seed):
        # get the attributes and their types from SQL, as well as the relations
        self.opperators = ['=', '<', '>', '<=', '>=', 'is', 'is not']
        self.aggregateFunctions = ['count(', 'max(', 'min(', 'avg(', '']
        self.condition = ['where', 'limit', 'order by', '']
        self.db = database
        self.seed = seed
        self.questionBuilder()


    def setRel(self, attTypeNeeded):
            #select random relation from database
            relation = random.randrange(0, newDB.numRelations()-1, 1)
            relation = newDB.getRelation(relation)
            
            return relation #del

            # # if the chosen action is a condition
            # if attTypeNeeded == 'cond':
            #     return relation
            
            # # if the chosen action is an aggregate fn or operator
            # else:
            #     # ensure relation contains at least one numeric attribute
    
    # For questions where 2+ attributes are chosen from one relation, must include logic to prevent the 
    # attribute being selected twice
    def setAttr(self, relation, attTypeNeeded):
            #select random attribute from relation
            attribute = random.randrange(0, relation.getNumAttributes()-1, 1)
            attribute = relation.getAttribute(attribute)
            #Must include option for where attribute given is *, but then must be 

            return attribute #del

            # # if the chosen action is a condition
            # if attTypeNeeded == 'cond':
            #     return attribute
            
            # # if the chosen action is an aggregate fn or operator
            # else:
            #     # ensure attribute is numeric

     
    def questionBuilder(self):
        #Randomly select either an aggregate fn or condition
        aggOrCond = random.choice(['agg', 'cond'])
        #select relation from database
        relation = self.setRel(aggOrCond)
        # print("Relation: " + relation.name)

        #If the random selection is an aggregate fn
        if aggOrCond == 'agg':
            #select the type of aggregate function
            aggType = random.choice(self.aggregateFunctions)
            # print("Aggregate Function: " + aggType)

            #select attribute from relation
            attr = self.setAttr(relation, aggOrCond)
            # print("Attribute: " + attr.name)

            print("SELECT " + aggType + attr.name + ") FROM " + relation.name)


        #If the random selection is a condition, select a random column and random condition   
        elif aggOrCond == 'cond':
            condType = random.choice(self.condition)
            print("Condition")

        #Create Eng and SQL
 
class EasyQuestion(Question):
    
    def __init__(self, database, seed):
        super().__init__(database, seed)
        
class MediumQuestion(Question):
    
    def __init__(self):
        super().__init__()
        
        
class DifficultQuestion(Question):
    
    def __init__(self):
        super().__init__()

# testing (delete me)
newDB = Database.Database(db_name = 'sakila')
#print(newDB.numRelations())
newQ = Question(newDB, 'seed')
print(newQ)