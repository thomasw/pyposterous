import xml.etree.ElementTree as ET

class Parser(object):
    """This object is responsible for parsing the Pyposterous API data and 
    returning nice Python objects."""
    
    def __init__(self, resource):
        self.resource = resource
        self.xml = ET.parse(self.resource)
        self.output = []
        
    def parse(self):
        for element in self.xml.getroot().getchildren():
            self.output.append(self.build_object(element))
        
        output = self.output
        
        if len(self.output) == 1:
            output = self.output[0]
        
        if len(self.output) == 0:
            output = None
        
        return output
        

    def build_object(self, element):
        """Accepts an element tree element and builds an object based on the
        type."""
        return 'Object!'
