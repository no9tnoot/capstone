# Molly Ryan
# 7 August 2023
# Question Class
import mysql.connector
import Database
import random
# val = random.random()
# print(val)


class Question2:

    def __init__(self, database, seed):
        # get the attributes and their types from SQL, as well as the relations
        self.opperators = ['=', '<', '>', '<=', '>=', 'is', 'is not']
        self.aggregateFunctions = ['count(', 'max(', 'min(', 'avg(', 'sum(']
        self.condition = ['where', 'limit', 'order by']
        self.db = database
        self.seed = seed
        self.question = ''
        self.query = ''

    """
    Functionality now handled in Database class - pull from the database.numericRelations array
    # Returns true if the datatype is numeric (not a string/date/time)
    """

    # Randomly selects a relation from the loaded database
    def setRel(self, attTypeNeeded, aggOrCondType):

        # select relation
        relation = random.randrange(0, self.db.numRelations()-1, 1)
        relation = self.db.getRelation(relation)

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

    # Randomly selects an attribute from the chosen relation
    def setAttr(self, relation, attTypeNeeded, aggOrCondType, attNum):

        # if condition or count, include * as an option
        '''decided to include * in this way as it will allow it to appear with reasonable frequency'''
        if attTypeNeeded == 'cond' or aggOrCondType == 'count(' or aggOrCondType == '':

            # Randomly select attribute from relation -> doesn't have to be numeric
            attribute = random.randrange(0, relation.getNumAttributes()-1, 1)
            attribute = relation.getAttribute(attribute)
            
            # Choose between attribute and '*' if attNum is 1
            # (Ensures that 2nd attribute is never * -> select x where y='*' doesn't make sense)
            if attNum == 1:
                astOrAttr = random.choice(['*', 'attribute'])
                if astOrAttr == '*':
                    attribute = Database.Attribute('*', 'varchar(50)' , 'NO', '')
        
        else: # * should not be an option
            attribute = random.randrange(0, len(relation.numericAttributes)-1, 1)
            attribute = relation.numericAttributes[attribute]
        
        return attribute


    # Function to return the number of rows in the relation
    def findNumRows(self, relation, attribute):

        # Connect to database
        database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mySQL_sew1',
            database='classicmodels2022'
        )

        cursor = database.cursor()  # Create a cursor to interact with the database
        
        cursor.execute("SELECT count(" + attribute.getName() + ") FROM " +
                       relation.getName() + ";")   # SQL: print the table names
       
        numRows = cursor.fetchall() # get the output table names from SQL
        
        return numRows[0][0] #Return the number of rows


    # Function to find a value for an attribute that you will set in the where clause
    # eg. WHERE attribute = 'attributeVal'
    def selectAttrVal(self, relation, attribute):

        # Connect to database
        database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='mySQL_sew1',
            database='classicmodels2022'
        )

        cursor = database.cursor()  # Create a cursor to interact with the database

        cursor.execute("SELECT " + attribute.getName() + " FROM " +
                       relation.getName() + ";")   # SQL: print the table names
        
        values = cursor.fetchall()       # get the output table names from SQL

        reqVal = random.randrange(0, len(values)-1, 1) #Select a random value between 0 and the total number 
        # of values -1
        reqVal = values[reqVal][0] # Select the attribute value in this position
        return reqVal
    
    #write the english question for the sql query
    def englishQuestion(sql):
        #2d array holds slots for each part of the question
        english = ['','']

        #aggregates and attributes
        english[0] = ['Show'] + Question2.block1(sql[1],sql[0])

        #relation, condition, attr2, #operator, compare to          self.aggFns, self.conds, self.attrs, self.rels
        english[1] = Question2.block2(sql[2], sql[4], sql[5], sql[6], sql[3])

        #test
        print(Question2.englishToString(english))

    def englishToString(english):
        question = ''
        for block in english:
            for string in block:
                question += string
        return question

    def block1(attributes, aggregates = ['']):
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
            if attributes[x] == '*':
                block1[x] += 'all columns'
            else:
                block1[x] += attributes[x]


            if len(attributes) > 1:
                if x >= len(attributes) - 2:
                    block1[x] += ' and'
                else:
                    block1[x] += ','

        return block1
    
    def block2(relation, x, operator, y, condition = ''):
        block2 = []

        #relation
        block2.append(' in the ' + relation[0] + ' table')

        match condition[0]:
            case 'limit':
                if y[0] == 1:
                    block2.append(' but only show 1 row')
                else:
                    block2.append(' but only show ' + y[0] + ' rows')
            case 'where':                                                   #add in operator for more options
                block2.append(' but only for rows with an ' + x[0] + ' value of ' + y[0])
            case 'order by':
                if y[0] == 'desc':
                    block2.append(' in descending order of ' + x[0] + ' value')
                else:
                    block2.append(' in ascending order of ' + x[0] + ' value')

        block2.append('.')
        return block2
    
    def getQuestion(self):
        return self.question
    
    def getQuery(self):
        return self.query

