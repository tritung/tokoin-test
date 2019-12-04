'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''

import os
import pandas as pd

class DataLoader:
    __instance = None
    users_table = None
    organizations_table = None
    tickets_table = None
    
    @staticmethod 
    def get_instance():
        if DataLoader.__instance == None:
            DataLoader()
        return DataLoader.__instance
    
    def __init__(self):
        if DataLoader.__instance != None:
            return DataLoader.__instance
        else:
            try:
                self.users_table = self.get_dataframte('users')
                self.users_table['verified_users'] = self.users_table['verified_users'].astype('bool')
                self.organizations_table = self.get_dataframte('organizations')
                self.tickets_table = self.get_dataframte('tickets')
                DataLoader.__instance = self
            except Exception as ex:
                raise ex
            
    def get_dataframte(self, item_name):
        path_file = os.path.abspath('resources/%s.json' % item_name)
        df = pd.read_json(path_file, orient='columns')
        df.set_index('_id')
        df = df.add_suffix('_' + item_name)
        return df
