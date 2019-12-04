'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''

import logging

import pandas as pd
from tokoin.searchitem.base import BaseProcessor


logger = logging.getLogger(__name__)

ORFANIZATION_FIELD = [
    '_id', 'url', 'external_id', 'name', 'domain_names', 'created_at',
    'details', 'shared_tickets', 'tags'
]

class OrganizationProcessor(BaseProcessor):
    name = 'organizations'
    
    def do_loads_data(self):
        self.df_org_user = pd.merge(self.df_organizations, self.df_user, left_on='_id_organizations',
                       right_on='organization_id_users', how='left')
        
        self.df_org_ticket = pd.merge(self.df_organizations, self.df_tickets, left_on='_id_organizations', 
                                      right_on='organization_id_tickets', how='left')

    
    def check_search_field(self, field_name):
        if field_name in ORFANIZATION_FIELD:
            return True
        return False
    
    def do_search(self, field_name, field_value):
        data = {}
        try:
            field_name = field_name + '_' + self.name
            d_type = self.df_org_user[field_name].dtype.name
            field_value = self.do_format_search_value(d_type, field_value)
            
            res1 = self.df_org_user[self.df_org_user[field_name] == field_value]
            res2 = self.df_org_ticket[self.df_org_ticket[field_name] == field_value]
            self.filter_data(data, res1, 'users')
            self.filter_data(data, res2, 'tickets')
        except Exception as ex:
            logger.exception(ex)
        return data
    
    
    def filter_data(self, map_data, df, filter_type='users'):
        try:
            for _, row in df.iterrows():
                dict_row = row.to_dict()
                _id_organization = dict_row.get('_id_organizations')
                if _id_organization not in map_data.keys():
                    if filter_type == 'users':
                        list_user = []
                        list_user.append(dict_row.get('name_users'))
                        dict_row['list_user'] = list_user
                    else:
                        list_ticket = []
                        list_ticket.append(dict_row.get('subject_tickets'))
                        dict_row['list_ticket'] = list_ticket
                        
                    map_data[_id_organization] = dict_row
                else:
                    if filter_type == 'users':
                        map_data[_id_organization]['list_user'].append(dict_row.get('name_users'))
                    else:
                        if 'list_ticket' not in map_data[_id_organization].keys():
                            map_data[_id_organization]['list_ticket'] = []
                        map_data[_id_organization]['list_ticket'].append(dict_row.get('subject_tickets'))
        except Exception as ex:
            logger.exception(ex)
        return map_data
    
    def do_format_data(self, dict_data):
        list_result = []
        try:
            for _, val in dict_data.items():
                r = {}
                for item in ORFANIZATION_FIELD:
                    r[item] = val.get(item +'_' + self.name, None)
                    
                list_ticket = val.get('list_ticket', [])
                for i in range(len(list_ticket)):
                    r['ticket_%s' % str(i)] = list_ticket[i]
                    
                list_user = val.get('list_user', [])
                for i in range(len(list_user)):
                    r['user_%s' % str(i)] = list_user[i]
                    
                list_result.append(r)
        except Exception as ex:
            logger.exception(ex)
        return list_result
    