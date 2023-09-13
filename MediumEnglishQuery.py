# Molly Ryan, Peter Berens, Sian Wood
# 9 September 2023
# MediumEnglishQuery

from IEnglishQuery import IEnglishQuery

class MediumEnglishQuery(IEnglishQuery):

    likePos = ['second','third','fourth','fifth','sixth']

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

    def englishToString(self, english):
        return super().englishToString(english)
    
    def getEnglishQuery(self):
        return super().getEnglishQuery()
    
    def translateAgg(self, agg):
        return super().translateAgg(agg)
    
    def translateOperator(self, condition):
        return super().translateOperator(condition)
    
    def translateAttr(self, attr):
        return super().translateAttr(attr)
    
    def translateCond(self, condition):
        return super().translateCond(condition)
    
    def translateLike(self, like):
        return super().translateLike(like)
    
    def attrsAndAggs(self, attrs, agg):
        return super().attrsAndAggs(attrs, agg)
    
    def onlyAttrs(self, attrs):
        return super().onlyAttrs(attrs)
    
    def translateVal2(self, condition):
        return super().translateVal2(condition)


    #show (function) as (asName)
    #e.g.: show price * 0.152 as VAT
