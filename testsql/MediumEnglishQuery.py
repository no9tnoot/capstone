# Molly Ryan, Peter Berens, Sian Wood
# 9 September 2023
# MediumEnglishQuery

from .IEnglishQuery import IEnglishQuery

class MediumEnglishQuery(IEnglishQuery):

    def __init__(self, sqlQuery):
        super().__init__(sqlQuery)
        self.englishQuery = 'Show '

        if sqlQuery['aggregates']:
            self.englishQuery += self.attrsAndAggs(sqlQuery['attributes'][0], sqlQuery['aggregates'][0], sqlQuery['roundTo'][1:])
        else:
            self.englishQuery += 'the values of ' + self.onlyAttrs(sqlQuery['attributes'])

        self.englishQuery += ' in the ' + sqlQuery['relation']['rel1'].name + ' table'

        if sqlQuery['condition']:
            self.englishQuery += self.translateCond(sqlQuery['condition'])

        #handles distinct queries
        if sqlQuery['distinct']:
            if len(sqlQuery['attributes']) == 1:
                self.englishQuery += ' but only for unique values of ' + self.onlyAttrs(sqlQuery['attributes'])
            else:
                self.englishQuery += ' but only for unique combinations of ' + self.onlyAttrs(sqlQuery['attributes'])

        self.englishQuery += '.'

    def translateRound(self, roundTo):
        """
        Translate round functions to english
        """
        if roundTo == '1':
            s = ' rounded to ' + roundTo + ' decimal place'
        else:
            s = ' rounded to ' + roundTo + ' decimal places'
        return s

    def englishToString(self, english):
        return super().englishToString(english)
    
    def easyEnglish(self, sqlQuery):
        return super().easyEnglish(sqlQuery)
    
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
    
    def attrsAndAggs(self, attrs, agg, roundTo):
        """
        Overriding attrsAndAggs to deal with round aggs
        """
        if agg != 'round(':
            engAttrs = self.translateAgg(agg)
            engAttrs += self.translateAttr(attrs)
        else:
            engAttrs = self.translateAgg('')
            engAttrs += self.translateAttr(attrs)
            engAttrs += self.translateRound(roundTo)
        return engAttrs
    
    def onlyAttrs(self, attrs):
        return super().onlyAttrs(attrs)
    
    def translateVal2(self, condition, nested=False):
        return super().translateVal2(condition, nested)


    #show (function) as (asName)
    #e.g.: show price * 0.152 as VAT
