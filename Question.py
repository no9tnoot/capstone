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
        self.operators = ['=', '<', '>', '<=', '>=']
        self.nullOperators = ['is', 'is not']
        self.aggregateFunctions = ['count(', 'max(', 'min(', 'avg(', 'sum(']
        self.condition = ['where', 'limit', 'order by']
        self.db = database
        self.seed = seed
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

        #names for AS aggregates
        self.asNames = []

    """
    Functionality now handled in Database class - pull from the database.numericRelations array
    # Returns true if the datatype is numeric (not a string/date/time)
    """

    # Randomly selects a relation from the loaded database
    # by default does not require relation to contain numeric attributes
    def setRel(self, numeric = False):

        # select relation
        relation = random.randrange(0, self.db.numRelations()-1, 1)
        relation = self.db.getRelation(relation)
        if not numeric:
            return relation
        else:
            if relation.numNumeric():
                return relation
            else:
                return self.setRel(True)

    ''' For questions where 2+ attributes are chosen from one relation, must include logic to prevent the
        attribute being selected twice'''

    # Randomly selects an attribute from the chosen relation
    def setAttr(self, relation, numeric = False):

        if not numeric:
            astOrAttr = random.choice(['*', 'attribute'])
            # Randomly select attribute from relation -> doesn't have to be numeric
            i = random.randrange(0, relation.getNumAttributes()-1, 1)
            attribute = relation.getAttribute(i)
        
        else: # * should not be an option
            i = random.randrange(0, relation.numNumeric(), 1)
            attribute = relation.getAttribute(i, True)
        
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
    
    def setAgg(self):
        aggType = random.choice(self.aggregateFunctions) # select the type of aggregate function
        self.aggFns.append(aggType) # add chosen aggregate function to array instance variable
    
    # takes aggregates, attributes, and AS names and put them into query form.
    def queryAggs(attributes, aggregates, asNames = ['']):
        aggs = ''
        if aggregates[0] != '':
            aggs += aggregates[0] + attributes[0] + ')' + asNames[0]
        else:
            aggs += attributes[0]
        
        #if we have more than one attribute/aggregate
        if len(attributes) > 1:
            for x in range(1,len(attributes)-1):
                if aggregates[x] != '':
                    aggs += ', ' + aggregates[x] + attributes[x] + ')' + asNames[x]
                else:
                    aggs += ', ' + attributes[x]
        return aggs
    
    # relation/s to query form. including joins
    def queryRels(rel1, rel2, join):
        if rel2 == '':
            return rel1
        else:
            return rel1 + join + rel2

    #conditions to query form. will add a few extra spaces in some cases but shouldn't matter too much 
    # still need to implement AND/OR for extra conditions   
    def queryConds(conds):
        cond = conds[0] + ' ' + conds[1] + ' ' + conds[2] + ' ' + conds[3]
        return cond

    def toQuery(self):
        q = 'SELECT '
        q += Question.queryAggs(self.attrs, self.aggFns, self.asNames)
        q += 'FROM' + Question.queryRels(self.rels[0], self.rels[1], self.rels[2])
        q += Question.queryConds(self.conds)
        return q

    #write the english question for the sql query
    def englishQuestion(sql):
        #2d array holds slots for each part of the question
        english = []

        #aggregates and attributes
        english.append(['Show'] + Question.block1(sql[1], sql[0]))

        #relation, condition, attr2, #operator, compare to          self.aggFns, self.conds, self.attrs, self.rels
        english.append(Question.block2(sql[3], sql[4]))

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
                if condition[1] == 1:
                    block2.append(' but only show 1 row')
                else:
                    block2.append(' but only show ' + condition[1] + ' rows')
            case 'where':
                block2.append(' but only for rows where ' + condition[1] + ' ' + condition[2] + ' ' + condition[3])
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

        self.easyBuilder()


    # Function to create SQL query and send the relevant information to the English Question functions
    def easyBuilder(self):
        # Randomly select either an aggregate fn or condition or neither
        aggOrCond = random.choice(['agg', 'cond', ''])

        # If the random selection is an aggregate fn
        if aggOrCond == 'agg':
            self.setAgg()
            if self.aggFns[0] == 'count(':
                relation = Question.setRel(self) # select relation from database
                self.rels.append(relation.name) # add chosen aggregate function to array instance variable
                astOrAttr = random.choice(['*', 'attribute'])
                if astOrAttr == '*':
                    self.attrs.append('*')
                else:
                    attr = self.setAttr(relation) # select attribute from relation
                    self.attrs.append(attr.name) # add chosen attribute function to array instance variable
            else:
                relation = Question.setRel(self, True) # select relation that countains a numeric attribute from database
                self.rels.append(relation.name) # add chosen aggregate function to array instance variable
                attr = self.setAttr(relation, True) # select numeric attribute from relation
                self.attrs.append(attr.name) # add chosen attribute function to array instance variable
            self.asNames.append('')#placeholder

                
            self.conds = ['','','','']#placeholder

        # If the random selection is a condition
        elif aggOrCond == 'cond':
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
                
                numRows = Question.findNumRows(self, relation, attr) # get number of rows in relation -> numRows
                lim = random.randrange(1, min(10,numRows), 1) # max limit is 10 unless there are less than 10 rows

                #self.conds.append('')
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
        
        elif aggOrCond == '':
            relation = self.setRel()
            self.rels.append(relation)
            self.attrs.append(self.setAttr(relation))

        self.rels += ['','']
        self.query = self.toQuery()
        
        # Send the relevant array to the English Question function
        self.question = Question.englishQuestion([self.aggFns, self.attrs, self.rels, self.conds])

class MediumQuestion(Question):

    def __init__(self):
        super().__init__()


class DifficultQuestion(Question):

    def __init__(self):
        super().__init__()
