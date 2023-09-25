# Peter Berens
# 9 August 2023
# Session Class

from . import Database
#from . import Question
from . import Marker

class Session:
    """
    Session is responsible for creating the Database and Marker instances that will be used by other classes.
    """

    def __init__(self):
        self.details = []
        Session.readDatabaseDetails(self)

        #load database with details read from file
        self.database = Session.loadDatabase(self.details[0],self.details[1],self.details[2],self.details[3])
        self.marker = Marker.Marker(self.database)
    
    def loadDatabase(host='localhost', user='student', pword='password', db_name = 'classicmodels2022'):
        """
        Create a static instance of a Database object with the given / default paramaters
        """
        return Database.Database(host, user, pword, db_name)
    
    def markQuery(self, stuAns,  modalAns):
        """
        Mark a query to see if the student's entered query is equivalent to the expected model query.
        """
        return self.marker.markQuery(stuAns, modalAns)
    
    def readDatabaseDetails(self):
        """
        Reads line by line from the database details file in order: 
        host, user, password, database name
        """
        f = open('docs/database_details.txt','r')
        for x in f:
            self.details.append(x.strip())
