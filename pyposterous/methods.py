from pyposterous.error import PyposterousError
from pyposterous.idl import METHODS
from pyposterous.utils import docstring_trim

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