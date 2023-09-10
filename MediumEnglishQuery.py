# Molly Ryan, Peter Berens, Sian Wood
# 9 September 2023
# MediumEnglishQuery

import IEnglishQuery

class MediumEnglishQuery(IEnglishQuery):
    def __init__(self, sqlQuery):
        super().__init__(self, sqlQuery)
        self.englishQuery = 'Show '
        self.englishQuery += self.attrsAndAggs(sqlQuery['attributes'], sqlQuery['aggregates'])
        self.englishQuery += ' in the ' + sqlQuery['relation'] + ' table '
        self.englishQuery += self.translateCond(sqlQuery['condition'])

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
