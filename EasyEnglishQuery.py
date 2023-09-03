# Molly Ryan, Peter Berens, Sian Wood
# 3 September 2023
# EasyEnglishQuery

import IEnglishQuery

class EasyEnglishQuery(IEnglishQuery):
    
    def __init__(self, sqlQuery):
        super().__init__(self, sqlQuery)
        englishQuery = 'Show '
        englishQuery += self.attrsAndAggs(sqlQuery['attributes'], sqlQuery['aggregates'])
        englishQuery += ' in the ' + sqlQuery['relation'] + ' table '
        englishQuery += self.translateCond(sqlQuery['condition'])

    def attrsAndAggs(self, attrs, agg):
        engAttrs = self.translateAgg(agg)
        engAttrs += self.translateAttr(attrs[0])
        if len(attrs) == 2:
            endAttrs += ' and ' + self.translateAttrs(attrs[1])
        return engAttrs
