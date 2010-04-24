import xml.etree.ElementTree as ET

from pyposterous.error import PyposterousError
from pyposterous.models import element_map, attribute_map

class Parser(object):
    """This object is responsible for parsing the Pyposterous API data and 
    returning nice Python objects."""
    
    def __init__(self, api, resource, return_conf):
        self.api = api
        self.resource = resource
        self.return_conf = return_conf
        self.output = []
        
        # If the following is failing, either Posterous is giving us garbage
        # or there are connection issues occuring. Most likely connection issues.
        try:
            self.xml = ET.parse(self.resource)
        except:
            if self.resource.getcode() == 200:
                raise PyposterousError("malformed XML returned by Posterous")
            raise PyposterousError("%s connection error" % self.resource.getcode())
        
        
    def parse(self):
        for element in self.xml.getroot().getchildren():
            obj = self.build_object(element)
            if obj:
                # Okay. This is a little weird. When the Posterous API returns
                # results, it sometimes returns children elements as children
                # of their parent (e.g. comments as children of their post),
                # and sometimes they don't do that, and they just give 
                # everything as a big hairy list (e.g. both the post AND
                # its comments at the top level). TODO: Ask dev group about this
                
                # To fix this problem, I'm going to append subsequent elements
                # to the previous element returned if the types don't match.
                # 3 posts will return a list of 3 posts, 1 post and 2 comments
                # will return 1 post with a list of 2 comments as an attrib.
                
                try:
                    if type(obj) == type(self.output[-1]):
                        self.output.append(obj)
                    else:
                        attrib = "%ss" % (obj.__class__.__name__,)
                        attrib = attrib.lower()
                        
                        existing = getattr(self.output[-1], attrib, None)                        
                        if existing and type(existing) == list:
                            existing.append(obj)
                        elif not existing:
                            setattr(self.output[-1], attrib, [obj,])
                        else:
                            # If this happens, then my little XML inconsistency
                            # hack is overwritting a legitimate value.
                            raise PyposterousError("Posterous API response could not be parsed.")
                except IndexError:
                    # There was no previous element!
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
        tag = element.tag.lower()
        val = element.text
        
        if obj is None:
            if element_map.get(tag):
                prop_val = self.build_object(element)
            else:
                pro_val = val
            try:
                setattr(self.output[-1], tag, self.clean_value(tag, pro_val))
            except IndexError:
                # There was nothing in self.output - weird.
                pass
            return obj
            
        obj = obj(self.api)
        # Add properties for all of element's children        
        for prop in element.getchildren():
            prop_tag = prop.tag.lower()
            if element_map.get(prop_tag):
                # If the element is one of our base types, we need to create
                # an object of it. This should only happen for media assets, so
                # we force it to be a list.
                if not hasattr(obj, prop_tag):
                    setattr(obj, prop_tag, [self.build_object(prop),])
                else:
                    getattr(obj, prop_tag).append(self.build_object(prop))
            else:
                # Base case - set a property called prop.tag in obj
                setattr(obj, prop_tag, self.clean_value(prop_tag, prop.text))
        
        return obj
    
    def build_error(self, element):
        """Throws a PyposterousError based on the element specified.
        """
        raise PyposterousError(element.get('msg'), element.get('code'))
    
    def clean_value(self, name, value):
        for names in attribute_map:
            if name in names:
                return attribute_map.get(names)(value)
        return value
