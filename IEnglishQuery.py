# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from abc import ABC, abstractmethod

class IEnglishQuery(ABC):

    def __init__(self,sqlQuery):
        englishQuery = ''
    
    @abstractmethod
    def englishToString(english):
        question = ''
        for block in english:
            for string in block:
                question += string
        return question
    
    #translate aggregate function from SQL to english
    @abstractmethod
    def translateAgg(agg):
        match agg:
            case 'count(':
                engAgg = ' how many rows there are in '
            case 'max(':
                engAgg = ' the greatest value of '
            case 'min(':
                engAgg = ' the smallest value of '
            case 'avg(':
                engAgg = ' the average value of '
            case 'sum(':
                engAgg = ' the sum of all values of '
            case _:
                engAgg = ' the values of '
        return engAgg
    
    #translate attribute/s to english format
    @abstractmethod
    def translateAttr(attr):
        if attr == '*':
            engAttr = 'all columns' 
        else:
            engAttr = attr
        return engAttr
    
    #translate SQL condition to english
    @abstractmethod
    def translateCond(condition):
        engCond = ''
        match condition[0]:
            case 'limit':
                if condition[1] == 1:
                    engCond += ' but only show 1 row'
                else:
                    engCond += ' but only show ' + condition[1] + ' rows'
            case 'where':
                engCond += ' but only for rows where ' + condition[1] + ' ' + condition[2] + ' ' + condition[3]
            case 'order by':
                if condition[2].lower() == 'desc':
                    engCond += ' in descending order of ' + condition[1] + ' value'
                else:
                    engCond += ' in ascending order of ' + condition[1] + ' value'