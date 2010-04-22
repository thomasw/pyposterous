from pyposterous.error import PyposterousError
from pyposterous.utils import bool_string

class PosterousData(object):
    def __init__(self, api):
        self.api = api

class Site(PosterousData):    
    def get_tags(self):
        """Returns the tags for this site using self.id first and self.hostname
        second. If neither is specified, a PosterousError is raised."""
        try:
            return self.api.get_tags(site_id=self.id)
        except TypeError:
            try:
                return self.api.get_tags(hostname=self.hostname)
            except TypeError:
                raise PyposterousError('No ID or hostname has been specified for this site object.')

class Post(PosterousData):
    pass

class Comment(PosterousData):
    pass

class Media(PosterousData):
    pass

# Posterous element -> class mapping
element_map = {
    'site':Site,
    'post':Post,
    'comment':Comment,
    'Media':Media,
    }

# Attributes specified in the key are cleaned by the function specified in 
# the value
attribute_map = {
    ('id', 'views', 'filesize', 'height', 'width', 'commentscount', 'num_posts'):int,
    ('private', 'commentsenabled', 'primary'):bool_string,}