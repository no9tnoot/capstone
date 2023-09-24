# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from abc import ABC, abstractmethod

class IEnglishQuery(ABC):
    """
    IEnglishQuery contains methods that are used in more than one type of question. 
    """

    likePos = ['second','third','fourth','fifth','sixth']

    def __init__(self,sqlQuery):
        self.englishQuery = ''
        self.sqlQuery = sqlQuery

    @abstractmethod
    def easyEnglish(self, sqlQuery):
        """
        Translates a simple query to english. Handles aggregate function and conditions including nested functions.
        """
        eq = ''
        if sqlQuery['aggregates']:
            eq += self.attrsAndAggs(sqlQuery['attributes'][0], sqlQuery['aggregates'][0])
        else:
            eq += 'the values of ' + self.onlyAttrs(sqlQuery['attributes'])

        eq += ' in the ' + sqlQuery['relation']['rel1'].name + ' table'

        if sqlQuery['condition']:
            eq += self.translateCond(sqlQuery['condition'], sqlQuery['nested'])
        return eq
    
    @abstractmethod
    def translateAttr(self, attr):
        """
        translate attribute/s to english format
        """
        if attr.name == '*':
            engAttr = 'all columns' 
        else:
            engAttr = attr.name
        return engAttr
    
    @abstractmethod
    def translateAgg(self, agg):
        """
        Translate aggregate function from SQL to english
        """
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
    
    
    @abstractmethod
    def translateCond(self, condition, nested = False):
        """
        Translate SQL condition to english.
        """
        engCond = ''
        match condition['cond']:

            case 'limit':
                if condition['val2'] == 1:
                    engCond += ' but only show the first'
                else:
                    engCond += ' but only show the first ' + condition['val2'] + ' records'

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
    
    @abstractmethod
    def translateLike(self, like):
        """
        Tranlate like wildcard patterns.
        """
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
    
    @abstractmethod
    def translateOperator(self, condition):
        """
        Translate comparison sybols into english.
        """
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

    @abstractmethod
    def translateVal2(self, condition, nested = False):
        """
        Interpret and translate the value that a field is compared to. Including LIKE and nested comparisons.
        """        
        if nested:
            return self.easyEnglish(condition['val2'].getDict())
        
        elif condition['operator'] == 'like':
            return "'" + condition['likeDict']['wildcard_free_string'] + "'"
        
        elif condition['val2'] == 'NULL':
            return 'exist'
        else:
            return condition['val2']

    
    @abstractmethod
    def attrsAndAggs(self, attrs, agg):
        """
        Translate an attribute with an aggregate function.
        """
        engAttrs = self.translateAgg(agg)
        engAttrs += self.translateAttr(attrs)
        return engAttrs
    
    @abstractmethod
    def onlyAttrs(self, attrs):
        """
        Translate one or more attributes.
        """
        engAttrs = self.translateAttr(attrs[0])
        if len(attrs) == 2:
            engAttrs += ' and ' + self.translateAttr(attrs[1])
        return engAttrs
    
    @abstractmethod
    def getEnglishQuery(self):
        """
        Return the english query string
        """
        return self.englishQuery
    