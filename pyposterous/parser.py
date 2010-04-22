import xml.etree.ElementTree as ET

from pyposterous.error import PyposterousError
from pyposterous.models import element_map

class Parser(object):
    """This object is responsible for parsing the Pyposterous API data and 
    returning nice Python objects."""
    
    def __init__(self, api, resource, return_conf):
        self.api = api
        self.resource = resource
        self.return_conf = return_conf
        self.xml = ET.parse(self.resource)
        self.output = []
        
    def parse(self):
        for element in self.xml.getroot().getchildren():
            obj = self.build_object(element)
            if obj:
                self.output.append(obj)
        
        output = self.output
        
        if len(self.output) == 1 and 'force_list' not in self.return_conf:
            output = self.output[0]
        
        if len(self.output) == 0 and 'force_list' not in self.return_conf:
            output = None
        
        return output
        

    def build_object(self, element):
        """Accepts an element tree element and builds an object based on the
        type."""
        if element.tag == 'err':
            self.build_error(element)
        
        obj = element_map.get(element.tag)
        
        # Some Posterous calls don't seem to properly nest the XML. If the
        # returned base tag isn't one of our base types, just add it to the
        # last element parsed and hope for the best.
        # TODO: Post something to the Post. API discusssion group asking about
        # this.
        # Troublesome api calls: get_post
        if obj is None:
            if element_map.get(element.tag):
                prop_val = self.build_object(element)
            else:
                pro_val = element.text
            setattr(self.output[-1], element.tag, pro_val)
            
            return obj
            
        obj = obj(self.api)
        # Add properties for all of element's children        
        for prop in element.getchildren():
            if element_map.get(prop.tag):
                # If the element is one of our base types, we need to create
                # an object of it. This should only happen for media assets, so
                # we force it to be a list.
                if not hasattr(obj, prop.tag):
                    setattr(obj, prop.tag, [self.build_object(prop),])
                else:
                    getattr(obj, prop.tag).append(self.build_object(prop))
            else:
                # Base case - set a property called prop.tag in obj
                setattr(obj, prop.tag, self.clean_value(prop.tag, prop.text))
        
        return obj
    
    def build_error(self, element):
        """Throws a PyposterousError based on the element specified.
        """
        raise PyposterousError(element.get('msg'), element.get('code'))
    
    def clean_value(self, name, value):
        return value
