# Molly Ryan
# 11 August 2023
# Marker Class

import mysql.connector

import Database

class Marker:
    
    def __init__(self,db):
        self.database = db
    
    
    # issue: doesn't check the order (e.g. if it is ascending)
    def markQuery(self, studentQuery, modalAnswer):
        database = mysql.connector.connect(
            host=self.database.host,
            user=self.database.user,
            password=self.database.pword,
            database=self.database.db_name
        )
        
        cursor = database.cursor()  # Create a cursor to interact with the database
        
        instruction = "( SELECT * FROM (" + studentQuery + ") EXCEPT SELECT * FROM (" + modalAnswer + ") ) UNION ALL ( SELECT * FROM (" + studentQuery + ") EXCEPT SELECT * FROM (" + modalAnswer +") )"
        
        print(instruction)
        #cursor.execute(instruction)   # SQL: print the table names             
        #result = cursor.fetchall()       # get the output table names from SQL
        
        #print(result)

db = Database.Database(db_name='classicmodels2022')
marker = Marker(db)
q1 = "SELECT * FROM CUSTOMERS"
q2 = q1
marker.markQuery(q1, q2)