import types

import unittest

from pyposterous import API
from pyposterous.error import PyposterousError
from pyposterous.idl import METHODS

try:
    # Create a file called test_settings.py in the same dir as this file to 
    # override the settings in the except clause below. Use the except clause
    # as a template for your test_settings.py file
    # test_settings.py is in .gitignore, so it shouldn't be committed.
    from test_settings import p_username, p_password, t_username, t_password
except:    
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
    
    def test_method_invalid_kwarg(self):
        try:
            self.api.test_all_optional(1, yay=2,)
        except TypeError, e:
            if not "%s" % e == "function got an unexpected keyword argument. {'yay': 2}":
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
        self.api.test_all_optional(1, 'yay')
    
    # Test base API calls.
    def test_getsites(self):
        sites = self.api.get_sites()
        for site in sites:
            site.id
            site.name
            site.url
            site.private
            site.primary
            site.commentsenabled
            site.num_posts
        
    def test_readposts(self):
        posts = self.api.read_posts(site_id=1267571)
        for post in posts:
            post.url
            post.link
            post.title
            post.id
            post.body
            post.date
            post.views
            post.private
            post.author
            post.commentsenabled
        
    def test_gettags(self):
        sites = self.api.get_sites()
        for site in sites:
            tags = site.get_tags()
            for tag in tags:
                tag.id
                tag.tag_string
                tag.count
        else:
            if len(sites) == 0:
                self.api.get_tags(site_id=1267571)
    
    def test_newpost_getpost_updatepost_newcomment(self):
        body = "This is a test post."
        title = 'Test.'
        
        # Test new_post, get_post, and new_comment
        posted_post = self.api.new_post(body=body, title=title)
        
        new_comment = self.api.new_comment(posted_post.id, 'Great post!',)
        posted_post.new_comment('That wasn\'t very helpful!',)
        posted_post.new_comment('Great comment!', 'Jane Doe', 'test@test1.com')
        posted_post.new_comment('I hate you!',)        
        posted_post.new_comment('I love you!',)        
        read_post = self.api.get_post(id=posted_post.url.replace('http://post.ly/', ''))

        self.assertEqual(read_post.comments[0].author, 'pyposttest')
        self.assertEqual(read_post.comments[0].body, 'Great post!')
        self.assertEqual(read_post.comments[2].author, 'Jane Doe')
        self.assertEqual(read_post.comments[2].body, 'Great comment!')
        self.assertEqual(read_post.comments[-1].author, 'pyposttest')
        self.assertEqual(read_post.comments[-1].body, 'I love you!')        
        self.assertEqual(read_post.body.strip(), body)
        self.assertEqual(read_post.title, title)
        self.assertEqual(read_post.commentscount, 5)
        
        # Test update_post and get_post
        new_title = 'Test title.'
        new_body = 'Test body!'
        read_post.title = new_title
        read_post.body = new_body
        read_post.update_post()        
        read_post = self.api.get_post(id=posted_post.url.replace('http://post.ly/', ''))
        self.assertEqual(read_post.body.strip(), new_body)
        self.assertEqual(read_post.title, new_title)
    
    def test_upload(self):
        pass
    
    def test_uploadAndPost(self):
        pass
            
if __name__ == '__main__':
    unittest.main()
