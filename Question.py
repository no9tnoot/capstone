# Molly Ryan
# 7 August 2023
# Question Class

import Database
import random
# val = random.random()
# print(val)


class Question:

    def __init__(self, database, seed):
        # get the attributes and their types from SQL, as well as the relations
        self.opperators = ['=', '<', '>', '<=', '>=', 'is', 'is not']
        self.aggregateFunctions = ['count(', 'max(', 'min(', 'avg(', '']
        self.condition = ['where', 'limit', 'order by', '']
        self.db = database
        self.seed = seed
        self.questionBuilder()

    # remove excess characters from datatype
    # e.g. smallint unsigned -> smallint, binary(4) -> binary

    def simplifyDatatype(self, attrType):

        # if contains a space, split at space
        if " " in attrType:
            attrType = attrType.split(" ")

        # if contains a bracket, split at bracket
        elif "(" in attrType:
            attrType = attrType.split("(")

        # ensure attrType will come out of this if else statement as an array
        else:
            attrType = attrType.split()

        # return simplified datatype
        return attrType[0]

"""Functionality now handled in Database class - pull from the database.numericRelations array
    # Returns true if the datatype is numeric (not a string/date/time)

    def isNumeric(self, attrType):

        if attrType == 'bit' or attrType == 'tinyint' or attrType == 'smallint' or attrType == 'mediumint' or attrType == 'int' or attrType == 'integer' or attrType == 'bigint' or attrType == 'float' or attrType == 'double' or attrType == 'decimal' or attrType == 'dec':
            # print("Numeric: " + attrType) # testing (delete me)
            return True

        else:
            return False
"""

    # Randomly selects a relation from the loaded database

    def setRel(self, attTypeNeeded):

        # select relation
        relation = random.randrange(0, newDB.numRelations()-1, 1)
        relation = newDB.getRelation(relation)

        # if the chosen action is a condition, just return the relation
        if attTypeNeeded == 'cond':
            return relation

        # if the chosen action is an aggregate fn or operator, first 
        # ensure relation contains at least one numeric attribute
        else:
            # iterate through attributes, looking for numeric
            for i in range(relation.getNumAttributes()):

                # remove excess characters from datatype 
                # eg. smallint unsigned -> smallint, binary(4) -> binary
                attrType = self.simplifyDatatype(
                    relation.getAttribute(i).getDataType())

                # if numeric, return relation
                if self.isNumeric(attrType):
                    return relation

                # if no numeric attributes in relation, recurse and select a new relation
                elif i == relation.getNumAttributes()-1:
                    '''I'm not confident this will work, as I haven't run an example that tested it.
                       setAttr() has the same logic, however, and it works''' 
                    relation = self.setRel(attTypeNeeded)
                    return relation

    ''' For questions where 2+ attributes are chosen from one relation, must include logic to prevent the
        attribute being selected twice'''

    def setAttr(self, relation, attTypeNeeded):
        # select random attribute from relation
        attribute = random.randrange(0, relation.getNumAttributes()-1, 1)
        attribute = relation.getAttribute(attribute)

        '''Must include option for where attribute given is *. This happens:
            - for conditions
            - for counts '''

        # remove excess characters from datatype eg. smallint unsigned -> smallint, binary(4) -> binary
        attrType = self.simplifyDatatype(attribute.getDataType())

        # if numeric, return attribute
        if self.isNumeric(attrType):
            return attribute

        # else, recurse until select numeric attribute
        else:
            attribute = self.setAttr(relation, attTypeNeeded)
            return attribute

    def questionBuilder(self):
        # Randomly select either an aggregate fn or condition
        aggOrCond = random.choice(['agg', 'cond'])
        # select relation from database
        relation = self.setRel(aggOrCond)
        # print("Relation: " + relation.name) # testing (delete me)

        # If the random selection is an aggregate fn
        if aggOrCond == 'agg':
            # select the type of aggregate function
            aggType = random.choice(self.aggregateFunctions)
            # print("Aggregate Function: " + aggType) # testing (delete me)

            # select attribute from relation
            attr = self.setAttr(relation, aggOrCond)
            # print("Attribute: " + attr.name) # testing (delete me)

            print("SELECT " + aggType + attr.name + ") FROM " + relation.name) # testing (delete me)

        # If the random selection is a condition, select a random column and random condition
        elif aggOrCond == 'cond':
            condType = random.choice(self.condition)
            print("Condition") # testing (delete me)

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
newDB = Database.Database(db_name='sakila')
# print(newDB.numRelations())
newQ = Question(newDB, 'seed')
