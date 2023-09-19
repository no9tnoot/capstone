# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from EasySQLQuery import EasySQLQuery
from ISQLQuery import ISQLQuery
import random
import mysql.connector


class HardSQLQuery(ISQLQuery):
        
    def __init__(self, database, seed):
        super().__init__(database, seed)
        self.hardBuilder()
        
    def getRel(self, numeric=False, string=False):
        return super().getRel(numeric, string)
    
    def selectAttrVal(self, relation, attribute):
        return super().selectAttrVal(relation, attribute)
    
    def getAgg(self):
        return super().getAgg()
    
    def formatQueryAggs(self, attributes, aggregates):
        return super().formatQueryAggs(attributes, aggregates)
    
    def formatQueryConds(self, conds):
        return super().formatQueryConds(conds)
    
    def createAgg(self, relation=None, attribute=None, aggFn=None):
        return super().createAgg(relation, attribute, aggFn)
    
    def createCond(self, relation, astOrAttr=None, condType=None, numeric=False):
        super().createCond(relation, astOrAttr, condType, numeric)
    
    def createSimple(self, relation, attribute=None):
        return super().createSimple(relation, attribute)
    
    def createOrderByCond(self, relation):
        return super().createOrderByCond(relation)
    
    def createLimitCond(self, relation):
        return super().createLimitCond(relation)
    
    def createWhereCond(self, relation, cond_details, numeric=False, whereAttr=None):
        return super().createWhereCond(relation, cond_details, numeric, whereAttr)
    
    def createLikeCond(self, relation, cond_details):
        super().createLikeCond(relation, cond_details)
        
    def insertPercentWildCard(self, value, ends_with_perc, num_char_to_remove, cond_details):
        super().insertPercentWildCard(value, ends_with_perc, num_char_to_remove, cond_details)
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()
    
    def easyBuilder(self, relation, attribute = None, aggOrCond=None, aggFn = None, condType = None):
        super().easyBuilder(relation, attribute, aggOrCond, aggFn, condType)
        
    def mediumBuilder(self, relation = None, attribute = None, components = None):
        super().mediumBuilder(relation, attribute, components)
            
    def hardBuilder(self):
        
        type = random.choice(['nested', 'join', 'groupBy'])
        
        match type:
            
            case 'nested':
                relation = self.getRel(numeric=True)
                self.easyBuilder(relation = relation, aggOrCond = 'nestedWhereCond')
                # ensure not doing a null comparison
                while self.conds['operator'] not in ISQLQuery.operators:
                    self.easyBuilder(relation = relation, aggOrCond = 'nestedWhereCond')
                            
                sqlQuery2 = self.createNestedQuery(self.rels['rel1'], self.conds, self.attrs)
                
                self.conds['val2']=sqlQuery2
                self.nested = True
                
                self.query =  self.toQuery()
                
            case 'join':
                joinRelsAndAtts = random.choice(self.db.joinRelations)
                self.rels['rel1'] = joinRelsAndAtts['rel1']
                self.rels['rel2'] = joinRelsAndAtts['rel2']
                self.createJoin(joinRelsAndAtts)
                self.query = self.toQuery()
                
            case 'groupBy':
                self.createGroupBy()
                self.query = self.toQuery()
                
    
    def selectHavingVal(self, operator):
            
        # Connect to database
        database = mysql.connector.connect(
            host=self.db.host,
            user=self.db.user,
            password=self.db.pword,
            database=self.db.db_name
        )
        
        cursor = database.cursor()  # Create a cursor to interact with the database
        print(self.toQuery())
        cursor.execute(self.toQuery())
        counts = cursor.fetchall()
        if len(counts)==0:
            self.createGroupBy()
        else:
            counts = [row[0] for row in counts]

        # try do a comparison to a value, but if not enough different values exist, change to an '='
        try:
            if operator[0] == '<': val = random.randint( max(min(counts),max(counts)//2), max(counts))
            elif operator[0] == '>': val = random.randint( min(counts), min(min(counts)*2,max(counts)))
            else: val = random.choice(counts)
        except:  
            operator = '='
            val = random.choice(counts)

        
        if val is not None: return val # if the value isn't a null value
        else: return self.selectAttrVal(operator) # recurse until a non null value is selected

              
    def createGroupBy(self):
        
        relation = random.choice(self.db.groupByRelations)
        
        groupAttr = random.choice(relation.groupByAttributes)
        
        if len(relation.groupByAttributes) > 1:
            aggOrCond = random.choice(['','cond'])
        else:
            aggOrCond = ''
        
        self.easyBuilder(relation = relation, 
                         attribute=groupAttr, 
                         aggOrCond = aggOrCond, 
                         condType = 'where')
        
        # select second attribute
        attr2 = random.choice([ISQLQuery.asterisk, relation.getAttribute()])
        while groupAttr.isEqual(attr2):
            attr2 = relation.getAttribute()
        
        # get an appropriate aggregate function
        if attr2.isEqual(ISQLQuery.asterisk): 
            aggFn = 'count('
        elif attr2.numeric: aggFn = self.getAgg()
        else: aggFn = random.choice(['count(', 'max(', 'min('])
        
        self.attrs.insert(0, attr2)
        self.aggFns.insert(0, aggFn)
        
        self.groupBy['cond']=' GROUP BY '
        self.groupBy['groupAttr']=self.attrs[1]
        
        having = random.choice([True, False])
        having = True
        self.groupBy['having']=None
        if having: 
            self.groupBy['operator'] = random.choice(self.operators)
            self.groupBy['val'] = self.selectHavingVal(self.groupBy['operator'])
            self.groupBy['having']=' HAVING '
            self.groupBy['aggAttr'] = self.aggFns[0] + self.attrs[0].name + ')'
                
        
        
        

    def createJoin(self, joinRelsAndAtts):
        
        astOrAttr = random.choice([ISQLQuery.asterisk,joinRelsAndAtts['rel1'].getAttribute()])
        #english currently only working with 2 attributes
        astOrAttr = joinRelsAndAtts['rel1'].getAttribute()
        # make sure that the chosen attribute is not the only joinable attribute
        if len(joinRelsAndAtts['joinAttributes'])==1:
            while astOrAttr.isEqual(joinRelsAndAtts['joinAttributes'][0]):
                astOrAttr = joinRelsAndAtts['rel1'].getAttribute()
    
        if astOrAttr.isEqual(ISQLQuery.asterisk): aggFn='count('
        elif not astOrAttr.numeric: aggFn = random.choice(['count(', 'max(', 'min('])
        else: aggFn = None
                
        
        self.easyBuilder(relation = self.rels['rel1'], 
                         attribute=astOrAttr, 
                         aggOrCond = random.choice(['','agg']), 
                         aggFn=aggFn)
        
        
        # select second attribute
        if not astOrAttr.isEqual(ISQLQuery.asterisk):
            attr2 = joinRelsAndAtts['rel2'].getAttribute()
            while astOrAttr.isEqual(attr2):
                attr2 = joinRelsAndAtts['rel2'].getAttribute()
            self.attrs.append(attr2)
        
                
        joinType = random.choice(['natural inner join', 'inner join', 'left outer join', 'right outer join'])
              
        if joinType != 'natural inner join':
            self.rels['operator']='on'
            self.rels['attr'] = random.choice(joinRelsAndAtts['joinAttributes'])
            while self.rels['attr'].isEqual(astOrAttr):
                self.rels['attr'] = random.choice(joinRelsAndAtts['joinAttributes'])
        
            # if astOrAttr != ISQLQuery.asterisk:
            #     attr_from_rel1 = self.rels['rel1'].getAttributeWithName(self.rels['attr'].name)
            #     attr_from_rel2 = self.rels['rel2'].getAttributeWithName(self.rels['attr'].name)
            #     if attr_from_rel1.isPrimary() and attr_from_rel2.isPrimary():
            #         self.attrs.append(self.rels['rel1'].getAttribute(secondary=True))

        
        self.rels['joinType'] = joinType
        self.join=True
            
        
    def createNestedQuery(self, relation, conds, attrs):
        
        
        attribute = conds['val1']
        operator = conds['operator']

        match operator:
            case '=':
                aggFn=random.choice(['max(', 'min(', 'avg('])
            case _:
                aggFn = 'avg('
        
        aggOrCond = random.choice(['agg','nestedWhereCond'])
        
        nestedQuery = EasySQLQuery(self.db, 'seed', relation = relation, attribute = attribute, aggFn = aggFn, aggOrCond=aggOrCond)
        if nestedQuery.conds:
            while nestedQuery.conds['val1']==attrs[0] or nestedQuery.conds['val1']==conds['val1']:
                nestedQuery = EasySQLQuery(self.db, 'seed', relation = relation, attribute = attribute, aggFn = aggFn, aggOrCond=aggOrCond)

        nestedQuery.aggFns.append(aggFn)
        
        nestedQuery.rels['rel1']=relation

        return nestedQuery
        
                
    
    def toQuery(self):
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns)
        q += ' FROM ' + self.rels['rel1'].name
        
        if self.conds:
            q += self.formatQueryConds(self.conds)
        
        if self.orCond:
            q += self.formatQueryConds(self.conds['or'])
        
        if self.join:
            q += ' ' + self.rels['joinType'] + ' ' + self.rels['rel2'].name 
            if self.rels['joinType'] != 'natural inner join':
                q += ' ON ' + self.rels['rel1'].name + '.' + self.rels['attr'].name + ' = ' + self.rels['rel2'].name + '.' + self.rels['attr'].name
            
        if self.groupBy:
            q +=  ' GROUP BY ' + self.groupBy['groupAttr'].name
            if self.groupBy['having'] is not None:
                if self.attrs[0].numeric or self.aggFns[0]=='count(': 
                    q += ' HAVING ' + self.groupBy['aggAttr'] + ' ' + self.groupBy['operator'] + ' ' + str(self.groupBy['val'])
                else:
                    q += ' HAVING ' + self.groupBy['aggAttr'] + ' ' + self.groupBy['operator'] + ' \'' + str(self.groupBy['val']) +'\''
        
        return q
    
    
    # #temp for testing
from Session import Session     
d = Session.loadDatabase()
s = HardSQLQuery(d, 'seed')
print(s.getSqlQuery())
 