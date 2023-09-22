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
    
    def __init__(self, name, dt='', null='', k='', groupBy = False):
        self.name=name
        if not isinstance(dt, str):
            dt=dt.decode()
        self.dataType=dt
        self.null=null
        self.key=k
        self.numeric = Attribute.isNumeric(self)
        self.roundable = Attribute.isRoundable(self)
        self.string = Attribute.isString(self)
        self.groupBy = groupBy
    
    def isPrimary(self):
        return (self.key == 'PRI')

    """
        Sets numeric to True if the attribute is numeric (not a string/date/time/boolean)
    """
    def isNumeric(self):
        
        isNum = False
        
        numDataType = ['bit', 'int', 'float', 'double', 'dec']
        
        # search to see if the dataType contains one of the above strings - indicating numeric attribute
        for dt in numDataType:
            if dt in self.dataType.lower():  # set the dataType to lower case to include all string cases in search
                isNum = True
        
        return isNum
    
    """
        Sets string to True if the attribute is string (not a numeric/date/time/boolean)
    """
    def isString(self):
        
        isString = False
        
        stringDataType = ['char', 'varchar', 'text', 'tinytext', 'mediumtext', 'longtext']
        
        # search to see if the dataType contains one of the above strings - indicating numeric attribute
        for dt in stringDataType:
            if dt in self.dataType.lower():  # set the dataType to lower case to include all string cases in search
                isString = True
        
        return isString
    
    """
        Sets numeric to True if the attribute is numeric (not a string/date/time/boolean)
    """
    def isRoundable(self):
        
        isRoundable = False
        
        roundableDataType = ['float', 'double']
        
        # search to see if the dataType contains one of the above strings - indicating numeric attribute
        for dt in roundableDataType:
            if dt in self.dataType.lower():  # set the dataType to lower case to include all string cases in search
                isRoundable = True
        
        return isRoundable
    
    """
        Returns true if the calling attribute is equal to the given attribute
    """
    def isEqual(self, attribute):
        if self.name != attribute.name: return False
        if self.dataType != attribute.dataType: return False
        if self.null != attribute.null: return False
        return True
        
    



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
        self.groupByAttributes = []
    
    """
        Adds the given attribute object to the appropriate array instance variables
    """
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
    
    """
        Returns True if the relation has numeric attributes
    """
    def hasNumeric(self):
        return len(self.numericAttributes)>0
    
    """
        Returns True if the relation has string attributes
    """
    def hasString(self):
        return len(self.stringAttributes)>0
    
    """
        Returns True if the relation has numeric attributes
    """
    def hasRoundable(self):
        return len(self.roundableAttributes)>0

    """
        Returns a random attribute that meets the set requirements (i.e. numeric, string, and roundable
        requirements). If a requirement is set to False, this means it is not required, not that it is 
        not acceptable. i.e. numeric=False can still return a numeric attribute
    """  
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
    
    
    
    """
        Finds the attribute with the given name in self.attributes. Returns None if no
        matching attribute found.
    """
    def getAttributeWithName(self, name):
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute
        return None
    
    """
        Returns the number of attributes in the relation.
    """
    def getNumAttributes(self):
        return len(self.attributes)
    
    """
        Returns the number of rows (entries) in the relation.
    """
    def getNumRows(self):
        return self.numRows
    
    """
        Returns True if the passed attribute exists in this relation, and False otherwise.
    """
    def hasAttribute(self, attribute):
        for att in self.attributes:
            if att.isEqual(attribute): return True
        return False
        
    """
        Returns an array of attributes that are in both this relation and the passed relation.
    """
    def getJoinAttributes(self, otherRelation):
        joinAttributes = []
        primary = False
        # go through every attribute in the given relation
        for otherAttribute in otherRelation.attributes:
            primary = otherAttribute.isPrimary() # check if the attribute is a primary attribute in the other relation
            if self.hasAttribute(otherAttribute):
                if not primary: 
                    primary = self.getAttributeWithName(otherAttribute.name).isPrimary() # check if the attribute is primary in this relation
                # if primary in at least one of the relations, append to joinAttributes
                if primary: joinAttributes.append(otherAttribute)
                
        return joinAttributes
    
    """
        Adds attributes that can be used to group by to the groupByAttributes array
    """
    def getGroupByAttributes(self):
        for attribute in self.attributes:
            if attribute.groupBy:
                self.groupByAttributes.append(attribute)
    
    """
        Returns True if the relation has any attributes that can be used to group by 
    """    
    def hasGroupByAttributes(self):
        self.getGroupByAttributes()
        return len(self.groupByAttributes)>0




