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
            host=self.db.host,
            user=self.db.user,
            password=self.db.pword,
            database=self.db.db_name
        )

        cursor = database.cursor()  # Create a cursor to interact with the database
        
        cursor.execute("SELECT count(" + attribute.name + ") FROM " +
                       relation.name + ";")   # SQL: print the table names
       
        numRows = cursor.fetchall() # get the output table names from SQL
        
        return numRows[0][0] #Return the number of rows


    # Function to find a value for an attribute that you will set in the where clause
    # eg. WHERE attribute = 'attributeVal'
    def selectAttrVal(self, relation, attribute):

        # Connect to database
        database = mysql.connector.connect(
            host=self.db.host,
            user=self.db.user,
            password=self.db.pword,
            database=self.db.db_name
        )

        cursor = database.cursor()  # Create a cursor to interact with the database

        cursor.execute("SELECT " + attribute.name + " FROM " +
                       relation.name + ";")   # SQL: print the table names
        
        values = cursor.fetchall()       # get the output table names from SQL

        reqVal = random.randrange(0, len(values)-1, 1) #Select a random value between 0 and the total number 
        # of values -1
        reqVal = values[reqVal][0] # Select the attribute value in this position
        return reqVal
    
    #write the english question for the sql query
    def englishQuestion(sql):
        #2d array holds slots for each part of the question
        english = ['','']

        """Note to Peter: sql[0]->aggregate functions, sql[1]->conditions, sql[2]->attributes, 
        sql[3]->relations"""

        #aggregates and attributes
        english[0] = ['Show'] + Question.block1(sql[2], sql[0])

        #relation, condition, attr2, #operator, compare to          self.aggFns, self.conds, self.attrs, self.rels
        english[1] = Question.block2(sql[3], sql[1])

        #test
        return(Question.englishToString(english))

    #makes the array into a string
    def englishToString(english):
        question = ''
        for block in english:
            for string in block:
                question += string
        return question

    def block1(attributes, aggregates):
        #aggregate functions go in the first slot
        block1 = []

        #text for attributes and aggregates. supports multiple of each
        for x in range(len(attributes)):
            match aggregates[x]:
                case 'count(':
                    block1.append(' how many rows there are in ')
                case 'max(':
                    block1.append(' the greatest value of ')
                case 'min(':
                    block1.append(' the smallest value of ')
                case 'avg(':
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
    
    def block2(relation, condition):
        block2 = []

        #relation
        block2.append(' in the ' + relation[0] + ' table')

        #add text for conditions
        match condition[0]:
            case 'limit':
                if condition[2] == 1:
                    block2.append(' but only show 1 row')
                else:
                    block2.append(' but only show ' + condition[2] + ' rows')
            case 'where':
                block2.append(' but only for rows where ' + condition[1] + ' is equal to ' + condition[2])
            case 'order by':
                if condition[2].lower() == 'desc':
                    block2.append(' in descending order of ' + condition[1] + ' value')
                else:
                    block2.append(' in ascending order of ' + condition[1] + ' value')

        block2.append('.')
        return block2
    
    #return english question
    def getQuestion(self):
        return self.question
    
    #return sql query
    def getQuery(self):
        return self.query

