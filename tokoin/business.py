'''
Created on Dec 4, 2019

@author: TUNGTRUONG
'''
import sys

from tokoin.factory import SearchFactory
from tokoin.searchitem.organization import ORFANIZATION_FIELD
from tokoin.searchitem.ticket import TICKET_FIELD
from tokoin.searchitem.user import USER_FIELD


def check_exit_input(input_value):
    if input_value == 'quit':
        sys.exit(0)

def check_search_input():
    is_valid = False
    print ("Select 1) Users or 2) Tickets or 3)Organizations:\n")
    while not is_valid:
        search_type = input()
        check_exit_input(search_type)
        if search_type in ['1', '2', '3']:
            is_valid = True
        else:
            print ('Invalid select. Please input again\n')
            
    search_processor = SearchFactory.get_search_processor(search_type)
    
    is_valid = False
    print ("Enter search term:\n")
    while not is_valid:
        search_field = input()
        if search_processor.check_search_field(search_field):
            is_valid = True
        else:
            print ('Invalid select. Please input again\n')
    
    search_value = input("Enter search value:\n")
    
    search_res = search_processor.search(search_field, search_value)
    search_processor.print_result(search_res)

    print ('\n\n=============================================\n\n')
    check_option_type_input()
    
    
def show_list_searchable():
    print ('Search Users with:\n')
    for item in USER_FIELD:
        print (item + '\n')
    
    print ('----------------------------------------\n\n')
    print ('Search Tickets with:\n')
    for item in TICKET_FIELD:
        print (item + '\n')
        
    print ('----------------------------------------\n\n')
    print ('Search Organizations with:\n')
    for item in ORFANIZATION_FIELD:
        print (item + '\n')
    
    print ('\n\n============================================================')
    check_option_type_input()

def check_option_type_input():
    print ("Type 'quit' to exit any time, Press 'Enter' to countinue\n\n")
    print ("\tSelect search options:\n")
    print ("\tPress 1 to search\n")
    print ("\tPress 2 to view a list of searchable fields\n")
    print ("\tType 'quit' to exit\n")
    is_valid = False
    while not is_valid:
        option_type = input()
        check_exit_input(option_type)
        if option_type in ['1', '2', 'quit']:
            is_valid = True
        else:
            print ('Invalid select. Please input again\n')
    
    if option_type == '1':
        check_search_input()
    else:
        show_list_searchable()
        
        