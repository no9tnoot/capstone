# Molly Ryan
# 11 August 2023
# Marker Class

import mysql.connector

import Database

class Marker:
    
    def __init__(self,db):
        self.database = db
    
    
    # issue: doesn't check the order (e.g. if it is ascending)
    def markQuery(self, studentQuery, modalQuery):
        database = mysql.connector.connect(
            host=self.database.host,
            user=self.database.user,
            password=self.database.pword,
            database=self.database.db_name
        )
        
        cursor = database.cursor()  # Create a cursor to interact with the database
        
        studentQuery = self.removeSemiColon(studentQuery)
        modalQuery = self.removeSemiColon(modalQuery)
        
        #instruction = "(SELECT * FROM (" + studentQuery + ") AS Q1 MINUS (" + modalAnswer + ") ) UNION ALL ( SELECT * FROM (" + modalAnswer + ") AS Q2 WHERE NOT EXISTS (" + studentQuery +") );"
        
        #print(instruction)
        #cursor.execute(instruction)   # SQL: print the table names             
        #result = cursor.fetchall()       # get the output table names from SQL
        
        #print(result)
        
        """The below is a place holder for until i figure out stupid mysql which can't do MINUS or 
        EXCEPT and cries if you put more than one column in a nested table and needs you to name every 
        derived table and everyone on the internet has differently complicated ideas that don't work"""
        
        cursor.execute(studentQuery)
        studentAnswer = cursor.fetchall()
        
        cursor.execute(modalQuery)
        modalAnswer = cursor.fetchall()
        
        if (studentAnswer==modalAnswer):
            return True
        
        return False
        

    """
    Remove the semi-colon from the end of the entered query if it has one.
    This is to prevent problems with the marker syntax.
    """
    def removeSemiColon(self, query):
        if query.endswith(';'):  # if it ends with a semi-colon, remove it
            return query.rstrip(';') # 
        return query # if it doesn't end with a semi-colon, just return the query



db = Database.Database(db_name='classicmodels2022')
marker = Marker(db)
q1 = "SELECT * FROM CUSTOMERS"
q2 = "SELECT * FROM CUSTOMERS WHERE CONTACTLASTNAME = 'SCHMITT';"
print(marker.markQuery(q1, q2))