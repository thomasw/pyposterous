import types

from pyposterous.error import PyposterousError
from pyposterous.methods import build_method
from pyposterous.methods import METHODS

class API(object):
    """Posterous API"""    
    def __init__(self, username='', password='', host='posterous.com'):
        self.username = username
        self.password = password
        self.host = host
        
        # Add API methods based on the IDL.
        self.__build_methods('application')
        self.__build_methods('post.ly')
        self.__build_methods('twitter')
    
    def __build_methods(self, method_subsection):
        """Add a bound method to this object for each method defined in the 
        specified method_subsection of METHODS. """
        for method_name in METHODS.get(method_subsection, {}):
            config = METHODS.get(method_subsection, {}).get(method_name)
            method = build_method(**config)
            self.__setattr__(method_name, types.MethodType(method, self, API))

    
