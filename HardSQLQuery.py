# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

import ISQLQuery
import random

class HardSQLQuery(ISQLQuery):
    
    
    def __init__(self):
        super.__init__(self)
        #names for AS aggregates
        self.asNames = []
    
    
    """
        relation/s to query form. including joins
    """
    def queryRels(rel1, rel2, join):
        if rel2 == '':
            return rel1
        else:
            return rel1 + join + rel2
        
    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns, self.asNames)
        q += 'FROM' + self.queryRels(self.rels[0], self.rels[1], self.rels[2])
        q += self.formatQueryConds(self.conds)
        return q