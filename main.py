'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''
from tokoin.factory import SearchFactory


if __name__ == '__main__':
#     search_type = input("Select 1) Users or 2) Tickets or 3)Organizations: ")
#     search_processor = SearchFactory.get_search_processor(search_type)
#     
#     search_field = input("Enter search term: ")
#     search_value = input("Enter search value: ")
#     res = search_processor.search(search_field, search_value)
    search_processor = SearchFactory.get_search_processor(2)
    res = search_processor.search('_id', '1a227508-9f39-427c-8f57-1b72f3fab87c')
    search_processor.print_result(res)
    