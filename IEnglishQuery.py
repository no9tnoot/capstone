# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from abc import ABC, abstractmethod

class IEnglishQuery(ABC):

    likePos = ['second','third','fourth','fifth','sixth']

    def __init__(self,sqlQuery):
        self.englishQuery = ''
        self.sqlQuery = sqlQuery

    """
    Translates a simple query to english. Handles aggregate function and conditions including nested functions.
    """
    @abstractmethod
    def easyEnglish(self, sqlQuery):
        eq = ''
        if sqlQuery['aggregates']:
            eq += self.attrsAndAggs(sqlQuery['attributes'][0], sqlQuery['aggregates'][0])
        else:
            eq += 'the values of ' + self.onlyAttrs(sqlQuery['attributes'])
        
        #not sure if this join bit is ever used
        if sqlQuery['join']:
            match sqlQuery['relation']['joinType']:
                case 'left outer join':
                    eq += ' in the ' + sqlQuery['relation']['rel1'].name + ' table'
                case 'right outer join':
                    eq += ' in the ' + sqlQuery['relation']['rel2'].name + ' table'
                case _:
                    eq += ' in the ' + sqlQuery['relation']['rel1'].name + ' table'     
        else:
            eq += ' in the ' + sqlQuery['relation']['rel1'].name + ' table'

        if sqlQuery['condition']:
            eq += self.translateCond(sqlQuery['condition'], sqlQuery['nested'])
        return eq
    
    """
    Takes the english from an array and puts it into one string.
    """
    #not sure if this is ever used anymore
    @abstractmethod
    def englishToString(self, english):
        question = ''
        for block in english:
            for string in block:
                question += string
        return question
    
    """
    Translate aggregate function from SQL to english
    """
    @abstractmethod
    def translateAgg(self, agg):
        match agg:
            case 'count(':
                engAgg = 'how many records there are in '
            case 'max(':
                engAgg = 'the greatest value of '
            case 'min(':
                engAgg = 'the smallest value of '
            case 'avg(':
                engAgg = 'the average value of '
            case 'sum(':
                engAgg = 'the total of all values in '
            case _:
                engAgg = 'the values of '
        return engAgg
    
    """
    translate attribute/s to english format
    """
    @abstractmethod
    def translateAttr(self, attr):
        if attr.name == '*':
            engAttr = 'all columns' 
        else:
            engAttr = attr.name
        return engAttr
    """
    Translate SQL condition to english.
    """
    @abstractmethod
    def translateCond(self, condition, nested = False):
        engCond = ''
        match condition['cond']:

            case 'limit':
                if condition['val2'] == 1:
                    engCond += ' but only show 1 row'
                else:
                    engCond += ' but only show ' + condition['val2'] + ' records'

            case 'where':
                engCond += ' but only for records where ' + condition['val1'].name + ' ' + self.translateOperator(condition) + ' ' + self.translateVal2(condition, nested)
                if self.sqlQuery['orCond']:
                    engCond += ' or ' + condition['or']['val1'].name + ' ' + self.translateOperator(condition['or']) + ' ' + self.translateVal2(condition['or'], nested)
            
            case 'order by':
                if condition['operator'].lower() == 'desc':
                    engCond += ' in descending order of ' + condition['val1'].name + ' value'
                else:
                    engCond += ' in ascending order of ' + condition['val1'].name + ' value'

            case _:
                print('Invalid condition')
        return engCond
    """
    Translate comparison sybols into english.
    """
    @abstractmethod
    def translateOperator(self, condition):
        match condition['operator']:
            case '=':
                return 'is'
            case '<':
                return 'is less than'
            case '>':
                return 'is greater than'
            case '<=':
                return 'is less than or equal to'
            case '>=':
                return 'is greater than or equal to'
            case 'like':
                return self.translateLike(condition['likeDict'])
            case 'is':
                return 'does not'
            case 'is not':
                return 'does'
            case _:
                return condition['operator']

    """
    Interpret and translate the value that a field is compared to. Including LIKE and nested comparisons.
    """        
    @abstractmethod
    def translateVal2(self, condition, nested = False):
        if nested:
            return self.easyEnglish(condition['val2'].getDict())
        
        elif condition['operator'] == 'like':
            return "'" + condition['likeDict']['wildcard_free_string'] + "'"
        
        elif condition['val2'] == 'NULL':
            return 'exist'
        else:
            return condition['val2']

    """
    Tranlate like wildcard patterns.
    """
    @abstractmethod
    def translateLike(self, like):
        match like['type']:

            case '%':  
                if like['starts_with_string']:
                    s = 'starts with'
                else:
                    s = 'ends with'

            case '%%':
                s = 'contains'
            
            case '_%':
                if like['starts_with_string']:
                    s = 'has a value where the ' + self.likePos[like['num_underscore']-1] + ' character from the beginning is'
                else:
                    s = 'has a value where the ' + self.likePos[like['num_underscore']-1] + ' character from the end is'

            case _:
                print('Invalid like type')
        return s

    """
    Return the english query string
    """
    @abstractmethod
    def getEnglishQuery(self):
        return self.englishQuery
    
    """
    Translate an attribute with an aggregate function.
    """
    @abstractmethod
    def attrsAndAggs(self, attrs, agg):
        engAttrs = self.translateAgg(agg)
        engAttrs += self.translateAttr(attrs)
        return engAttrs
    
    """
    Translate one or more attributes.
    """
    @abstractmethod
    def onlyAttrs(self, attrs):
        engAttrs = self.translateAttr(attrs[0])
        if len(attrs) == 2:
            engAttrs += ' and ' + self.translateAttr(attrs[1])
        return engAttrs