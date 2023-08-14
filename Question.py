# Molly Ryan
# 7 August 2023
# Question Class
import mysql.connector
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
        EasyQuestion.easyBuilder(self)

    """
    Functionality now handled in Database class - pull from the database.numericRelations array
    # Returns true if the datatype is numeric (not a string/date/time)
    """

    def isNumeric(self, attrType):

        if attrType == 'bit' or attrType == 'tinyint' or attrType == 'smallint' or attrType == 'mediumint' or attrType == 'int' or attrType == 'integer' or attrType == 'bigint' or attrType == 'float' or attrType == 'double' or attrType == 'decimal' or attrType == 'dec':
            # print("Numeric: " + attrType) # testing (delete me)
            return True

        else:
            return False

    # Randomly selects a relation from the loaded database

    def setRel(self, attTypeNeeded, aggOrCondType):

        # select relation
        relation = random.randrange(0, newDB.numRelations()-1, 1)
        relation = newDB.getRelation(relation)

        # if the chosen relation contains numeric attributes, return it
        # if the chosen action is a condition, a count, or nothing, just return the relation
        if relation.numNumeric() or attTypeNeeded == 'cond' or aggOrCondType == 'count(' or aggOrCondType == '':
            return relation

        # if the chosen relation is not appropriate, select a new relation
        else:
            relation = self.setRel(attTypeNeeded, aggOrCondType)
            return relation

    ''' For questions where 2+ attributes are chosen from one relation, must include logic to prevent the
        attribute being selected twice'''

    def setAttr(self, relation, attTypeNeeded, aggOrCondType, attNum):

        # Randomly select attribute from relation


        # if condition or count, include * as an option
        '''decided to include * in this way as it will allow it to appear with reasonable frequency'''
        if attTypeNeeded == 'cond' or aggOrCondType == 'count(':
            # Randomly select attribute from relation -> doesn't have to be numeric
            attribute = random.randrange(0, relation.getNumAttributes()-1, 1)
            attribute = relation.getAttribute(attribute)
            
            # Choose between attribute and '*' if attNum is 1
            if attNum == 1:
                astOrAttr = random.choice(['*', 'attribute'])
                if astOrAttr == '*':
                    attribute = Database.Attribute('*', 'varchar(50)' , 'NO', '')
        
        else:
            print(aggOrCondType + " -> ensuring numeric")
            attribute = random.randrange(0, len(relation.numericAttributes)-1, 1)
            attribute = relation.numericAttributes[attribute]
        
        return attribute



    def findNumRows(self, relation, attribute):

        database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mySQL_sew1',
            database='classicmodels2022'
        )

        cursor = database.cursor()  # Create a cursor to interact with the database
        cursor.execute("SELECT count(" + attribute.name + ") FROM " +
                       relation.name + ";")   # SQL: print the table names
        numRows = cursor.fetchall()
        return numRows[0][0]


    # Find a value for an attribute that you will set in the where clause
    # eg. WHERE attribute = 'attributeVal'
    def selectAttrVal(self, relation, attribute):

        database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mySQL_sew1',
            database='classicmodels2022'
        )

        cursor = database.cursor()  # Create a cursor to interact with the database

        cursor.execute("SELECT " + attribute.name + " FROM " +
                       relation.name + ";")   # SQL: print the table names
        values = cursor.fetchall()       # get the output table names from SQL

        reqVal = random.randrange(0, len(values), 1)
        reqVal = values[reqVal][0]
        return reqVal
    
    #write the english question for the sql query
    def englishQuestion(sql):
        #2d array holds slots for each part of the question
        english = ['','']

        #aggregates and attributes
        english[0] = ['Show'] + Question.block1(sql[0], sql[1])
    
        #relation
        english[1] = ' in the ' + sql[2] + ' table.'

        #test
        print(Question.englishToString(english))

    def englishToString(english):
        question = ''
        for block in english:
            for string in block:
                question += string
        return question

    def block1(aggregates, attributes):
        #aggregate functions go in the first slot
        block1 = []

        for x in range(len(attributes)):
            match aggregates[x]:
                case 'count':
                    block1.append(' how many rows there are in ')
                case 'max':
                    block1.append(' the greatest value of ')
                case 'min':
                    block1.append(' the smallest value of ')
                case 'avg':
                    block1.append(' the average value of ')
                case _:
                    block1.append(' the values of ')

            #attribute/s
            block1[x] += attributes[x]

            if len(attributes) > 1:
                if x >= len(attributes) - 2:
                    block1[x] += ' and'
                else:
                    block1[x] += ','

        return block1


