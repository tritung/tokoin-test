'''
Created on Dec 3, 2019

@author: TUNGTRUONG
'''
from tokoin import business
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename="log.log", level=logging.INFO)


if __name__ == '__main__':
    business.check_option_type_input()
    
