import urllib2
from datetime import datetime

from pyposterous.error import PyposterousError
from pyposterous.idl import METHODS
from pyposterous.parser import Parser
from pyposterous.utils import docstring_trim
from pyposterous.models import Tag
from pyposterous.auth import TwitterAuth, BasicAuth

def build_method(**conf):
    """
    Builds python functions based on the specified METHOD configuration
    """
    class MethodFactory(object):
        def __init__(self, api, args, kwargs):
            self.api = api
            self.args = []
            self.path = conf.get('path')
            self.params = conf.get('parameters', [])
            self.auth_required = conf.get('auth_required', False)
            self.twitter_auth_required = conf.get('twitter_auth_required', False)
            self.returns = conf.get('returns', [])
            
            # Raise an exception if authentication is required but credentials
            # are not specified
            if self.auth_required and not isinstance(self.api.auth, BasicAuth):
                raise PyposterousError("The API object's auth attribute most be an instance of pyposterous.auth.BasicAuth to use this method.")
            
            if self.auth_required and not (self.api.auth.username and self.api.auth.password):           
                raise PyposterousError('A username and password is required to use this method.')
                
            if self.twitter_auth_required and not isinstance(self.api.auth, TwitterAuth):
                raise PyposterousError("The API object's auth attribute most be an instance of pyposterous.auth.TwitterAuth to use this method.")
            
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
                        try:
                            value = kwargs.pop(name)
                        except:
                            pass
                    else:
                        raise TypeError("got multiple values for keyword argument '%s'" % name)
                
                # Make p_type a list if it isn't already.
                if type(p_type) is not tuple:
                    p_type = (p_type,)
                
                self.__verify_type(value, p_type, name)
                self.__verify_options(value, config, name)
                if value is not None:
                    self.__clean_and_set_value(name, value)
            
            if kwargs:
                raise TypeError("function got an unexpected keyword argument. %s" % kwargs)
                
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
            if value and not isinstance(value, p_type):
                raise TypeError("The value passed for '%s' is not valid. '%s' must be one of these: %s" % (name, name, p_type,))
            
            # If the value was something iterable, we need to make sure the
            # elements are of the appropriate type - no nested lists allowed.
            if type(value) is list:
                for a_value in value:
                    if not isinstance(a_value, p_type) or type(a_value) is list:
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
            if type(value) == datetime:
                value = "%s +0000" % value.strftime('%a, %d %b %Y %H:%M:%S').split('.')[0]
            
            if type(value) == bool:
                value = int(value)
            
            if type(value) == int:
                value = str(value)
            
            if type(value) == list:
                for val in value:
                    self.args.append(("%s[]" % name, val,))
                return 
            
            if type(value) == Tag:
                value = str(value)
            
            self.args.append((name, value,))
        
        def execute(self):
            import urllib2_file
            import base64
            
            # Anything with TEST in the URL is a test function, not a real API
            # call
            if 'TEST' in self.url:
                return None
            
            # urlopen doesn't like an empty list for 'data', so make it None
            if not self.args:
                self.args = None
            
            # Generate a request object
            req = self.api.auth.gen_request(self.url)
            
            try:
                resource = urllib2.urlopen(req, self.args)
            except (urllib2.HTTPError,), e:
                resource = e
            parser = Parser(self.api, resource, self.returns)
            
            data = parser.parse()
            resource.close()
            
            return data
            
    def _method(api, *args, **kwargs):
        method = MethodFactory(api, args, kwargs)
        return method.execute()
    _method.__doc__ = docstring_trim(conf.get('__doc__'))
    
    for param, types, config in conf.get('parameters', []):
        if 'page' == param:
            _method.pagination = True
            break
    
    return _method