# Class to manage easy questions -> 1 aggregate function OR 1 condition
class EasyQuestion(Question):

    # Constructor
    def __init__(self, database, seed):
        super().__init__(database, seed)
        

        self.query = ''
        self.question = ''

        # Ordered list of aggregate functions used in the query
        self.aggFns = []

        # Ordered list of conditions used in the query
        self.conds = []

        # Ordered list of attributes used in the query
        self.attrs = []

        # Ordered list of relations used in the query
        self.rels = []

        self.easyBuilder()

    # Function to create SQL query and send the relevant information to the English Question functions
    def easyBuilder(self):
        # Randomly select either an aggregate fn or condition
        aggOrCond = random.choice(['agg', 'cond'])

        # If the random selection is an aggregate fn
        if aggOrCond == 'agg':

            aggType = random.choice(self.aggregateFunctions) # select the type of aggregate function
            self.aggFns.append(aggType) # add chosen aggregate function to array instance variable 

            relation = Question.setRel(self, aggOrCond, aggType) # select relation from database
            self.rels.append(relation.name) # add chosen aggregate function to array instance variable 

            attr = self.setAttr(relation, aggOrCond, aggType, 1) # select attribute from relation
            self.attrs.append(attr.name) # add chosen aggregate function to array instance variable

            #placeholder array for conds
            self.conds.append('') 

            # If there is no aggregate function
            if aggType == '':
                # Assign this string to the instance variable 'question' in the Question parent class
                self.query = ("SELECT " + aggType + attr.name +
                      " FROM " + relation.name + ";")
                
                # Send the relevant array to the English Question function
                self.question = Question.englishQuestion([self.aggFns, self.conds, self.attrs, self.rels])

            else:
                # Assign this string to the instance variable 'question' in the Question parent class
                self.query = ("SELECT " + aggType + attr.name +
                      ") FROM " + relation.name + ";")
                
                # Send the relevant array to the English Question function
                self.question = Question.englishQuestion([self.aggFns, self.conds, self.attrs, self.rels])

        # If the random selection is a condition
        elif aggOrCond == 'cond':
            condType = random.choice(self.condition) # select a random condition
            self.conds.append(condType) # add chosen condition to array instance variable

            relation = Question.setRel(self, aggOrCond, condType) # select a random relation
            self.rels.append(relation.name) # add chosen relation to array instance variable

            '''Should I overload this function so that it doesn't have to deal with the numeric checks?'''
            attr_1 = self.setAttr(relation, aggOrCond, condType, 1) # select a random attribute
            self.attrs.append(attr_1.name) # add chosen attribute to array instance variable

            #placeholder array for aggs
            self.aggFns.append('')

            # If there is no condition
            if condType == '':
                # Assign this string to the instance variable 'question' in the Question parent class
                self.query = ("SELECT " + condType + attr_1.name +
                      " FROM " + relation.name + ";")
                
                # Send the relevant array to the English Question function
                self.question = Question.englishQuestion([self.aggFns, self.conds, self.attrs, self.rels])

            # If this is an "order by" condition
            elif condType == 'order by':
                attr_2 = self.setAttr(relation, aggOrCond, condType, 2) # select a second random attribute 
                # (can be the same as attr_1)
                self.conds.append(attr_2.name) # add chosen attribute to array instance variable

                orderBy = random.choice(['ASC', 'DESC']) # choose between ascending or descending order
                self.conds.append(orderBy) # add chosen order to array instance variable

                # Assign this string to the instance variable 'question' in the Question parent class
                self.query = ("SELECT " + attr_1.name + " FROM " + relation.name +
                      " ORDER BY " + attr_2.name + ' ' + orderBy + ';')
                
                # Send the relevant array to the English Question function
                self.question = Question.englishQuestion([self.aggFns, self.conds, self.attrs, self.rels])

            # If this is a "limit" condition
            elif condType == 'limit':
                
                numRows = Question.findNumRows(self, relation, attr_1) # get number of rows in relation -> numRows
                lim = random.randrange(1, numRows, 1) # choose a random value between 1 
                # and the total number of rows in the relation
                
                ''' ^ Should we limit this more? Possibly so that it's easily countable and the student
                    can see if they're right'''

                self.conds.append('')
                self.conds.append(str(lim)) # add chosen limit to array instance variable

                # Assign this string to the instance variable 'question' in the Question parent class
                self.query = ("SELECT " + attr_1.name + " FROM " +
                      relation.name + " LIMIT " + str(lim) + ';')
                
                # Send the relevant array to the English Question function
                self.question = Question.englishQuestion([self.aggFns, self.conds, self.attrs, self.rels])

            # If this is a "where" condition
            elif condType == 'where':
                #nullOrVal = random.choice(['null', 'val']) # Choose between ensuring the attribute value 
                # is not null and ensuring it has a given value
                
                #self.conds.append(nullOrVal) # add chosen nullOrVal value to array instance variable
                
                attr_2 = self.setAttr(relation, aggOrCond, condType, 2) # select a second random attribute 
                # (can be the same as attr_1)
                self.conds.append(attr_2.name) # add chosen attribute to array instance variable

                # If null option chosen and attribute contains null values
                # if nullOrVal == 'null' and attr_2.null == 'YES':
                    
                #     # Assign this string to the instance variable 'question' in the Question parent class
                #     self.question = ("SELECT " + attr_1.name + " FROM " +
                #           relation.name + " WHERE " + attr_2.name + " IS NOT NULL;")
                    
                #     # Send the relevant array to the English Question function
                #     Question.englishQuestion([self.aggFns, self.conds, self.attrs, self.rels])

                # If value option chosen or attribute does not contain any nulls
                # else:
                #     # Change the value in the english question array to 'val'
                #     if nullOrVal == 'null':
                #         self.conds[1] = 'val'
                    
                    # Select a required value for the attribute
                reqVal = Question.selectAttrVal(
                    self, relation, attr_2)
                
                self.conds.append(str(reqVal)) # add chosen required value to array instance variable

                # Assign this string to the instance variable 'question' in the Question parent class
                self.query = ("SELECT " + attr_1.name + " FROM " + relation.name +
                        " WHERE " + attr_2.name + " = '" + str(reqVal) + "';")
                
                # Send the relevant array to the English Question function
                self.question = Question.englishQuestion([self.aggFns, self.conds, self.attrs, self.rels])

            else:
                print("Invalid condition")

class MediumQuestion(Question):

    def __init__(self):
        super().__init__()


class DifficultQuestion(Question):

    def __init__(self):
        super().__init__()
