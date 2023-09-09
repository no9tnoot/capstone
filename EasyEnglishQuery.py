# Molly Ryan, Peter Berens, Sian Wood
# 3 September 2023
# EasyEnglishQuery

from IEnglishQuery import IEnglishQuery

class EasyEnglishQuery(IEnglishQuery):
    
    def __init__(self, sqlQuery):
        super().__init__(self, sqlQuery)
        self.englishQuery = 'Show '
        self.englishQuery += self.attrsAndAggs(sqlQuery['attributes'], sqlQuery['aggregates'])
        self.englishQuery += ' in the ' + sqlQuery['relation'] + ' table '
        self.englishQuery += self.translateCond(sqlQuery['condition'])

    
    def attrsAndAggs(self, attrs, agg):
        engAttrs = self.translateAgg(agg)
        engAttrs += self.translateAttr(attrs[0])
        if len(attrs) == 2:
            endAttrs += ' and ' + self.translateAttrs(attrs[1])
        return engAttrs
    
test_dict = {'attributes': '*', 'aggregates': '', 'relation': 'offices'}
q = EasyEnglishQuery(test_dict)
print(q.getQuery())
