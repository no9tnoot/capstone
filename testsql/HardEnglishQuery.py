# Molly Ryan, Peter Berens, Sian Wood
# 15 September 2023
# HardEnglishQuery

from .IEnglishQuery import IEnglishQuery

class HardEnglishQuery(IEnglishQuery):
    """
    Handles complicated mySQL queries including nested queries, 'JOIN', and 'GROUP BY'/'HAVING'. 
    Implements the IEnglishQuery interface.
    """

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

    def easyEnglish(self, sqlQuery):
        return super().easyEnglish(sqlQuery)
    
    def nested(self, query):
        """
        Calls the easyEnglish method to generate a query, but also passes it a nested query.
        """
        q = self.easyEnglish(query)
        return q
    
    def translateAttr(self, attr):
        return super().translateAttr(attr)
    
    def translateAgg(self, agg):
        return super().translateAgg(agg)
    
    def translateCond(self, condition, nested=False):
        return super().translateCond(condition, nested)
    
    def translateLike(self, like):
        return super().translateLike(like)
    
    def translateOperator(self, condition):
        return super().translateOperator(condition)
    
    def translateVal2(self, condition, nested=False):
        return super().translateVal2(condition, nested)
    
    def onlyAttrs(self, attrs):
        return super().onlyAttrs(attrs)
    
    def attrsAndAggs(self, attrs, agg):
        return super().attrsAndAggs(attrs, agg)
    
    def groupBy(self, query):
        """
        Translates group by queries into english.
        """

        q = self.translateAgg(query['aggregates'][0]) + self.translateAttr(query['attributes'][0])
        q += ' associated with each ' + query['attributes'][1].name + ' in the ' + query['relation']['rel1'].name + ' table'

        if query['condition'] and query['groupBy']['having']:
            q += self.translateCond(query['condition'])
            q += ' and only where ' + self.translateAttr(query['attributes'][0])
            q += self.having(query)
        elif query['condition']:
            q += self.translateCond(query['condition'])
        elif query['groupBy']['having']:
            
            q +=  ' but only where ' + self.having(query)
        return q
    
    def having(self, query):
        """
        Translates the having part of group by queries.
        """
        match query['aggregates'][0]:
            
            case 'count(':
                if query['attributes'][0].name == '*':
                    q = self.translateAttr(query['attributes'][0])
                    if query['groupBy']['val'] == 1:
                        q += ' appear ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val']) + ' time per ' + query['attributes'][1].name
                    else:
                        q += ' appear ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val']) + ' times per ' + query['attributes'][1].name
                else:
                    q = self.translateAttr(query['attributes'][0])
                    if query['groupBy']['val'] == 1:
                        q += ' appears ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val']) + ' time per ' + query['attributes'][1].name
                    else:
                        q += ' appears ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val']) + ' times per ' + query['attributes'][1].name
            
            case 'max(':
                q = 'has a maximum value ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val'])
            
            case 'min(':
                q = 'has a minimum value ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val'])
            
            case 'avg(':
                q = 'has an average value ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val'])
            
            case 'sum(':
                q = 'has an additive total ' + self.havingOperator(query['groupBy']['operator']) + str(query['groupBy']['val'])
        return q

    def havingOperator(self, operator, count = False):
        """
        Translates the operator in the having section.
        """
        match operator:
            case '=':
                return ''
            case '<':
                return 'less than '
            case '>':
                return 'more than '
            case '<=':
                return 'less than or equal to '
            case '>=':
                return 'more than or equal to '
            case _:
                return ''
    
    def join(self, query):
        """
        Translate join queries into english.
        """
        match query['relation']['joinType']:
            case 'left outer join':
                #agg and attr
                q = self.joinPart1(query['aggregates'], query['attributes'], query['relation'], 0)

            case 'right outer join':
                q = self.joinPart1(query['aggregates'], query['attributes'], query['relation'], 1)
                
            case 'inner join':
                q = self.joinPart1(query['aggregates'], query['attributes'], query['relation'], 0)
                
            case 'natural inner join':
                q = self.joinPart1(query['aggregates'], query['attributes'], query['relation'], 0)

        q += self.joinPart2(query['aggregates'], query['attributes'], query['relation'])
        return q
    
    def joinPart1(self, aggs, attrs, rels, right = 0):
        """
        Translates the first part of join queries. If it is a right outer join it uses the 2nd attribute as that
        is the one from the right table.
        """
        
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
        """
        Translate the second part of the join query. Includes how they are joined.
        """
        if attrs[0].name == '*':
            match rels['joinType']:
                case 'left outer join':
                    q = ' and in the ' + rels['rel2'].name + ' table where it has a corresponding ' + rels['attr'].name + ' value'
                case 'inner join':
                    q = ' and in the ' + rels['rel2'].name + ' table where they have a matching ' + rels['attr'].name + ' value'
                case 'natural inner join':
                    q = ' where they are associated with a record in the ' + rels['rel2'].name + ' table'
                case 'right outer join':
                    q = ' and in the ' + rels['rel1'].name + ' table where it has a corresponding ' + rels['attr'].name + ' value'
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
    
    def getEnglishQuery(self):
        return super().getEnglishQuery()
    
    