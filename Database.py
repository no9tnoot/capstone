# Molly Ryan
# 7 August 2023
# Database Class

from array import *

import mysql.connector # python3 --version, and then # pip3.8 install mysql-connector-python

"""
    Database attribute (column) with instance variables showing column name, 
    data type, if there are any nulls in the column, and the key (prime attribute
    or not)
"""
class Attribute:
    
    def __init__(self, name, dt, null, k):
        self.name=name
        self.dataType=dt.decode()
        self.null=null
        self.key=k
        self.numeric = self.isNumeric(self)
    
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
        
        return isNum;



""" 
    Database relation (table), with instance variables showing the name 
    of the relation, and an array containing all the attributes stored in 
    the relation.
"""
class Relation:
    
    def __init__(self, n):
        self.name = n
        self.attributes=[]
        self.numericAttributes=[]
    
    
    def addAttribute(self, attribute):
        self.attributes.append(attribute)
        # If attribute is numeric, add to numericAttributes array
        if (attribute.numeric):
            self.numericAttributes.append(attribute)
    
    
    # Returns the number of numeric attributes in the relation
    def numNumeric(self):
        return len(self.numericAttributes)>0

        
    def getAttribute(self, i):
        # check that the attribute number asked for is not out of bounds
        if (i<len(self.attributes)):
            return self.attributes[i]
        else:
            return 0
        
    def getNumAttributes(self):
        return len(self.attributes)




""" 
    Database
"""
class Database:
    
    def __init__(self, host='localhost', user='root', pword='mySQL_sew1', db_name = 'classicmodels2022'):
        
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
            
            r = Relation(table[0])       # Create a relation for each table name
            self.relations.append(r)     # store created relation in relations[]
            
            cursor.execute("SHOW COLUMNS FROM "+r.name+" ;") # get column details for relation r
            columns = cursor.fetchall()
            
            #create each attribute object for relation r
            for column in columns:
                r.addAttribute(Attribute(column[0], column[1], column[2], column[3]))
            
            # if relation r contains at least 1 numeric attribute, add it to numericRelations array
            if (r.numNumeric() > 0):
                self.numericRelations.append(r)
        
    
    def numRelations(self):
        return len(self.relations)
    
    def numNumericRelations(self):
        return len(self.numericRelations)
       
    def getRelation(self, i):
        return self.relations[i]
    
    def getNumericRelation(self, i):
        return self.numericRelations[i]
    
    
    





# testing (delete me)
new = Database(db_name='classicmodels2022')
#print(new.numRelations())
#dataType = new.getRelation(1).getAttribute(0).getDataType()
#dataType = dataType.split(" ")
#print(dataType[0])
#if " " in dataType:
#    print(dataType)