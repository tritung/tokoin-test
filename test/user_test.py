'''
Created on Dec 4, 2019

@author: TUNGTRUONG
'''
from unittest import TestCase

from tokoin.factory import SearchFactory


class TestUsers(TestCase):
    def setUp(self):
        self.processor = SearchFactory.get_search_processor('1')

    def test_search_field_found(self):
        res = self.processor.check_search_field('timezone')
        self.assertEqual(res, True)
        
    def test_search_field_not_found(self):
        res = self.processor.check_search_field('domain_names_test')
        self.assertEqual(res, False)
        
    def test_search_int(self):
        res = self.processor.search('_id', 1)
        self.processor.print_result(res)
        self.assertEqual(len(res), 1)
    
    def test_search_string(self):
        res = self.processor.search('name', 'Francisca Rasmussen')
        self.processor.print_result(res)
        self.assertEqual(len(res), 1)
        
    def test_search_tags(self):
        res = self.processor.search('tags', 'Foxworth')
        self.processor.print_result(res)
        self.assertEqual(len(res), 1)
        
    def test_search_bool(self):
        res = self.processor.search('verified', 'true')
        self.processor.print_result(res)
        self.assertEqual(len(res), 28)
        
        