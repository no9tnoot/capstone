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
        q = self.translateAgg(query['aggregates'][0]) + ' ' + self.translateAttr(query['attributes'][0])
        
        match query['relation']['joinType']:
            case 'left outer join':
                #agg and attr
                q = self.translateAgg(query['aggregates'][0]) + ' ' + self.translateAttr(query['attributes'][0])
                #first relation
                q += ' in the ' + query['relation']['rel1'].name + ' table'
                q += ' along with the ' + self.translateAttr(query['attributes'][1]) + ' values in the ' + query['relation']['rel2'] + ' table that have a corresponding ' + query['relation']['attr'] + ' value'
            case 'right outer join':
                q = self.translateAgg(query['aggregates'][0]) + ' ' + self.translateAttr(query['attributes'][1])
                
                q += ' in the ' + query['relation']['rel2'].name + ' table'
                q += ' along with the ' + self.translateAttr(query['attributes'][0]) + ' values in the ' + query['relation']['rel1'] + ' table that have a corresponding ' + query['relation']['attr'] + ' value'
            case 'inner join':
                q = self.translateAgg(query['aggregates'][0]) + ' ' + self.translateAttr(query['attributes'][0])
                q += ' in the ' + query['relation']['rel1'].name + ' table'
                q += ' and in the ' + query['relation']['rel2'] + ' table where they have a matching value of ' + query['relation']['attr']
                
            case 'natural inner join':
                q = self.translateAgg(query['aggregates'][0]) + ' ' + self.translateAttr(query['attributes'][0])
                q += ' in the ' + query['relation']['rel1'].name + ' table'
                q += ' and the associated values of ' + self.translateAttr(query['attributes'][1]) + 'in the ' + query['relation']['rel2'] + ' table'
                
     

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