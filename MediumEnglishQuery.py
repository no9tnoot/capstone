# Molly Ryan, Peter Berens, Sian Wood
# 9 September 2023
# MediumEnglishQuery

from IEnglishQuery import IEnglishQuery

class MediumEnglishQuery(IEnglishQuery):

    likePos = ['second','third','fourth','fifth','sixth']

    def __init__(self, sqlQuery):
        super().__init__(self, sqlQuery)
        self.englishQuery = 'Show '
        if sqlQuery['aggregates']:
            self.englishQuery += self.attrsAndAggs(sqlQuery['attributes'][0], sqlQuery['aggregates'][0])
        else:
            self.englishQuery += self.onlyAttrs(sqlQuery['attributes'])
        self.englishQuery += ' in the ' + sqlQuery['relation']['rel1'].name + ' table'
        if sqlQuery['condition']:
            self.englishQuery += self.translateCond(sqlQuery['condition'])
        self.englishQuery += '.'

    #show (function) as (asName)
    #e.g.: show price * 0.152 as VAT

    def like(self, like):
        match like['type']:
            case '%':  
                if like['startswith']:
                    s = 'starts with'
                else:
                    s = 'ends with'
            case '%%':
                s = 'contains'
            case '_%':
                s = self.likepos[like['pos']] + ''