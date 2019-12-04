'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''
import logging

import pandas as pd
from tokoin.searchitem.base import BaseProcessor

logger = logging.getLogger(__name__)

USER_FIELD = [
    '_id', 'url', 'external_id', 'name', 'alias', 'created_at', 'active', 
    'verified', 'shared', 'locale', 'timezone', 'last_login_at', 'email',
    'phone', 'signature', 'organization_id', 'tags', 'suspended', 'role'
]

class UserProcessor(BaseProcessor):
    name = 'users'
    
    def do_loads_data(self):
        df_user_org = pd.merge(self.df_user, self.df_organizations, left_on='organization_id_users',
                       right_on='_id_organizations',how='left')
        self.df_user_org_ticket_submitter = pd.merge(df_user_org, self.df_tickets, left_on='_id_users', 
                                      right_on='submitter_id_tickets', how='left')
        self.df_user_org_ticket_assignee = pd.merge(df_user_org, self.df_tickets, left_on='_id_users', 
                                      right_on='assignee_id_tickets', how='left')
    
    def check_search_field(self, field_name):
        if field_name in USER_FIELD:
            return True
        return False
    
    def do_search(self, field_name, field_value):
        data = {}
        try:
            field_name = field_name + '_' + self.name
            d_type = self.df_user_org_ticket_submitter[field_name].dtype.name
            field_value = self.do_format_search_value(d_type, field_value)
            if field_name not in ['tags']:
                res1 = self.df_user_org_ticket_submitter[self.df_user_org_ticket_submitter[field_name] == field_value]
                res2 = self.df_user_org_ticket_assignee[self.df_user_org_ticket_assignee[field_name] == field_value]
            else:
                res1 = self.df_user_org_ticket_submitter[self.df_user_org_ticket_submitter[field_name].astype(str).str.contains(field_value)]
                res2 = self.df_user_org_ticket_assignee[self.df_user_org_ticket_assignee[field_name].astype(str).str.contains(field_value)]
            self.filter_data(data, res1)
            self.filter_data(data, res2)
        except Exception as ex:
            logger.exception(ex)
        return data
    
    
    def filter_data(self, map_data, df):
        try:
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
        except Exception as ex:
            logger.exception(ex)
        return map_data
    
    def do_format_data(self, dict_data):
        list_result = []
        try:
            for _, val in dict_data.items():
                r = {}
                for item in USER_FIELD:
                    r[item] = val.get(item +'_' + self.name, None)
                
                r['organization_name'] = val.get('name_organizations', None)    
                list_ticket = val.get('list_ticket', [])
                for i in range(len(list_ticket)):
                    r['ticket_%s' % str(i)] = list_ticket[i]
                    
                list_result.append(r)
        except Exception as ex:
            logger.exception(ex)
        return list_result
    
        