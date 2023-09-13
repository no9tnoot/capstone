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
    
    def __init__(self, sqlQuery):
        super().__init__(sqlQuery)
        self.englishQuery = 'Show '
        if sqlQuery['aggregates']:
            self.englishQuery += self.attrsAndAggs(sqlQuery['attributes'][0], sqlQuery['aggregates'][0])
        else:
            self.englishQuery += self.onlyAttrs(sqlQuery['attributes'])
        self.englishQuery += ' in the ' + sqlQuery['relation']['rel1'].name + ' table'
        if sqlQuery['condition']:
            self.englishQuery += self.translateCond(sqlQuery['condition'])
        self.englishQuery += '.'

    
    def attrsAndAggs(self, attrs, agg):
        engAttrs = self.translateAgg(agg)
        engAttrs += self.translateAttr(attrs)
        return engAttrs
    
    def onlyAttrs(self, attrs):
        engAttrs = self.translateAttr(attrs[0])
        if len(attrs) == 2:
            engAttrs += ' and ' + self.translateAttr(attrs[1])
        return engAttrs
    
# test_dict = {'attributes': ['customernumber', 'customername'], 'aggregates': '', 'relation': 'offices', 'condition': {'cond': 'limit', 'val2': 1}}
# q = EasyEnglishQuery(test_dict)
# print(q.getEnglishQuery())
