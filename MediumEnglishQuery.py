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

