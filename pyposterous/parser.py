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
        # This is to handle the twitter api calls specifically.
        if 'force_primative' in self.return_conf:
            self.output = {}
            for x in self.xml.getroot().getchildren():
                if x.tag != 'err':
                    self.output[x.tag.lower()] = x.text 
            if self.output:
                return self.output
            else:
                # if self.output is empty, then an error occured and we'll
                # just let it continue on to the code below for it to be
                # caught and thrown.
                self.output = []          
        
        root = self.xml.getroot()
        # Some V2 api calls return the output as the root of the document.
        # this should handle those cases.
        if root.tag in element_map:
            self.output.append(self.build_object(root))
        else:
            # v1 stuff.
            for element in root.getchildren():
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
                            attrib = obj.__class__.__name__.lower()
                        
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
        
        self.output = self.clean_up(self.output)
        output = self.output
        
        if len(self.output) == 1 and 'force_list' not in self.return_conf:
            output = self.output[0]
        
        if len(self.output) == 0 and 'force_list' not in self.return_conf:
            output = None
        
        return output
        

    def build_object(self, element):
        """Accepts an element tree element and builds an object based on the
        type."""
        if element.tag == 'err' or element.tag == 'error':
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
            
            # If the element doesn't have any chidlren, using the element map obj
            # will hide the returned data. We don't want that. Most notably, this 
            # occurs when a post has a video attached to it. The thumb attribute
            # is typically an Image object, but in the case of the video media
            # element it's just a URL. The "and prop.getchildren()" should
            # prevent Pyposterous from doing a conversion to an object for this
            # anomalous data.
            
            if element_map.get(prop_tag) and prop.getchildren():
                # If the element is one of our base types, we need to create
                # an object of it.
                existing = getattr(obj, prop_tag, None)
                if not existing:
                    setattr(obj, prop_tag, self.build_object(prop),)
                elif type(existing) == list:
                    getattr(obj, prop_tag).append(self.build_object(prop))
                else:
                    setattr(obj, prop_tag, [existing,])
                    getattr(obj, prop_tag).append(self.build_object(prop))
            else:
                # Base case - set a property called prop.tag in obj
                setattr(obj, prop_tag, self.clean_value(prop_tag, prop.text))
        
        return obj
    
    def clean_up(self, obj):
        """Preforms some miscellaneous cleanup for attribute names that
        aren't quite right."""

        def clean_it(obj):
            # Rename comment list to 'comments' and force it to be a list.
            try:
                if obj.comment:
                    obj.comments = obj.comment
                    del obj.comment
                if not type(obj.comments) == list:
                    obj.comments = [obj.comments,]
            except AttributeError:
                pass
        
            # Force media to be a list.
            try:
                if not type(obj.media) == list:
                    obj.media = [obj.media,]
            except AttributeError:
                pass
            return obj
        
        
        if type(obj) == list:
            obj = [clean_it(x) for x in obj]
        else:
            obj = clean_it(obj)
        
        return obj
                    
    def build_error(self, element):
        """Throws a PyposterousError based on the element specified.
        """
        # This handles v1 api errors (business as usual)
        if element.tag == 'err':
            raise PyposterousError(element.get('msg'), element.get('code'))
        
        # Api v2 errors are formatted differently than API v1 errors. This is
        # dirty, but it'll prase them.
        message = "Unknown"
        code = "Unknown"
        for child in element.getchildren():
            if child.tag == "message":
                message = child.text
            
            if child.tag == "code":
                code = child.text
                
        raise PyposterousError("%s" % message, "%s" % code)
    
    def clean_value(self, name, value):
        for names in attribute_map:
            if name in names:
                return attribute_map.get(names)(value)
        return value
