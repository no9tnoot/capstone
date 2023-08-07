# Molly Ryan
# 7 August 2023
# Database Class

from array import *

import mysql.connector 

class Database:
    
    def __init__(self):
        # get the attributes and their types from SQL, as well as the relations
        self.attributes = [['att1','datatype'],['att2','datatype']]
        self.relations = ['relation1', 'relation2']
    
    def numAttributes(self):
        return len(self.attributes)
    
    def numRelations(self):
        return len(self.relations)
       
    def getAttribute(self, i):
        return self.attributes[i]
    
    def getRelation(self, i):
        return self.relations[i]
    
    