'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''
from tokoin.searchitem.user import UserProcessor
from tokoin.searchitem.ticket import TicketProcessor
from tokoin.searchitem.organization import OrganizationProcessor

class SearchFactory(object):
    @staticmethod
    def get_search_processor(search_type):
        if int(search_type) in SearchFactory.dict_processor:
            return SearchFactory.dict_processor.get(int(search_type))
        return None
    
    dict_processor = {
        1: UserProcessor(),
        2: TicketProcessor(),
        3: OrganizationProcessor()
    }