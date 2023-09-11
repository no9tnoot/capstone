# Molly Ryan, Peter Berens, Sian Wood
# 9 September 2023
# MediumEnglishQuery

import IEnglishQuery

class MediumEnglishQuery(IEnglishQuery):
    def __init__(self, sqlQuery):
        super().__init__(self, sqlQuery)
        self.englishQuery = 'Show '
        if sqlQuery['aggregates']:
            self.englishQuery += self.attrsAndAggs(sqlQuery['attributes'][0], sqlQuery['aggregates'][0])
        else:
            self.englishQuery += self.onlyAttrs(sqlQuery['attributes'])
        self.englishQuery += ' in the ' + sqlQuery['relation']['rel1'].name + ' table'
        if sqlQuery['condition']:
            self.englishQuery += self.translateCond(sqlQuery['condition'])
        self.englishQuery += '.'

    #show (function) as (asName)
    #e.g.: show price * 0.152 as VAT

    def like(self, pattern):
        pattern = [char for char in pattern]
        if (pattern[0] == '%'):
            pos = 'at the end of the string'
        elif (pattern[len(pattern) == '%']):
            pos = 'at the beginning of the string'
        elif (pattern[0] == '%') and (pattern[len(pattern) == '%']):
            pos = 'somewhere in the string'
