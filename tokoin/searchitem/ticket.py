'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''
import pandas as pd
from tokoin.searchitem.base import BaseProcessor

class TicketProcessor(BaseProcessor):
    name = 'tickets'
    
    def do_loads_data(self):
        df_ticket_org = pd.merge(self.df_tickets, self.df_organizations, left_on='organization_id_tickets',
                       right_on='_id_organizations',how='left')
        self.df_ticket_submitter = pd.merge(df_ticket_org, self.df_user, left_on='submitter_id_tickets', 
                                      right_on='_id_users', how='left')
        self.df_ticket_assignee = pd.merge(df_ticket_org, self.df_user, left_on='assignee_id_tickets', 
                                      right_on='_id_users', how='left')
        
    def get_all_search_field(self):
        return [
            '_id', 'url', 'external_id', 'created_at', 'type', 'subject',
            'description', 'priority', 'status', 'submitter_id', 'assignee_id',
            'organization_id', 'tags', 'has_incidents', 'due_at', 'via'
        ]
        
    def do_search(self, field_name, field_value):
        field_name = field_name + '_' + self.name
        res1 = self.df_ticket_submitter[self.df_ticket_submitter[field_name] == field_value]
        res2 = self.df_ticket_assignee[self.df_ticket_assignee[field_name] == field_value]
        data = {}
        self.filter_data(data, res1, 'submitter')
        self.filter_data(data, res2, 'assignee')
        return data
    
    
    def filter_data(self, map_data, df, filter_type='submitter'):
        for _, row in df.iterrows():
            dict_row = row.to_dict()
            _id_ticket = dict_row.get('_id_tickets')
            if _id_ticket not in map_data.keys():
                dict_row['submitter_name'] = None
                dict_row['assignee_name'] = None
                map_data[_id_ticket] = dict_row
            if filter_type == 'submitter':
                map_data[_id_ticket]['submitter_name'] = dict_row.get('name_users', None)
            else:
                map_data[_id_ticket]['assignee_name'] = dict_row.get('name_users', None)
                
        return map_data
    
    def do_format_data(self, dict_data):
        list_result = []
        for _, val in dict_data.items():
            r = {}
            for item in self.get_all_search_field():
                r[item] = val.get(item +'_' + self.name, None)
                
            r['submitter_name'] = val.get('submitter_name', None)
            r['assignee_name'] = val.get('assignee_name', None)
            r['organization_name'] = val.get('name_organizations', None)
            list_result.append(r)
        return list_result