# Molly Ryan, Peter Berens, Sian Wood
# 15 September 2023
# HardEnglishQuery

from IEnglishQuery import IEnglishQuery

class HardEnglishQuery(IEnglishQuery):

    def __init__(self, sqlQuery):
        super().__init__(sqlQuery)
        self.englishQuery = 'Show '
        self.englishQuery += self.nested(sqlQuery)
        self.englishQuery += '.'

    def nested(self, query):
        q = self.easyEnglish(query)
        return q
    
    def join(self, query):
        q = self.easyEnglish(query)
        match query['rels']['joinType']:
            case 'left outer join':
                q += ' along with the ' + query['rels']['rels2'] + ' records with the associated ' + query['rels']['attr']
            case 'right outer join':
                q += ' along with the ' + query['rels']['rels1'] + ' records with the associated ' + query['rels']['attr']
            
    
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
    
    def translateCond(self, condition, nested=False):
        return super().translateCond(condition, nested)
    
    def translateLike(self, like):
        return super().translateLike(like)
    
    def translateVal2(self, condition, nested=False):
        return super().translateVal2(condition, nested)
    
    def onlyAttrs(self, attrs):
        return super().onlyAttrs(attrs)
    
    def attrsAndAggs(self, attrs, agg):
        return super().attrsAndAggs(attrs, agg)
    
    def easyEnglish(self, sqlQuery):
        return super().easyEnglish(sqlQuery)