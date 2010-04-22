import types

import unittest

from pyposterous import API
from pyposterous.error import PyposterousError
from pyposterous.idl import METHODS

# Configuration 
# Posterous - Enter posterous credentials below
p_username = 'test'
p_password = 'test'

# Twitter - Enter Twitter credentials below
t_username = 'test'
t_password = 'test'


class PyposterousAPITests(unittest.TestCase):    
    def setUp(self):
        self.api = API(username=p_username, password=p_password)
    
    def test_method_creation(self):                
        for app_type in METHODS:
            for method in METHODS.get(app_type):
                self.assertTrue(hasattr(getattr(self.api, method), '__call__'))
                
    def test_method_required_params(self):
        # Has a required param
        try:
            self.api.test()
        except TypeError, e:
            if not "%s" % e == "'id' is required.":
                raise
        else:
            fail("Expected a TypeError")
           
        # has another required param
        try:
            self.api.test(id='yay')
        except TypeError, e:
            if not "%s" % e == "'test' is required.":
                raise
        else:
            fail("Expected a TypeError")
            
    def test_method_invalid_params(self):
        try:
            self.api.test(id=1)
        except TypeError, e:
            if not "%s" % e == "The value passed for 'id' is not valid. 'id' must be one of these: (<type 'str'>,)":
                raise
        else:
            fail("Expected a TypeError")
    
    def test_method_duplicate_values(self):
        try:
            self.api.test('asdf', id='asdf',)
        except TypeError, e:
            if not "%s" % e == "got multiple values for keyword argument 'id'":
                raise
        else:
            fail("Expected a TypeError")
    
    def test_method_too_many_values(self):
        try:
            self.api.test('asdf', 'asdf', 'asdf', 'asdf')
        except TypeError, e:
            if not "%s" % e == "function takes at most 4 arguments (5 given)":
                raise
        else:
            fail("Expected a TypeError")
    
    def test_method_invalid_list_value(self):        
        # Third parameter can only contain strings!
        try:
            self.api.test('asdf', 1, ['asdf', 1, 'asdf'],)
        except TypeError, e:
            if not "%s" % e == "One of the values passed for 'test1' is not valid. All values in 'test1' must be one of these: (<type 'str'>, <type 'list'>)":
                raise
        else:
            fail("Expected a TypeError")
    
    def test_method_auth_check(self):
        api = API()
        self.assertRaises(PyposterousError, api.test_auth_required)
    
    def test_method_valid_calls(self):
        self.api.test('test', 1,)
        self.api.test(id='test', test=1)
        self.api.test('test', test=1)
        
            
if __name__ == '__main__':
    unittest.main()