class EasyQuestion(Question):

    def __init__(self, database, seed):
        super().__init__(database, seed)

    def easyBuilder(self):
        # Randomly select either an aggregate fn or condition
        aggOrCond = random.choice(['agg', 'cond'])
        # aggOrCond = 'cond'

        # If the random selection is an aggregate fn
        if aggOrCond == 'agg':
            # select the type of aggregate function
            aggType = random.choice(self.aggregateFunctions)
            # print("Aggregate Function: " + aggType) # testing (delete me)

            # select relation from database
            relation = Question.setRel(self, aggOrCond, aggType)
            # print("Relation: " + relation) # testing (delete me)

            # select attribute from relation
            attr = self.setAttr(relation, aggOrCond, aggType, 1)
            # print("Attribute: " + attr.name) # testing (delete me)

            if aggType == '':
                print("SELECT " + aggType + attr.name +
                      " FROM " + relation.name + ";")
            else:
                print("SELECT " + aggType + attr.name +
                      ") FROM " + relation.name + ";")

        # If the random selection is a condition, select a random column and random condition
        elif aggOrCond == 'cond':
            condType = random.choice(self.condition)
            # condType = "where"
            # print("Condition: " + condType) # testing (delete me)

            relation = Question.setRel(self, aggOrCond, condType)
            # print("Relation: " + relation) # testing (delete me)

            '''Should I overload this function so that it doesn't have to deal with the numeric checks?'''
            attr_1 = self.setAttr(relation, aggOrCond, condType, 1)
            # print("Attribute 1: " + attr_1.name) # testing (delete me)

            if condType == '':
                print("SELECT " + condType + attr_1.name +
                      " FROM " + relation.name + ";")

            elif condType == 'order by':
                attr_2 = self.setAttr(relation, aggOrCond, condType, 2)
                # print("Attribute 2: " + attr_2.name) # testing (delete me)

                orderBy = random.choice(['ASC', 'DESC'])
                print("SELECT " + attr_1.name + " FROM " + relation.name +
                      " ORDER BY " + attr_2.name + ' ' + orderBy + ';')

            elif condType == 'limit':
                # get number of rows in relation -> numRows
                numRows = Question.findNumRows(self, relation, attr_1)
                lim = random.randrange(1, numRows, 1)
                print("SELECT " + attr_1.name + " FROM " +
                      relation.name + " LIMIT " + str(lim) + ';')

            elif condType == 'where':
                nullOrVal = random.choice(['null', 'val'])
                # nullOrVal = 'null'

                attr_2 = self.setAttr(relation, aggOrCond, condType, 2)
                # print("Attribute 2: " + attr_2.name) # testing (delete me)

                # an attribute is not null
                if nullOrVal == 'null' and attr_2.null == 'YES':
                    '''Should I first check if attribute 2 actually contains any nulls? That feels unneccesary?'''
                    print("SELECT " + attr_1.name + " FROM " +
                          relation.name + " WHERE " + attr_2.name + " IS NOT NULL;")

                else:
                    reqVal = Question.selectAttrVal(
                        self, relation, attr_2)
                    print("SELECT " + attr_1.name + " FROM " + relation.name +
                          " WHERE " + attr_2.name + " = '" + str(reqVal) + "';")

            else:
                print("Invalid condition")


class MediumQuestion(Question):

    def __init__(self):
        super().__init__()


class DifficultQuestion(Question):

    def __init__(self):
        super().__init__()


# testing (delete me)
newDB = Database.Database(db_name='classicmodels2022')
# print(newDB.numRelations())
newQ = EasyQuestion(newDB, 'seed')

sql = [['',''],['city', 'country'], 'offices']
Question.englishQuestion(sql)