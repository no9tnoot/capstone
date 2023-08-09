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
        self.dataType=dt
        self.null=null
        self.key=k
    
    def getName(self):
        return self.name
        
    def getDataType(self):
        return self.dataType
        



""" 
    Database relation (table), with instance variables showing the name 
    of the relation, and an array containing all the attributes stored in 
    the relation.
"""
class Relation:
    
    def __init__(self, n):
        self.name = n
        self.attributes=[]
    
    def addAttribute(self, attribute):
        self.attributes.append(attribute)
        
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
        self.loadRelations(db_name)
        
        
    """ Get the attributes and their types from SQL, as well as the relations"""
    def loadRelations(self, db_name):
        # connect to sql database
        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mySQL_sew1",
            database=db_name
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
        
    
    def numRelations(self):
        return len(self.relations)
       
    
    def getRelation(self, i):
        return self.relations[i]
    





# testing (delete me)
# new = Database()
# print(new.numRelations())
# print(new.getRelation(0).getAttribute(0).getDataType())