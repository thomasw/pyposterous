import sys

from pyposterous.error import PyposterousError

def build_method(**conf):
    """
    Builds python functions based on the specified METHOD configuration
    """
    class MethodFactory(object):
        path = conf.get('path')
        params = conf.get('parameters')
        auth_required = conf.get('auth_required')
        args = {}
        
        def __init__(self, api, args, kwargs):
            self.api = api

            # Raise an exception if authentication is required but credentials
            # are not specified
            if self.auth_required and not (self.api.username and self.api.password):           
                raise PyposterousError('Authentication is required to use this method.')
            
            self.url = "http://%s%s" % (self.api.host, self.path)
            self.__verify_args(list(args), kwargs)
        
        def __verify_args(self, args, kwargs):
            """Check to make sure that the specified arguments are appropriate
            given this API call's definition."""
            if len(self.params) < len(args)+len(kwargs):
                raise TypeError("function takes at most %s arguments (%s given)" % (len(self.params)+1, len(args)+len(kwargs)+1))
            
            # Reverse args so I can use pop -- reverse happens in place!
            args.reverse()
            
            for name, p_type, config in self.params:
                # Check for positional and a keyword argument, raise error if
                # there is an overlapping value
                value = None
                if args:
                    value = args.pop()
                
                if name in kwargs:
                    if not value:
                        value = kwargs.get(name)
                    else:
                        raise TypeError("got multiple values for keyword argument '%s'" % name)
                
                # Make p_type a list if it isn't already.
                if type(p_type) is not tuple:
                    p_type = (p_type,)

                self.__verify_type(value, p_type, name)
                self.__verify_options(value, config, name)
                self.__clean_and_set_value(name, value)
                
        def __verify_type(self, value, p_type, name):
            """Check to make sure that the type of the value specified is in 
            the accepted type list.
            
            Keyword arguments:
            value -- the value that we'll check the type of
            p_type -- a list of acceptable types
            name -- the name of the argument we're checking
            
            Returns True if succesful, throws a TypeError if not.
            """
            # Check to make sure that value is the right type.
            if value and type(value) not in p_type:
                raise TypeError("The value passed for '%s' is not valid. '%s' must be one of these: %s" % (name, name, p_type,))
            
            # If the value was something iterable, we need to make sure the
            # elements are of the appropriate type - no nested lists allowed.
            if type(value) is list:
                for a_value in value:
                    if type(a_value) not in p_type or type(a_value) is list:
                        raise TypeError("One of the values passed for '%s' is not valid. All values in '%s' must be one of these: %s" % (name, name, p_type))
            return True
        
        def __verify_options(self, value, config, name):
            """Raise type errors if the options defined by conifg are not
            satisfied.
            
            Keyword arguments:
            value -- the value to be checked
            config -- a list of configuration options: 'optional' is the only option implemented right now
            name -- the name of the parameter we're doing a check for right now.
            
            Returns True if succesful, throws a TypeError if not.
            """
            if 'optional' not in config and value is None:
                raise TypeError("'%s' is required." % name)
            
            return True
        
        def __clean_and_set_value(self, name, value):            
            self.args[name] = value
        
        def execute(self):
            return "Executing %s" % self.url
            
    def _method(api, *args, **kwargs):
        method = MethodFactory(api, args, kwargs)
        return method.execute()
    _method.__doc__ = docstring_trim(conf.get('__doc__'))
    
    return _method

def docstring_trim(docstring):
    """A docstring normalization function taken straight from PEP 257 at
    http://www.python.org/dev/peps/pep-0257/ 
    
    docstring -- the string to be normalized
    
    """
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

# Posterous IDL
METHODS = {
    # Base read and write Methods
    'application': {
        'get_sites': {
            'path':'/api/getsites',
            'parameters':(),
            'auth_required':True,
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
                ('tag', str, ['optional'])],
            'auth_required':False,
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
                ('media', (str, list), ['optional']),
                ('title', str, ['optional']),
                ('body', str, ['optional']),
                ('autopost', bool, ['optional']),
                ('private', bool, ['optional']),
                ('date', str, ['optional']),
                ('tags', str, ['optional']),
                ('source', str, ['optional']),
                ('sourceLink', str, ['optional']),
            ],
            'auth_required':True,
            '__doc__':"""Creates a new post.
            
            Keyword arguments:
            site_id -- Optional. Id of the site to post to. If not supplied, posts to the user's default site
            media -- Optional. File data for single file or a list of files
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
                ('media', (str, list), ['optional']),
                ('title', str, ['optional']),
                ('body', str, ['optional']),
            ],
            'auth_required':True,
            '__doc__':"""Updates an existing post.
            
            Keyword arguments:
            post_id -- Id of the post to update.
            media -- Optional. File data for single file or a list of files. Will append to post.
            title -- Optional. Title of post. Will update post if present.
            body -- Optional. Body of post. Will update post if present.
            
            """
        },
        'new_comment':{        
            'path':'/api/newcomment',
            'parameters':[
                ('post_id', str, []),
                ('comment', str, []),
                ('name', str, ['optional']),
                ('email', str, ['optional']),
                ('date', str, ['optional']),
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
                ('media', (str, list), ['optional']),
                ('message', str, ['optional']),
                ('body', str, ['optional']),
                ('source', str, ['optional']),
                ('sourceLink', str, ['optional']),            
            ],
            'auth_required':False,
            '__doc__':"""Post text and files on Posterous using Twitter credentials.
            
            Keyword arguments:
            username -- Twitter username
            password -- Twitter password
            media -- Optional. File data for single file or a list of files.
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
                ('media', (str, list), ['optional']),
                ('message', str, ['optional']),
                ('body', str, ['optional']),
                ('source', str, ['optional']),
                ('sourceLink', str, ['optional']),            
            ],
            'auth_required':False,
            '__doc__':"""Post text and files on Posterous using Twitter 
            credentials and then tweet a message with a link to the post.
            
            Keyword arguments:
            username -- Twitter username
            password -- Twitter password
            media -- Optional. File data for single file or a list of files.
            message -- Optional. Title of post
            body -- Optional. Body of post
            source -- Optional. The name of your application or website
            sourceLink -- Optional. Link to your application or website            
            
            """        
        },
    },
    # NOT REAL API CALLS - usedd for testing.
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
    }
}