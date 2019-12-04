'''
Created on Dec 4, 2019

@author: TUNGTRUONG
'''
from unittest import TestCase

from tokoin.factory import SearchFactory


class TicketUsers(TestCase):
    def setUp(self):
        self.processor = SearchFactory.get_search_processor('2')

    def test_search_field_found(self):
        res = self.processor.check_search_field('description')
        self.assertEqual(res, True)
        
    def test_search_field_not_found(self):
        res = self.processor.check_search_field('domain_names_test')
        self.assertEqual(res, False)
        
    def test_search_int(self):
        res = self.processor.search('submitter_id', 38)
        self.processor.print_result(res)
        self.assertEqual(len(res), 3)
    
    def test_search_string(self):
        res = self.processor.search('_id', '436bf9b0-1147-4c0a-8439-6f79833bff5b')
        self.processor.print_result(res)
        self.assertEqual(len(res), 1)
        
    def test_search_bool(self):
        res = self.processor.search('has_incidents', 'true')
        self.processor.print_result(res)
        self.assertEqual(len(res), 99)
        
        