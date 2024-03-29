# Molly Ryan, Peter Berens, Sian Wood
# 9 September 2023
# MediumEnglishQuery

from .IEnglishQuery import IEnglishQuery

class MediumEnglishQuery(IEnglishQuery):
    """
    Handles slightly more complex mySQL queries including 'DISTINCT', 'ROUND', and various types of
    'LIKE' conditions. Implements the IEnglishQuery interface.
    """

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
    
    def easyEnglish(self, sqlQuery):
        return super().easyEnglish(sqlQuery)

    def translateAttr(self, attr):
        return super().translateAttr(attr)
    
    def translateAgg(self, agg):
        return super().translateAgg(agg)
    
    def translateRound(self, roundTo):
        """
        Translate round functions to english
        """
        if roundTo == '1':
            s = ' rounded to ' + roundTo + ' decimal place'
        else:
            s = ' rounded to ' + roundTo + ' decimal places'
        return s
    
    def translateCond(self, condition):
        return super().translateCond(condition)
    
    def translateLike(self, like):
        return super().translateLike(like)
    
    def translateOperator(self, condition):
        return super().translateOperator(condition)
    
    def translateVal2(self, condition, nested=False):
        return super().translateVal2(condition, nested)

    def onlyAttrs(self, attrs):
        return super().onlyAttrs(attrs)
    
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
    
    def getEnglishQuery(self):
        return super().getEnglishQuery()