# Class to manage easy questions -> 1 aggregate function OR 1 condition
class EasyQuestion(Question2):
    # Ordered list of aggregate functions used in the query
    aggFns = []

    # Ordered list of conditions used in the query
    conds = []
    conds2 = []
    opps = []

    # Ordered list of attributes used in the query
    attrs = []
    attrs2 = []

    # Ordered list of relations used in the query
    rels = []

    # Constructor
    def __init__(self, database, seed):
        super().__init__(database, seed)
        self.easyBuilder()

    # Function to create SQL query and send the relevant information to the English Question functions
    def easyBuilder(self):
        # Randomly select either an aggregate fn or condition
        aggOrCond = random.choice(['agg', 'cond', ''])

        if aggOrCond == 'agg':

            aggType = random.choice(self.aggregateFunctions) # select the type of aggregate function
            self.aggFns.append(aggType) # add chosen aggregate function to array instance variable 

            relation = Question2.setRel(self, aggOrCond, aggType) # select relation from database
            self.rels.append(relation.getName()) # add chosen aggregate function to array instance variable 

            attr = self.setAttr(relation, aggOrCond, aggType, 1) # select attribute from relation
            self.attrs.append(attr.getName()) # add chosen aggregate function to array instance variable 

            # Assign this string to the instance variable 'question' in the Question parent class
            self.query = ("SELECT " + aggType + attr.getName() +
                    ") FROM " + relation.getName() + ";")

        elif aggOrCond == 'cond':
            condType = random.choice(self.condition) # select a random condition
            self.conds.append(condType) # add chosen condition to array instance variable

            relation = Question2.setRel(self, aggOrCond, condType) # select a random relation
            self.rels.append(relation.getName()) # add chosen relation to array instance variable

            '''Should I overload this function so that it doesn't have to deal with the numeric checks?'''
            attr_1 = self.setAttr(relation, aggOrCond, condType, 1) # select a random attribute
            self.attrs.append(attr_1.getName()) # add chosen attribute to array instance variable

            match condType:
                case 'order by':
                    attr_2 = self.setAttr(relation, aggOrCond, condType, 2) # select a second random attribute 
                    # (can be the same as attr_1)
                    self.attrs2.append(attr_2.getName()) # add chosen attribute to array instance variable

                    orderBy = random.choice(['ASC', 'DESC']) # choose between ascending or descending order
                    self.conds2.append(orderBy) # add chosen order to array instance variable
                case 'limit':
                    numRows = Question2.findNumRows(self, relation, attr_1) # get number of rows in relation -> numRows
                    lim = random.randrange(1, numRows, 1) # choose a random value between 1 
                    # and the total number of rows in the relation
                    
                    ''' ^ Should we limit this more? Possibly so that it's easily countable and the student
                        can see if they're right'''

                    self.conds2.append(lim) # add chosen limit to array instance variable
                case 'where':  
                    attr_2 = self.setAttr(relation, aggOrCond, condType, 2) # select a second random attribute 
                    # (can be the same as attr_1)
                    self.attrs2.append(attr_2.getName()) # add chosen attribute to array instance variable
                        
                    # Select a required value for the attribute
                    reqVal = Question2.selectAttrVal(
                        self, relation, attr_2)
                    
                    self.opps.append('=')
                    self.conds2.append(str(reqVal)) # add chosen required value to array instance variable

            # Assign this string to the instance variable 'question' in the Question parent class
            self.query = ("SELECT " + self.attrs[0] + " FROM " + self.rels[0] +
                    ' ' + self.conds[0] + ' ' + self.attrs2[0] + ' ' + self.opps[0] + self.conds2[0] + "';")
        else:
            relation = Question2.setRel(self, aggOrCond, '') # select relation from database
            self.rels.append(relation.getName()) # add chosen aggregate function to array instance variable 

            attr = self.setAttr(relation, aggOrCond, '', 1) # select attribute from relation
            self.attrs.append(attr.getName()) # add chosen aggregate function to array instance variable 

            # Assign this string to the instance variable 'question' in the Question parent class
            self.query = ("SELECT " + attr.getName() +
                    ") FROM " + relation.getName() + ";")
        
        # Send the relevant array to the English Question function
        self.question = Question2.englishQuestion([self.aggFns, self.attrs, self.rels, self.conds, self.attrs2, self.opps, self.conds2])


class MediumQuestion(Question2):

    def __init__(self):
        super().__init__()


class DifficultQuestion(Question2):

    def __init__(self):
        super().__init__()


# testing (delete me)
#newDB = Database.Database(db_name='classicmodels2022')
# print(newDB.numRelations())
#newQ = EasyQuestion(newDB, 'seed')

#sql = [[''],['*'], ['offices'],['where'],['country'],['Spain']]
#Question.englishQuestion(sql)