# Molly Ryan
# 7 August 2023
# Database Class

from array import *
import random

import mysql.connector # python3 --version, and then # pip3.8 install mysql-connector-python

"""
    Database attribute (column) with instance variables showing column name, 
    data type, if there are any nulls in the column, and the key (prime attribute
    or not)
"""
class Attribute:
    
    def __init__(self, name, dt='', null='', k=''):
        self.name=name
        if not isinstance(dt, str):
            dt=dt.decode()
        self.dataType=dt
        self.null=null
        self.key=k
        self.numeric = Attribute.isNumeric(self)
        self.roundable = Attribute.isRoundable(self)
        self.string = Attribute.isString(self)
    
    def getName(self):
        return self.name
        
    def getDataType(self):
        return self.dataType

    # Sets numeric to True if the attribute is numeric (not a string/date/time/boolean)
    def isNumeric(self):
        
        isNum = False
        
        numDataType = ['bit', 'int', 'float', 'double', 'dec']
        
        # search to see if the dataType contains one of the above strings - indicating numeric attribute
        for dt in numDataType:
            if dt in self.dataType.lower():  # set the dataType to lower case to include all string cases in search
                isNum = True
        
        return isNum
    
    # Sets string to True if the attribute is string (not a numeric/date/time/boolean)
    def isString(self):
        
        isString = False
        
        stringDataType = ['char', 'varchar', 'text', 'tinytext', 'mediumtext', 'longtext']
        
        # search to see if the dataType contains one of the above strings - indicating numeric attribute
        for dt in stringDataType:
            if dt in self.dataType.lower():  # set the dataType to lower case to include all string cases in search
                isString = True
        
        return isString
    
    # Sets numeric to True if the attribute is numeric (not a string/date/time/boolean)
    def isRoundable(self):
        
        isRoundable = False
        
        roundableDataType = ['float', 'double']
        
        # search to see if the dataType contains one of the above strings - indicating numeric attribute
        for dt in roundableDataType:
            if dt in self.dataType.lower():  # set the dataType to lower case to include all string cases in search
                isRoundable = True
        
        return isRoundable
    



""" 
    Database relation (table), with instance variables showing the name 
    of the relation, and an array containing all the attributes stored in 
    the relation.
"""
class Relation:
    
    def __init__(self, n, nrow):
        self.name = n
        self.attributes=[]
        self.numericAttributes=[]
        self.stringAttributes=[]
        self.roundableAttributes=[]
        self.numRows = nrow
    
    def ___str___(self):
        return self.name
    
    
    def addAttribute(self, attribute):
        self.attributes.append(attribute)
        # If attribute is numeric, add to numericAttributes array
        if (attribute.numeric):
            self.numericAttributes.append(attribute)
            if (attribute.roundable):
                self.roundableAttributes.append(attribute)
        # If attribute is string, add to stringAttributes array
        if (attribute.string):
            self.stringAttributes.append(attribute)
    
    
    # Returns if the relation has numeric attributes
    def hasNumeric(self):
        return len(self.numericAttributes)>0
    
    # Returns if the relation has string attributes
    def hasString(self):
        return len(self.stringAttributes)>0
    
    # Returns if the relation has numeric attributes
    def hasRoundable(self):
        return len(self.roundableAttributes)>0

        
    def getAttribute(self, numeric = False, string = False, roundable = False):
        # check that the attribute number asked for is not out of bounds
        if not numeric and not string and not roundable:
            i = random.randrange(0, self.getNumAttributes()-1, 1)
            return self.attributes[i]

        elif numeric:
            i = random.randrange(0, len(self.numericAttributes), 1)
            return self.numericAttributes[i]

        elif string:
            i = random.randrange(0, len(self.stringAttributes), 1)
            return self.stringAttributes[i]
        
        elif roundable:
            i = random.randrange(0, len(self.roundableAttributes), 1)
            return self.roundableAttributes[i]

            
        
    def getNumAttributes(self):
        return len(self.attributes)
    
    def getNumRows(self):
        return self.numRows




""" 
    Database
"""
class Database:
    
    def __init__(self, host, user, pword, db_name):
        
        self.relations = []  # initialise empty array of relations
        self.numericRelations = [] # initialise empty array of relations that contain at least 1 numeric attribute
        self.host = host
        self.user = user
        self.pword = pword
        self.db_name = db_name
        self.loadRelations()
            
        
    """ Get the attributes and their types from SQL, as well as the relations"""
    def loadRelations(self):
        # connect to sql database
        database = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.pword,
            database=self.db_name
        )
        
        cursor = database.cursor()  # Create a cursor to interact with the database
        
        cursor.execute("SHOW TABLES;")   # SQL: print the table names             
        tables = cursor.fetchall()       # get the output table names from SQL
        
        # create each relation object and store in relations[]
        for table in tables:
            
            cursor.execute("SELECT count(*) FROM " + table[0] + ";")   # SQL: print the number of rows in table
            nrows = cursor.fetchall()
            nrows = nrows[0][0]
            
            r = Relation(table[0], nrows)       # Create a relation for each table name
            self.relations.append(r)     # store created relation in relations[]
            
            cursor.execute("SHOW COLUMNS FROM "+r.name+" ;") # get column details for relation r
            columns = cursor.fetchall()
            
            
            #create each attribute object for relation r
            for column in columns:
                r.addAttribute(Attribute(column[0], column[1], column[2], column[3]))
            
            # if relation r contains at least 1 numeric attribute, add it to numericRelations array
            if (r.hasNumeric() > 0):
                self.numericRelations.append(r)
        
    
    def numRelations(self):
        return len(self.relations)
    
    def numNumericRelations(self):
        return len(self.numericRelations)
       
    def getRelation(self, i):
        return self.relations[i]
    
    def getNumericRelation(self, i):
        return self.numericRelations[i]
