# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

import ISQLQuery
import random

class HardSQLQuery(ISQLQuery):
    
    
    
    """
        relation/s to query form. including joins
    """
    def queryRels(rel1, rel2, join):
        if rel2 == '':
            return rel1
        else:
            return rel1 + join + rel2