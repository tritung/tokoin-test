'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''
from tokoin.data_loader import DataLoader


class BaseProcessor(object):
    def __init__(self, *args, **kwargs):
        data_tables = DataLoader.get_instance()
        self.df_user = data_tables.users_table
        self.df_organizations = data_tables.organizations_table
        self.df_tickets = data_tables.tickets_table
        self.do_loads_data()
        
    def do_loads_data(self):
        pass
    
    def get_all_search_field(self):
        return []
    
    def get_search_field(self, field_name):
        return None
    
    def search(self, field_name, field_value):
        result = self.do_search(field_name, field_value)
        return self.do_format_data(result)
    
    def do_search(self, field_name, field_value):
        return None
    
    def do_format_data(self, result):
        return None
    
    def print_result(self, result):
        if len(result) > 0:
            for item in result:
                for key, val in item.items():
                    print ('%s : \t %s' % (key, val))
                print ('\n-------------------------------------------------\n')
        else:
            print ('No results found')
    
    