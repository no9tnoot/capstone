# Molly Ryan
# 7 August 2023
# Database Class

from array import *
import random

import mysql.connector

class Attribute:
    """
    Database attribute (column) with instance variables showing column name, 
    data type, if there are any nulls in the column, and the key (whether it is
    a prime attribute or not).
    """
    
    def __init__(self, name, dt='', null='', k='', groupBy = False):
        """
        Sets the instance variables of the Attribute.
        """
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
        """
        Returns true if the attribute is the primary key of the relation it is in.
        """
        return (self.key == 'PRI')

    def isNumeric(self):
        """
        Sets numeric instance variable to True if the attribute is numeric (not a string/date/time/boolean)
        """
        
        isNum = False
        
        numDataType = ['bit', 'int', 'float', 'double', 'dec']
        
        # search to see if the dataType contains one of the above strings - indicating numeric attribute
        for dt in numDataType:
            if dt in self.dataType.lower():  # set the dataType to lower case to include all string cases in search
                isNum = True
        
        return isNum
    
    def isString(self):
        """
        Sets string to True if the attribute is string (not a numeric/date/time/boolean)
        """
        
        isString = False
        
        stringDataType = ['char', 'varchar', 'text', 'tinytext', 'mediumtext', 'longtext']
        
        # search to see if the dataType contains one of the above strings - indicating numeric attribute
        for dt in stringDataType:
            if dt in self.dataType.lower():  # set the dataType to lower case to include all string cases in search
                isString = True
        
        return isString
    
    def isRoundable(self):
        """
        Sets numeric to True if the attribute is numeric (not a string/date/time/boolean)
        """
        
        isRoundable = False
        
        roundableDataType = ['float', 'double']
        
        # search to see if the dataType contains one of the above strings - indicating numeric attribute
        for dt in roundableDataType:
            if dt in self.dataType.lower():  # set the dataType to lower case to include all string cases in search
                isRoundable = True
        
        return isRoundable
    
    def isEqual(self, attribute):
        """
        Returns true if the calling attribute is equal to the given attribute
        """
        if self.name != attribute.name: return False
        if self.dataType != attribute.dataType: return False
        if self.null != attribute.null: return False
        return True
        
    



class Relation:
    """ 
    Database relation (table), with instance variables showing the name 
    of the relation, and an array containing all the attributes stored in 
    the relation.
    """
    
    def __init__(self, n, nrow):
        """
        Initialises the instance variables of the Relation.
        """
        self.name = n
        self.attributes=[]
        self.numericAttributes=[]
        self.stringAttributes=[]
        self.roundableAttributes=[]
        self.numRows = nrow
        self.groupByAttributes = []
    
    def addAttribute(self, attribute):
        """
        Adds the given attribute object to the appropriate array instance variables
        """
        self.attributes.append(attribute)
        # If attribute is numeric, add to numericAttributes array
        if (attribute.numeric):
            self.numericAttributes.append(attribute)
            if (attribute.roundable):
                self.roundableAttributes.append(attribute)
        # If attribute is string, add to stringAttributes array
        if (attribute.string):
            self.stringAttributes.append(attribute)
    
    def hasNumeric(self):
        """
        Returns True if the relation has numeric attributes
        """
        return len(self.numericAttributes)>0
    
    def hasString(self):
        """
        Returns True if the relation has string attributes
        """
        return len(self.stringAttributes)>0
    
    def hasRoundable(self):
        """
        Returns True if the relation has numeric attributes
        """
        return len(self.roundableAttributes)>0

    def getAttribute(self, numeric = False, string = False, roundable = False):
        """
        Returns a random attribute that meets the set requirements (i.e. numeric, string, and roundable
        requirements). If a requirement is set to False, this means it is not required, not that it is 
        not acceptable. i.e. numeric=False can still return a numeric attribute
        """  
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
    
    
    
    def getAttributeWithName(self, name):
        """
        Finds the attribute with the given name in self.attributes. Returns None if no
        matching attribute found.
        """
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute
        return None
    
    def getNumAttributes(self):
        """
        Returns the number of attributes in the relation.
        """
        return len(self.attributes)
    
    def getNumRows(self):
        """
        Returns the number of rows (entries) in the relation.
        """
        return self.numRows
    
    def hasAttribute(self, attribute):
        """
        Returns True if the passed attribute exists in this relation, and False otherwise.
        """
        for att in self.attributes:
            if att.isEqual(attribute): return True
        return False
        
    def getJoinAttributes(self, otherRelation):
        """
        Returns an array of attributes that are in both this relation and the passed relation.
        """
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
    
    def getGroupByAttributes(self):
        """
        Adds attributes that can be used to group by to the groupByAttributes array
        """
        for attribute in self.attributes:
            if attribute.groupBy:
                self.groupByAttributes.append(attribute)
    
    def hasGroupByAttributes(self):
        """
        Returns True if the relation has any attributes that can be used to group by 
        """    
        self.getGroupByAttributes()
        return len(self.groupByAttributes)>0




class Database:
    """
    Database (table) object, with an array of relations, as well as arrays for special types of relations 
    (e.g ones that contain numeric attribute(s)). Takes the SQL database information and creates the connection
    to the mySQL server, getting the relevant relations and attribute information therefrom.
    """
    def __init__(self, host, user, pword, db_name):
        """
        Initialises the instance variables of the Database, and loads the relations and 
        attributes into these instance arrays.
        """
        
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
            
        
    def loadRelations(self):
        """ Get the attributes and their types from SQL, as well as the relations"""
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
    
    def numRelations(self):
        """
        Returns the number of relations in the database.
        """
        return len(self.relations)
    
    def getRelation(self, i):
        """
        Returns the ith relation from the database
        """
        return self.relations[i]
    
    def getNumericRelation(self, i):
        """
        Returns the ith numeric relation from the database
        """
        return self.numericRelations[i]
    
    def getJoinRelations(self):
        """
        Find relations that can be joined and store them in an array
        """    
        # For each relation pair
        for i in range(len(self.relations)):
            for j in range(i+1, len(self.relations)):
                rel1=self.relations[i]
                rel2=self.relations[j]
                joinAttributes = rel1.getJoinAttributes(rel2)
                if len(joinAttributes)>0:
                    joinDict = dict(rel1=rel1, rel2=rel2, joinAttributes=joinAttributes)
                    self.joinRelations.append(joinDict)
                    

    def getGroupByRelations(self):
        """
        Find relations that have attributes that can be used to group by and store them in an array
        """
        for relation in self.relations:
            if relation.hasGroupByAttributes():
                self.groupByRelations.append(relation)
    
    def selectAttrVal(self, relation, attribute):
        """
        Return a random (not null) value from an attribute from the database.
        """               
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
        
    def selectHavingVals(self, query):
        """
        Returns the counts that a 'group by' query will produce. These can be used to construct 
        a 'having by' condition
        """    
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
           
            
