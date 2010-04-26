from datetime import datetime

from pyposterous.models import Tag

# Posterous IDL
METHODS = {
    # Base read and write Methods
    'application': {
        'get_sites': {
            'path':'/api/getsites',
            'parameters':(),
            'auth_required':True,
            'returns': ['force_list',],
            '__doc__':"""Returns a list of all sites owned and authored by
            this user.
            """
        },
        'read_posts': {
            'path':'/api/readposts',
            'parameters':[
                ('site_id', int, ['optional']),
                ('hostname', str, ['optional']),
                ('num_posts', int, ['optional']),
                ('page', int, ['optional']),
                ('tag', (str, Tag), ['optional'])],
            'auth_required':False,
            'returns': ['force_list',],
            '__doc__':"""Returns a list of posts based on the specified 
            parameters.
            
            Keyword arguments:
            site_id -- Optional. Id of the site to read from
            hostname -- Optional. Subdomain of the site to read from
            num_posts -- Optional. How many posts you want. Default is 10, max is 50
            page -- Optional. What 'page' you want (based on num_posts). Default is 1
            tag -- Optional
            
            """
        },
        'get_tags': {
            'path':'/api/gettags',
            'parameters':[
                ('site_id', int, ['optional']),
                ('hostname', str, ['optional'])],
            'auth_required':False,
            'returns': ['force_list',],
            '__doc__':"""Returns a list of tags based on the specified 
            site.
            
            Keyword arguments:
            site_id -- Optional. Id of the site to read from
            hostname -- Optional. Subdomain of the site to read from
            
            """
        },
        'new_post':{
            'path':'/api/newpost',
            'parameters':[
                ('site_id', int, ['optional']),
                ('media', (file, list), ['optional']),
                ('title', str, ['optional']),
                ('body', str, ['optional']),
                ('autopost', bool, ['optional']),
                ('private', bool, ['optional']),
                ('date', datetime, ['optional']),
                ('tags', str, ['optional']),
                ('source', str, ['optional']),
                ('sourceLink', str, ['optional']),
            ],
            'auth_required':True,
            '__doc__':"""Creates a new post.
            
            Keyword arguments:
            site_id -- Optional. Id of the site to post to. If not supplied, posts to the user's default site
            media -- Optional. File object for single file or a list of file objects.
            title -- Optional. Title of post
            body -- Optional. Body of post
            autopost -- Optional. 0 or 1.
            private -- Optional. 0 or 1.
            date -- Optional. In GMT. Any parsable format. Cannot be in the future.
            tags -- Optional. Comma separate tags
            source -- Optional. The name of your application or website
            sourceLink -- Optional. Link to your application or website
                   
            """
        },
        'update_post':{
            'path':'/api/updatepost',
            'parameters':[
                ('post_id', int, []),
                ('media', (file, list), ['optional']),
                ('title', str, ['optional']),
                ('body', str, ['optional']),
            ],
            'auth_required':True,
            '__doc__':"""Updates an existing post.
            
            Keyword arguments:
            post_id -- Id of the post to update.
            media -- Optional. File object for single file or a list of file objects. Will append to post.
            title -- Optional. Title of post. Will update post if present.
            body -- Optional. Body of post. Will update post if present.
            
            """
        },
        'new_comment':{        
            'path':'/api/newcomment',
            'parameters':[
                ('post_id', int, []),
                ('comment', str, []),
                ('name', str, ['optional']),
                ('email', str, ['optional']),
                ('date', datetime, ['optional']),
            ],
            'auth_required':True,
            '__doc__':"""Adds a comment to the specified post.
            
            Keyword arguments:
            post_id -- The post id to comment on
            comment -- The comment body
            name -- Optional. The name to use
            email -- Optional. The email address to use
            date -- Optional. In GMT. Any parsable format. Cannot be in the future.
            
            """
        },
    },
    # http://post.ly related methods
    'post.ly': {
        'get_post':{
            'path':'/api/getpost',
            'parameters':[
                ('id', str, []),
            ],
            'auth_required':False,
            '__doc__':"""Retrieve a post object based on a http://post.ly shortcode
            
            Keyword arguments:
            id -- Post.ly shortcode. (Example: 123abc in http://post.ly/123abc) 
            
            """
        },
    },
    # Twitter auth methods
    'twitter': {
        'upload':{
            'path':'/api/upload',
            'parameters':[
                ('username', str, []),
                ('password', str, []),
                ('media', (file, list), ['optional']),
                ('message', str, ['optional']),
                ('body', str, ['optional']),
                ('source', str, ['optional']),
                ('sourceLink', str, ['optional']),            
            ],
            'auth_required':False,
            'returns':['force_primative',],
            '__doc__':"""Post text and files on Posterous using Twitter credentials.
            
            Keyword arguments:
            username -- Twitter username
            password -- Twitter password
            media -- Optional. File object for single file or a list of file objects.
            message -- Optional. Title of post
            body -- Optional. Body of post
            source -- Optional. The name of your application or website
            sourceLink -- Optional. Link to your application or website            
            
            """   
        },
        'upload_and_post':{
            'path':'/api/uploadAndPost',
            'parameters':[
                ('username', str, []),
                ('password', str, []),
                ('media', (file, list), ['optional']),
                ('message', str, ['optional']),
                ('body', str, ['optional']),
                ('source', str, ['optional']),
                ('sourceLink', str, ['optional']),            
            ],
            'auth_required':False,
            'returns':['force_primative',],
            '__doc__':"""Post text and files on Posterous using Twitter 
            credentials and then tweet a message with a link to the post.
            
            Keyword arguments:
            username -- Twitter username
            password -- Twitter password
            media -- Optional. File object for single file or a list of file objects.
            message -- Optional. Title of post
            body -- Optional. Body of post
            source -- Optional. The name of your application or website
            sourceLink -- Optional. Link to your application or website            
            
            """        
        },
    },
    # NOT REAL API CALLS - used for testing.
    'test': {
        'test':{
            'path':'TEST',
            'parameters':[
                ('id', str, []),
                ('test', int, []),
                ('test1', (str, list), ['optional']),         
            ],
            'auth_required':False,
            '__doc__':"Not a real API call. Only used by the unit tests.",
        },
        'test_auth_required':{
            'path':'TEST',
            'parameters':[],
            'auth_required':True,
            '__doc__':"Not a real API call. Only used by the unit tests.",
        },
        'test_all_optional':{
            'path':'TEST',
            'parameters':[
                ('id', int, ['optional']),
                ('test', str, ['optional']),
            ],
            'auth_required':False,
            '__doc__':"Not a real API call. Only used by the unit tests.",
        }
    }
}