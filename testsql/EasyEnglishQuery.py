# Molly Ryan, Peter Berens, Sian Wood
# 3 September 2023
# EasyEnglishQuery

from .IEnglishQuery import IEnglishQuery

class EasyEnglishQuery(IEnglishQuery):

    def __init__(self, sqlQuery):
        super().__init__(sqlQuery)
        self.englishQuery = 'Show '
        self.englishQuery += self.easyEnglish(sqlQuery)
        self.englishQuery += '.'
        
    def easyEnglish(self, sqlQuery):
        return super().easyEnglish(sqlQuery)
    
    def translateAttr(self, attr):
        return super().translateAttr(attr)
    
    def translateAgg(self, agg):
        return super().translateAgg(agg)
    
    def translateCond(self, condition, nested=False):
        return super().translateCond(condition, nested)
    
    def translateLike(self, like):
        return super().translateLike(like)
    
    def translateOperator(self, condition):
        return super().translateOperator(condition)
    
    def translateVal2(self, condition, nested=False):
        return super().translateVal2(condition, nested)
    
    def onlyAttrs(self, attrs):
        return super().onlyAttrs(attrs)
    
    def attrsAndAggs(self, attrs, agg):
        return super().attrsAndAggs(attrs, agg)
    
    def getEnglishQuery(self):
        return super().getEnglishQuery()

