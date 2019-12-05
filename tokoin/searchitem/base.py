'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''
import logging

from tokoin.data_loader import DataLoader


logger = logging.getLogger(__name__)

class BaseProcessor(object):
    name = ''
    
    def __init__(self, *args, **kwargs):
        data_tables = DataLoader.get_instance()
        self.df_user = data_tables.users_table
        self.df_organizations = data_tables.organizations_table
        self.df_tickets = data_tables.tickets_table
        self.do_loads_data()
        
    def do_loads_data(self):
        pass
    
    def check_search_field(self, field_name):
        return False
    
    def search(self, field_name, field_value):
        print ('Searching %s for %s with a value %s  ...........' % (self.name, field_name, field_value))
        result = self.do_search(field_name, field_value)
        return self.do_format_data(result)
    
    def do_search(self, field_name, field_value):
        return None
    
    def do_format_data(self, result):
        return None
    
    def do_format_search_value(self, d_type, field_value):
        try:
            if d_type in ['int64', 'int32']:
                field_value = int(field_value)
            elif d_type in ['float64']:
                field_value = float(field_value)
            elif d_type in ['bool']:
                field_value = True if field_value.lower() == 'true' else False if field_value.lower() == 'false' else field_value
        except Exception as ex:
            logger.exception(ex)
            
        return field_value
    
    def print_result(self, result):
        if len(result) > 0:
            print ('Results: %s objects founds \n' % len(result))
            for item in result:
                for key, val in item.items():
                    print ('%s : \t %s' % (key, val))
                print ('\n-------------------------------------------------\n')
        else:
            print ('No results found')
    
    def try_parse_int(self, s, base=10, val=None):
        try:
            if type(s) is float:
                return round(s)
            return int(s)
        except Exception as ex:
            logger.exception(ex)
            return s