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
    def update_post(self, media=None):
        """Updates the post this object represents based on the values of 
        post_id, title, and body.
        
        media -- a list of files to upload to the existing post.
        """
        kwargs = {}
        try:
            kwargs['post_id'] = self.id
        except:
            raise PyposterousError('No post_id specified for this Post object.')
        
        if self.title:
            kwargs['title'] = self.title
        
        if self.body:
            kwargs['body'] = self.body
            
        return self.api.update_post(**kwargs)
        
    def new_comment(self, body, name=None, email=None, date=None):
        return self.api.new_comment(self.id, body, name, email, date)

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
    ('id', 'views', 'filesize', 'height', 'width', 'commentscount', 'num_posts',):int,
    ('private', 'commentsenabled', 'primary'):bool_string,
    ('body',):lambda x: x.strip()} # Hopefully whitespace will not be significant. 