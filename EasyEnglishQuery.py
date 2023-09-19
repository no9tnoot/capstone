# Molly Ryan, Peter Berens, Sian Wood
# 3 September 2023
# EasyEnglishQuery

from IEnglishQuery import IEnglishQuery

class EasyEnglishQuery(IEnglishQuery):

    def englishToString(self, english):
        return super().englishToString(english)
    
    def getEnglishQuery(self):
        return super().getEnglishQuery()
    
    def translateAgg(self, agg):
        return super().translateAgg(agg)
    
    def translateAttr(self, attr):
        return super().translateAttr(attr)
    
    def translateCond(self, condition):
        return super().translateCond(condition)
    
    def getEnglishQuery(self):
        return super().getEnglishQuery()
    
    def translateOperator(self, condition):
        return super().translateOperator(condition)
    
    def translateLike(self, like):
        return super().translateLike(like)
    
    def translateVal2(self, condition, nested=False):
        return super().translateVal2(condition, nested)
    
    def easyEnglish(self, sqlQuery):
        return super().easyEnglish(sqlQuery)
    
    def __init__(self, sqlQuery):
        super().__init__(sqlQuery)
        self.englishQuery = 'Show '
        self.englishQuery += self.easyEnglish(sqlQuery)
        self.englishQuery += '.'

    def attrsAndAggs(self, attrs, agg):
        return super().attrsAndAggs(attrs, agg)
    
    def onlyAttrs(self, attrs):
        return super().onlyAttrs(attrs)
    
# test_dict = {'attributes': ['customernumber', 'customername'], 'aggregates': '', 'relation': 'offices', 'condition': {'cond': 'limit', 'val2': 1}}
# q = EasyEnglishQuery(test_dict)
# print(q.getEnglishQuery())
