# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from .EasySQLQuery import EasySQLQuery
from .ISQLQuery import ISQLQuery
import random

class HardSQLQuery(ISQLQuery):
    """
    Hard mySQL Query object and constructor. Implements the ISQLQuery interface. Generates a
    hard query on initialisation and stores the string, runnable query in the 'query' instance
    variable.
    """
    
    def __init__(self, database):
        """
        Sets the instance variables of the hard query, and creates the string query.
        """
        super().__init__(database)
        self.hardBuilder()
        self.query = self.toQuery()
    
    def getRel(self, numeric=False, string=False):
        return super().getRel(numeric, string)
    
    def getAgg(self, numeric=False):
        return super().getAgg(numeric)
    
    def formatQueryAggs(self, attributes, aggregates):
        return super().formatQueryAggs(attributes, aggregates)
    
    def formatQueryConds(self, conds):
        return super().formatQueryConds(conds)
    
    def createSimple(self, relation, attribute=None):
        return super().createSimple(relation, attribute)
    
    def createAgg(self, relation=None, attribute=None, aggFn=None): 
        return super().createAgg(relation, attribute, aggFn)
    
    def createCond(self, relation, astOrAttr=None, condType=None, numeric=False):
        super().createCond(relation, astOrAttr, condType, numeric)
    
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
    
    def createGroupBy(self):
        """
        Creates a 'group by' query.
        Selects an attribute with a large proportion of repeated entries by which to group other 
        attributes. 
        """
        relation = random.choice(self.db.groupByRelations) # select a relation that has an attribute suitable for grouping
        
        groupAttr = random.choice(relation.groupByAttributes) # select an attribute to group by
        
        if len(relation.groupByAttributes) > 1:
            aggOrCond = random.choice(['','cond'])
        else:
            aggOrCond = ''
        
        # fill the instance variables with values for an easy simple or where query
        self.easyBuilder(relation = relation, 
                         attribute=groupAttr, 
                         aggOrCond = aggOrCond, 
                         condType = 'where')    
        
        # select a second attribute (which will be aggregated, and grouped by the first attribute)
        attr2 = random.choice([ISQLQuery.asterisk, relation.getAttribute()])
        while groupAttr.isEqual(attr2):
            attr2 = relation.getAttribute()
        
        having = random.choice([True, False]) # decide if doing a 'having' condition
        
        # get an appropriate aggregate function to apply to attr2
        if attr2.isEqual(ISQLQuery.asterisk): 
            aggFn = 'count('
        elif attr2.numeric: aggFn = self.getAgg()
        else: 
            aggFn = random.choice(['count(', 'max(', 'min('])
            having = False
        
        self.attrs.insert(0, attr2)
        self.aggFns.insert(0, aggFn)
        
        self.groupBy['cond']=' GROUP BY '
        self.groupBy['groupAttr']=self.attrs[1]
        
        self.groupBy['having']=None
        if having: # try create 'HAVING' section of query
            self.groupBy['operator'] = random.choice(self.operators)
            self.groupBy['val'] = self.createHaving()
            if self.groupBy['val']!='': # if having could be created, set the appropriate instance variables
                self.groupBy['having']=' HAVING '
                self.groupBy['aggAttr'] = self.aggFns[0] + self.attrs[0].name + ')'
            
        
    def createHaving(self):
        """
            Creates the 'having' condition of a 'group by' query.
        """ 
        # get an array of possible count values from the database
        counts = self.db.selectHavingVals(self.toQuery())
        
        # if the group by query does not produce many groups, do not further constrict with a having condition
        if len(counts)<3:
            self.groupBy['operator']=''
            return ''
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
        else: return self.createHaving() # recurse until a non null value is selected 
        
        
    def createJoin(self, joinRelsAndAtts):
        """
            Creates a 'join' query. 
            Chooses an attribute to select from one of the two relations, chooses the type of join,
            and then selects the attribute on which to join (if not doing a natural inner join).
        """
        astOrAttr = random.choice([ISQLQuery.asterisk,joinRelsAndAtts['rel1'].getAttribute()]) # select * or a random attribute from the first relation

        # make sure that the chosen attribute is not the only joinable attribute
        if len(joinRelsAndAtts['joinAttributes'])==1:
            while astOrAttr.isEqual(joinRelsAndAtts['joinAttributes'][0]):
                astOrAttr = joinRelsAndAtts['rel1'].getAttribute()
                
        # fill the instance variables with 
        self.easyBuilder(relation = self.rels['rel1'], 
                         attribute=astOrAttr, 
                         aggOrCond = '')
        
        
        # select second attribute if the first is not *
        if not astOrAttr.isEqual(ISQLQuery.asterisk):
            # if limited number of joinable attributes in relation, use a non joinable attribute
            loopForNotJoinableAttr =  len(joinRelsAndAtts['joinAttributes']) < 3 
            attr2 = joinRelsAndAtts['rel2'].getAttribute()
            while astOrAttr.isEqual(attr2) or loopForNotJoinableAttr:
                attr2 = joinRelsAndAtts['rel2'].getAttribute()
                if loopForNotJoinableAttr: 
                    loopForNotJoinableAttr = attr2 in joinRelsAndAtts['joinAttributes']
            self.attrs.append(attr2) # add the choicen attribute to attrs instance array
        
              
        joinType = random.choice(['natural inner join', 'inner join', 'left outer join', 'right outer join'])
        
        if joinType != 'natural inner join': 
            self.rels['operator']='on' # do a 'join on' statement to avoid ambiguous clause SQL error
            self.rels['attr'] = random.choice(joinRelsAndAtts['joinAttributes']) # select the attribute to join on
            while self.rels['attr'].isEqual(astOrAttr) or (not astOrAttr.isEqual(ISQLQuery.asterisk) and self.rels['attr'].isEqual(self.attrs[1])):
                self.rels['attr'] = random.choice(joinRelsAndAtts['joinAttributes'])

        
        self.rels['joinType'] = joinType
        self.join=True
            
    
    def createNestedQuery(self, relation, conds, attrs):
        """
        Creates a nested query.
        Creates an easy query (with either an aggregate or a numeric where condition), by which to 
        compare the main easy query to.
        """    
        attribute = conds['val1'] # get the attribute being compared from conds
        operator = conds['operator'] # get the operator being used from conds

        match operator:
            case '=':
                aggFn=random.choice(['max(', 'min(', 'avg('])
            case _:
                aggFn = 'avg('
        
        aggOrCond = random.choice(['agg','nestedWhereCond']) # choose to do either an aggregate or numeric where query
        
        nestedQuery = EasySQLQuery(self.db, relation = relation, attribute = attribute, aggFn = aggFn, aggOrCond=aggOrCond)
        
        if nestedQuery.conds: # if doing a where condition, ensure the nested query is not redundant
            while nestedQuery.conds['val1']==attrs[0] or nestedQuery.conds['val1']==conds['val1']:
                nestedQuery = EasySQLQuery(self.db, relation = relation, attribute = attribute, aggFn = aggFn, aggOrCond=aggOrCond)

        nestedQuery.aggFns.append(aggFn)
        
        nestedQuery.rels['rel1']=relation

        return nestedQuery
    
    
    def easyBuilder(self, relation, attribute = None, aggOrCond=None, aggFn = None, condType = None):
        super().easyBuilder(relation, attribute, aggOrCond, aggFn, condType)
    
    def mediumBuilder(self, relation = None, attribute = None, components = None):
        super().mediumBuilder(relation, attribute, components)
            
    def hardBuilder(self):
        """
        Sets the query instance variables with values for a hard SQL query. Can create queries
        of type 'nested,' which consists of an easy query conditional on another easy query,
        'join,' which connects information in two relations, and 'group by' which groups entries 
        by shared values.
        """    
        # randomly select the type of hard query to create
        type = random.choice(['nested', 'join', 'groupBy'])

        match type:
            # Generate a 'nested' query
            case 'nested':
                relation = self.getRel(numeric=True) # select a random numeric relation
                while len(relation.numericAttributes)<3: # make sure the relation has enough numeric attributes for comparison
                    relation = self.getRel(numeric=True)
                    
                self.easyBuilder(relation = relation, aggOrCond = 'nestedWhereCond') # fill instance variables as for a numeric where condition
                
                # ensure not doing a null comparison
                while self.conds['operator'] not in ISQLQuery.operators:
                    self.easyBuilder(relation = relation, aggOrCond = 'nestedWhereCond')
                            
                sqlQuery2 = self.createNestedQuery(self.rels['rel1'], self.conds, self.attrs) # create the nested query
                
                self.conds['val2']=sqlQuery2 # insert the nested query into conds
                self.nested = True
                
            
            # Generate a 'join' query
            case 'join':
                joinRelsAndAtts = random.choice(self.db.joinRelations)
                self.rels['rel1'] = joinRelsAndAtts['rel1']
                self.rels['rel2'] = joinRelsAndAtts['rel2']
                self.createJoin(joinRelsAndAtts)
            
            # Generate a 'group by' query
            case 'groupBy':
                self.createGroupBy()
                
        
                
    def toQuery(self):
        """
        Formats instance variable information into a string SQL command and returns it.
        """
        q = 'SELECT '
        q += self.formatQueryAggs(self.attrs, self.aggFns) # format the main attributes and aggregate functions
        q += ' FROM ' + self.rels['rel1'].name
        
        if self.conds: # formats the condition, if one exists
            q += self.formatQueryConds(self.conds) 
        
        if self.orCond: # formats the or condition, if one exists
            q += self.formatQueryConds(self.conds['or']) 
        
        if self.join:  # formats the join, if one exists
            q += ' ' + self.rels['joinType'] + ' ' + self.rels['rel2'].name 
            if self.rels['joinType'] != 'natural inner join':
                q += ' ON ' + self.rels['rel1'].name + '.' + self.rels['attr'].name + ' = ' + self.rels['rel2'].name + '.' + self.rels['attr'].name
            
        if self.groupBy: # formats the group by condition, if one exists
            q +=  ' GROUP BY ' + self.groupBy['groupAttr'].name
            if self.groupBy['having'] is not None:
                if self.attrs[0].numeric or self.aggFns[0]=='count(': 
                    q += ' HAVING ' + self.groupBy['aggAttr'] + ' ' + self.groupBy['operator'] + ' ' + str(self.groupBy['val'])
                else:
                    q += ' HAVING ' + self.groupBy['aggAttr'] + ' ' + self.groupBy['operator'] + ' \'' + str(self.groupBy['val']) +'\''
        
        return q
    
    def getSqlQuery(self):
        return super().getSqlQuery()
    
    def getDict(self):
        return super().getDict()
 