# Molly Ryan, Peter Berens, Sian Wood
# 15 September 2023
# HardEnglishQuery

from IEnglishQuery import IEnglishQuery

class HardEnglishQuery(IEnglishQuery):

    def __init__(self, sqlQuery):
        super().__init__(sqlQuery)
        self.englishQuery = 'Show '
        if sqlQuery['join']:
            self.englishQuery += self.join(sqlQuery)
        elif sqlQuery['nested']:
            self.englishQuery += self.nested(sqlQuery)
        elif sqlQuery['groupBy']:
            self.englishQuery += self.groupBy(sqlQuery)
        self.englishQuery += '.'

    def nested(self, query):
        q = self.easyEnglish(query)
        return q
    
    def groupBy(self, query):
        q = 'each ' + query['attributes'][1].name + ' in the ' + query['relation']['rel1'].name + ' table along with ' + self.translateAgg(query['aggregates'][0]) + self.translateAttr(query['attributes'][0]) + ' that is associated with that ' + query['attributes'][1].name
        if query['condition']:
            q += self.translateCond(query['condition'])
        if query['groupBy']['having']:
            q += ' but only for ' + self.translateAttr(query['attributes'][0]) + ' values that '
            q += self.having(query)
        return q
    
    def having(self, query):
        match query['aggregates'][0]:
            case 'count(':
                q = 'appear ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val']) + ' times'
            case 'max(':
                q = 'have a maximum value ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val'])
            case 'min(':
                q = 'have a minimum value ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val'])
            case 'avg(':
                q = 'have an average value ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val'])
            case 'sum(':
                q = 'have an additive total ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val'])
        return q

    def havingOperator(self, operator, count = False):
        match operator:
            case '=':
                return ' '
            case '<':
                return 'less than '
            case '>':
                return 'greater than '
            case '<=':
                return 'less than or equal to '
            case '>=':
                return 'greater than or equal to '
            case _:
                return ''
    
    def join(self, query):
        
        match query['relation']['joinType']:
            case 'left outer join':
                #agg and attr
                #q = self.translateAgg(query['aggregates'][0]) + self.translateAttr(query['attributes'][0])
                q = self.joinPart1(query['aggregates'], query['attributes'], query['relation'], 0)
                #first relation
                #q += ' in the ' + query['relation']['rel1'].name + ' table'
                #second attribute and relation
                #q += ' along with the ' + self.translateAttr(query['attributes'][1]) + ' values in the ' + query['relation']['rel2'].name + ' table that have a corresponding ' + query['relation']['attr'].name + ' value'
            
            case 'right outer join':
                q = self.joinPart1(query['aggregates'], query['attributes'], query['relation'], 1)
                #q += ' along with the ' + self.translateAttr(query['attributes'][0]) + ' values in the ' + query['relation']['rel1'].name + ' table that have a corresponding ' + query['relation']['attr'].name + ' value'
            
            case 'inner join':
                q = self.joinPart1(query['aggregates'], query['attributes'], query['relation'], 0)
                #q += ' and the values of ' + self.translateAttr(query['attributes'][1]) +' in the ' + query['relation']['rel2'].name + ' table where they have a matching value of ' + query['relation']['attr'].name
                
            case 'natural inner join':
                q = self.joinPart1(query['aggregates'], query['attributes'], query['relation'], 0)
                #q += ' and the associated values of ' + self.translateAttr(query['attributes'][1]) + ' in the ' + query['relation']['rel2'].name + ' table'
        q += self.joinPart2(query['aggregates'], query['attributes'], query['relation'])
        return q
    
    def joinPart1(self, aggs, attrs, rels, right = 0):
        
        if not right:
            if aggs:
                q= self.translateAgg(aggs[0]) + self.translateAttr(attrs[right])
            else:
                q= self.translateAgg('') + self.translateAttr(attrs[right])
            q += ' in the ' + rels['rel1'].name + ' table'
        else:
            if attrs[0].name == '*':
                if aggs:
                    q= self.translateAgg(aggs[0]) + self.translateAttr(attrs[0])
                else:
                    q= self.translateAgg('') + self.translateAttr(attrs[0])
            else:
                q= self.translateAgg('') + self.translateAttr(attrs[right])
            q += ' in the ' + rels['rel2'].name + ' table'
        return q
    
    def joinPart2(self, aggs, attrs, rels):
        if attrs[0].name == '*':
            match rels['joinType']:
                case 'left outer join':
                    q = ' and in the ' + rels['rel2'].name + ' table where it has a corresponding' + rels['attr'].name + ' value'
                case 'inner join':
                    q = ' and in the ' + rels['rel2'].name + ' table where they have a matching ' + rels['attr'].name + ' value'
                case 'natural inner join':
                    q = ' where they are associated with a record in the ' + rels['rel2'].name + ' table'
                case 'right outer join':
                    q = ' and in the ' + rels['rel1'].name + ' table where it has a corresponding' + rels['attr'].name + ' value'
        else:
            match rels['joinType']:
                case 'left outer join':
                    q = ' along with the ' + self.translateAttr(attrs[1]) + ' values in the ' + rels['rel2'].name + ' table that have a corresponding ' + rels['attr'].name + ' value'
                case 'inner join':
                    q = ' and the values of ' + self.translateAttr(attrs[1]) +' in the ' + rels['rel2'].name + ' table where they have a matching ' + rels['attr'].name + ' value'
                case 'natural inner join':
                    q = ' and the associated values of ' + self.translateAttr(attrs[1]) + ' in the ' + rels['rel2'].name + ' table'
                case 'right outer join':
                    if aggs:
                        q = ' along with ' + self.translateAgg(aggs[0]) + 'the ' + self.translateAttr(attrs[0]) + ' values in the ' + rels['rel1'].name + ' table that have a corresponding ' + rels['attr'].name + ' value'
                    else:
                        q = ' along with ' + self.translateAgg('') + self.translateAttr(attrs[0]) + ' in the ' + rels['rel1'].name + ' table that have a corresponding ' + rels['attr'].name + ' value'
        return q

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