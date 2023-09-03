# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

import ISQLQuery
import random

class MediumSQLQuery(ISQLQuery):
    
    
    def __init__(self):
        super.__init__(self)
        self.asNames = [] #names for AS aggregates
    
    
    def toQuery(self):
        q = 'SELECT '
        q += self.queryAggs(self.attrs, self.aggFns, self.asNames)
        q += 'FROM' + self.queryRels(self.rels[0], self.rels[1], self.rels[2])
        q += self.queryConds(self.conds)
        return q