'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''
import pandas as pd
from tokoin.searchitem.base import BaseProcessor


class UserProcessor(BaseProcessor):
    name = 'users'
    
    def do_loads_data(self):
        df_user_org = pd.merge(self.df_user, self.df_organizations, left_on='organization_id_users',
                       right_on='_id_organizations',how='left')
        self.df_user_org_ticket_submitter = pd.merge(df_user_org, self.df_tickets, left_on='_id_users', 
                                      right_on='submitter_id_tickets', how='left')
        self.df_user_org_ticket_assignee = pd.merge(df_user_org, self.df_tickets, left_on='_id_users', 
                                      right_on='assignee_id_tickets', how='left')
        
    def get_all_search_field(self):
        return [
            '_id', 'url', 'external_id', 'name', 'alias', 'created_at', 'active', 
            'verified', 'shared', 'locale', 'timezone', 'last_login_at', 'email',
            'phone', 'signature', 'organization_id', 'tags', 'suspended', 'role'
        ]
    
    def do_search(self, field_name, field_value):
        field_name = field_name + '_' + self.name
        res1 = self.df_user_org_ticket_submitter[self.df_user_org_ticket_submitter[field_name] == field_value]
        res2 = self.df_user_org_ticket_assignee[self.df_user_org_ticket_assignee[field_name] == field_value]
        data = {}
        self.filter_data(data, res1)
        self.filter_data(data, res2)
        return data
    
    
    def filter_data(self, map_data, df):
        for _, row in df.iterrows():
            dict_row = row.to_dict()
            _id_user = dict_row.get('_id_users')
            if _id_user not in map_data.keys():
                list_ticket = []
                list_ticket.append(dict_row.get('subject_tickets'))
                dict_row['list_ticket'] = list_ticket
                map_data[_id_user] = dict_row
            else:
                map_data[_id_user]['list_ticket'].append(dict_row.get('subject_tickets'))
        return map_data
    
    def do_format_data(self, dict_data):
        list_result = []
        for _, val in dict_data.items():
            r = {}
            for item in self.get_all_search_field():
                r[item] = val.get(item +'_' + self.name, None)
            
            r['organization_name'] = val.get('name_organizations', None)    
            list_ticket = val.get('list_ticket', [])
            for i in range(len(list_ticket)):
                r['ticket_%s' % str(i)] = list_ticket[i]
                
            list_result.append(r)
        return list_result
    
        