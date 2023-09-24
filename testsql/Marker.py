# Molly Ryan
# 11 August 2023
# Marker Class

import mysql.connector
from .Results import Results

class Marker:
    """ Class that compares the equivalence of MySQL queries."""
    
    def __init__(self,db):
        self.database = db
    
    def markQuery(self, studentQuery, modelQuery):
        """
        Checks if the studentQuery returns the same output as the modelQuery. Returns an array,
        wherein the first item is a Boolean indicating True if the outputs are identical. If False,
        a second item in the array is a string communicating if the studentQuery is valid and produced
        an incorrect output, or if it is invalid and the server threw an error.
        """
        database = mysql.connector.connect(
            host=self.database.host,
            user=self.database.user,
            password=self.database.pword,
            database=self.database.db_name
        )
        
        cursor = database.cursor()  # Create a cursor to interact with the database
        
        try: # either the student and model outputs match, or there is a logic error 
            cursor.execute(studentQuery)
            studentResults = cursor.fetchall()
            validity = "log"
        except: # if the studentResults causes the server to throw an error
            studentResults = ""
            # There is a syntax error
            validity="syn"
        
        # Fetch output from modelQuery
        cursor.execute(modelQuery)
        modelResults = cursor.fetchall()

        # Fetch attribute names from modelQuery output
        headers = [tuple(i[0] for i in cursor.description)]
        
        # Create a Results object to store data from Marker
        return Results(studentResults==modelResults, validity, headers + modelResults)
