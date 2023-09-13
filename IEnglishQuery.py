# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from abc import ABC, abstractmethod

class IEnglishQuery(ABC):

    def __init__(self,sqlQuery):
        self.englishQuery = ''
    
    @abstractmethod
    def englishToString(self, english):
        question = ''
        for block in english:
            for string in block:
                question += string
        return question
    
    #translate aggregate function from SQL to english
    @abstractmethod
    def translateAgg(self, agg):
        match agg:
            case 'count(':
                engAgg = 'how many rows there are in '
            case 'max(':
                engAgg = 'the greatest value of '
            case 'min(':
                engAgg = 'the smallest value of '
            case 'avg(':
                engAgg = 'the average value of '
            case 'sum(':
                engAgg = 'the sum of all values of '
            case _:
                engAgg = 'the values of '
        return engAgg
    
    #translate attribute/s to english format
    @abstractmethod
    def translateAttr(self, attr):
        if attr.name == '*':
            engAttr = 'all columns' 
        else:
            engAttr = attr.name
        return engAttr
    
    #translate SQL condition to english
    @abstractmethod
    def translateCond(self, condition):
        engCond = ''
        match condition['cond']:
            case 'limit':
                if condition['val2'] == 1:
                    engCond += ' but only show 1 row'
                else:
                    engCond += ' but only show ' + condition['val2'] + ' rows'
            case 'where':
                engCond += ' but only for rows where ' + condition['val1'].name + ' ' + self.translateOperator(condition) + ' ' + condition['val2']
            case 'order by':
                if condition['operator'].lower() == 'desc':
                    engCond += ' in descending order of ' + condition['val1'].name + ' value'
                else:
                    engCond += ' in ascending order of ' + condition['val1'].name + ' value'
        return engCond
    
    @abstractmethod
    def translateOperator(self, condition):
        match condition['operator']:
            case '=':
                return 'is equal to'
            case '<':
                return 'is less than'
            case '>':
                return 'is greater than'
            case '<=':
                return 'is less than or equal to'
            case '>=':
                return 'is greater than or equal to'
            case 'like':
                return self.translateLike(condition['like'])
            case _:
                return condition['operator']

    @abstractmethod
    def translateLike(self, like):
        match like['type']:
            case '%':  
                if like['startswith']:
                    s = 'starts with'
                else:
                    s = 'ends with'
            case '%%':
                s = 'contains'
            case '_%':
                s = self.likepos[like['pos']-1] + ''

    @abstractmethod
    def getEnglishQuery(self):
        return self.englishQuery