"""
    Database (table) object, with an array of relations, as well as arrays for special types of relations 
    (e.g ones that contain numeric attribute(s)). Takes the SQL database information and creates the connection
    to the mySQL server, getting the relevant relations and attribute information therefrom.
"""
class Database:
    
    def __init__(self, host, user, pword, db_name):
        
        self.relations = []  # initialise empty array of relations
        self.numericRelations = [] # initialise empty array of relations that contain at least 1 numeric attribute
        self.host = host
        self.user = user
        self.pword = pword
        self.db_name = db_name
        self.groupByRelations = []
        self.joinRelations = []
        self.loadRelations() # load the relations in from the server
        self.getJoinRelations() 
        self.getGroupByRelations() 
            
        
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
                groupBy = False
                # if doesn't have null
                if column[2]=='NO':
                    # find out if attribute can be used for grouping
                    cursor.execute("SELECT COUNT(DISTINCT "+column[0]+") / COUNT(*) FROM "+r.name)
                    proportionDistinct = cursor.fetchall()
                    proportionDistinct = proportionDistinct[0][0]
                    if proportionDistinct < 0.5: groupBy = True # if at most 80% of the values are unique, can use for grouping
                r.addAttribute(Attribute(column[0], column[1], column[2], column[3], groupBy = groupBy))
            
            # if relation r contains at least 1 numeric attribute, add it to numericRelations array
            if (r.hasNumeric() > 0):
                self.numericRelations.append(r)
    
    """
        Returns the number of relations in the database.
    """
    def numRelations(self):
        return len(self.relations)
    
    """
        Returns the ith relation from the database
    """
    def getRelation(self, i):
        return self.relations[i]
    
    """
        Returns the ith numeric relation from the database
    """
    def getNumericRelation(self, i):
        return self.numericRelations[i]
    
    """
        Find relations that can be joined and store them in an array
    """
    def getJoinRelations(self):
        
        # For each relation pair
        for i in range(len(self.relations)):
            for j in range(i+1, len(self.relations)):
                rel1=self.relations[i]
                rel2=self.relations[j]
                joinAttributes = rel1.getJoinAttributes(rel2)
                if len(joinAttributes)>0:
                    joinDict = dict(rel1=rel1, rel2=rel2, joinAttributes=joinAttributes)
                    self.joinRelations.append(joinDict)
                    

    """
        Find relations that have attributes that can be used to group by and store them in an array
    """
    def getGroupByRelations(self):
        for relation in self.relations:
            if relation.hasGroupByAttributes():
                self.groupByRelations.append(relation)
    
    """
        Return a random (not null) value from an attribute from the database.
    """           
    def selectAttrVal(self, relation, attribute):
        
        # Connect to database
        database = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.pword,
            database=self.db_name
        )
        
        cursor = database.cursor()  # Create a cursor to interact with the database
        
        reqVal = str( random.randint(0, relation.getNumRows()-1) ) #Select a random value between 0 and the total number of values in the attribute -1

        cursor.execute("SELECT " + attribute.name + " FROM " + relation.name + " limit 1 offset " + reqVal + ";")   # SQL: print a single value at index reqVal from the attribute
        
        reqVal = cursor.fetchall()[0][0] # get the value from the SQL output
        
        if reqVal is None: return self.selectAttrVal(relation, attribute) # recurse until a non null value is selected
        else: return reqVal # if the value isn't a null value
        
    """
        Returns the counts that a 'group by' query will produce. These can be used to construct 
        a 'having by' condition
    """
    def selectHavingVals(self, query):
            
        # Connect to database
        database = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.pword,
            database=self.db_name
        )
        
        cursor = database.cursor()  # Create a cursor to interact with the database
        cursor.execute(query)
        return cursor.fetchall()
           
            
