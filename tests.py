import types
import time
import unittest

from pyposterous import API, Cursor
from pyposterous.error import PyposterousError
from pyposterous.idl import METHODS

try:
    # Create a file called test_settings.py in the same dir as this file to 
    # override the settings in the except clause below. Use the except clause
    # as a template for your test_settings.py file
    # test_settings.py is in .gitignore, so it shouldn't be committed.
    from test_settings import *
except:    
    # Posterous - Enter posterous credentials below
    p_username = 'test'
    p_password = 'test'
    name_of_first_blog = 'pyposttest'

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
            if not "%s" % e == "The value passed for 'id' is not valid. 'id' must be one of these: (<type 'basestring'>,)":
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
            if not "%s" % e == "One of the values passed for 'test1' is not valid. All values in 'test1' must be one of these: (<type 'basestring'>, <type 'list'>)":
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
        sites[0].new_post(title="post_object_test", body="hurray!")
        
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
        from datetime import datetime, timedelta
        
        body = "This is a test post."
        title = 'Test.'
        date = datetime.now()+timedelta(hours=4)
        # Test new_post, get_post, and new_comment
        posted_post = self.api.new_post(body=body, title=title, date=date)
        
        new_comment = self.api.new_comment(posted_post.id, 'Great post!',)
        posted_post.new_comment('Great comment!', 'Jane Doe', 'test@test1.com')
        posted_post.new_comment('I hate you!',)
        read_post = self.api.get_post(id=posted_post.url.replace('http://post.ly/', ''))
        
        # Test Comments
        self.assertEqual(read_post.comments[0].author, name_of_first_blog)
        self.assertEqual(read_post.comments[0].body, 'Great post!')
        self.assertEqual(read_post.comments[1].author, 'Jane Doe')
        self.assertEqual(read_post.comments[1].body, 'Great comment!')
        self.assertEqual(read_post.comments[2].author, name_of_first_blog)
        self.assertEqual(read_post.comments[2].body, 'I hate you!')
        self.assertEqual(read_post.commentscount, 3)
        
        # Test Post Content
        self.assertEqual(read_post.body.strip(), body)
        self.assertEqual(read_post.title, title)
        #self.assertEqual(read_post.date.strftime('%a, %d %b %Y %H:%M:%S'), date.strftime('%a, %d %b %Y %H:%M:%S'))
        # The above will faill because Posterous isn't handling incomming API times as GMT like their docs state
        
        # Test update_post and get_post
        new_title = 'Test title.'
        new_body = 'Test body!'
        read_post.title = new_title
        read_post.body = new_body
        read_post.update_post()        
        read_post = self.api.get_post(id=posted_post.url.replace('http://post.ly/', ''))
        self.assertEqual(read_post.body.strip(), new_body)
        self.assertEqual(read_post.title, new_title)
    
    def test_new_post_single_media(self):
        # An Image!
        test_file = open('test_assets/1.jpg')
        post = self.api.new_post(title='Testing single file upload', media=test_file)
        test_file.close()
        
        # A Word Doc! - Not sure why this fails
        #test_file = open('test_assets/test.docx')
        #post = self.api.new_post(title='Testing doc upload', media=test_file)
        #test_file.close()
        
        # A PDF!        
        test_file = open('test_assets/test.pdf')
        post.title = "%s - and then adding another file to it!" % post.title
        post.update_post(media=test_file)
        test_file.close()
    
    def test_new_post_with_multi_media_and_comments(self):
        from os import listdir, path
        images = [open(path.join('test_assets', fname)) for fname in listdir('test_assets') if '.jpg' in fname]
        
        # Post the images and close them
        title = 'Multi-file upload test!'
        post = self.api.new_post(title=title, media=images)
        [image.close() for image in images]
        
        # Post some comments
        comment_text1 = "Hello, world!"
        comment_text2 = "Hello, world! x 2"
        post.new_comment(comment_text1)
        post.new_comment(comment_text2)
        
        # Get the post data
        full_post_data = self.api.get_post(post.url.replace('http://post.ly/', ''))
        
        self.assertEqual(len(images), len(full_post_data.media))
        self.assertEqual(full_post_data.title, 'Multi-file upload test!')
        self.assertEqual(len(full_post_data.comments), 2)
        self.assertEqual(full_post_data.comments[0].body, comment_text1)
        self.assertEqual(full_post_data.comments[1].body, comment_text2)
        
    def test_upload(self):
        from pyposterous.auth import TwitterAuth
        
        api = API(auth=TwitterAuth(consumer_key, consumer_secret, user_key, user_secret))
        
        images = [open('test_assets/1.jpg'), open('test_assets/2.jpg'),]
        title = 'Check out this awesome media'
        body = 'AWESOME.'
        source = 'Pyposterous'
        sourceLink = 'http://github.com/thomasw/pyposterous'
        
        post = api.upload(images, title, body, source, sourceLink)
        
        retrieved = api.get_post(post.id)
        
        self.assertEqual(title, retrieved.title)
        self.assertEqual(len(retrieved.media), len(images))
        self.assertEqual(retrieved.title, post.text)
    
    def test_cursor(self):
        results = []
        limit = 40
        for post in Cursor(method=self.api.read_posts, start_page=5, num_posts=10, limit=limit, parameters={'hostname':name_of_first_blog,}):
            results.append("%s -- %s" % (post.title, post.url))
        
        #print results
        
        # This should return limit posts
        self.assertEqual(limit, len(results))
        
        # self.api.get_sites does not support pagination
        self.assertRaises(PyposterousError, Cursor, {'method':self.api.get_sites})
        
        # You can't pass page or num_posts as parameters
        self.assertRaises(PyposterousError, Cursor, {'method':self.api.read_posts, 'parameters':{'hostname':name_of_first_blog,'page':4},})
        self.assertRaises(PyposterousError, Cursor, {'method':self.api.read_posts, 'parameters':{'hostname':name_of_first_blog,'num_posts':4},})
            
if __name__ == '__main__':
    unittest.main()
