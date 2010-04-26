from pyposterous.error import PyposterousError
from pyposterous.utils import parse_date

class PosterousData(object):
    def __init__(self, api):
        self.__api = api
    
    def api(self):
        return self.__api

class Site(PosterousData):    
    def get_tags(self):
        """Returns the tags for this site using self.id first and self.hostname
        second. If neither is specified, a PosterousError is raised."""
        try:
            return self.api().get_tags(site_id=self.id)
        except AttributeError:
            try:
                return self.api().get_tags(hostname=self.hostname)
            except AttributeError:
                raise PyposterousError('No ID or hostname has been specified for this site object.')
                
    def read_posts(self, num_posts=None, page=None, tag=None):
        """Returns a list of posts for this site using self.id."""
        try:
            return self.api().read_posts(site_id=self.id, num_posts=num_posts, page=page, tag=tag)
        except AttributeError:
            try:
                return self.api().read_posts(hostname=self.hostname, num_posts=num_posts, page=page, tag=tag)
            except AttributeError:
                raise PyposterousError('No ID or hostname has been specified for this site object.')
            
    
    def new_post(self, media=None, title=None, body=None, autopost=None, private=None, date=None, tags=None, source=None, sourceLink=None):
        """Posts a new blog post to this site using self.id"""
        try:
            return self.api().new_post(self.id, media, title, body, autopost, private, date, tags, source, sourceLink)
        except AttributeError:
            raise PyposterousError('No ID has been specified for this site object.')

class Tag(PosterousData):
    def __str__(self):
        try:
            return self.tag_string
        except AttributeError:
            return ''

class Post(PosterousData):
    def update_post(self, media=None):
        """Updates the post this object represents based on the values of 
        post_id, title, and body.
        
        media -- a file or a list of files to APPEND to the existing post.
        """
        kwargs = {}
        try:
            kwargs['post_id'] = self.id
        except:
            raise PyposterousError('No post_id specified for this Post object.')
        
        try:
            kwargs['title'] = self.title
        except AttributeError:
            pass
            
        try:
            kwargs['body'] = self.body
        except AttributeError:
            pass
        
        if media: kwargs['media'] = media
            
        return self.api().update_post(**kwargs)
        
    def new_comment(self, body, name=None, email=None, date=None):
        return self.api().new_comment(self.id, body, name, email, date)

class Comment(PosterousData):
    pass

class Media(PosterousData):
    pass

class Image(PosterousData):
    pass

# Posterous element -> class mapping
element_map = {
    'site':Site,
    'post':Post,
    'comment':Comment,
    'media':Media,
    'thumb':Image,
    'medium':Image,
    'tag':Tag,
    }

# Attributes specified in the key are cleaned by the function specified in 
# the value
attribute_map = {
    ('id', 'views', 'filesize', 'height', 'width', 'commentscount', 'num_posts',):int,
    ('private', 'commentsenabled', 'primary'):lambda x: x.upper() == 'TRUE',
    ('body',):lambda x: x.strip(), # Hopefully whitespace will not be significant. 
    ('date',):lambda x: parse_date(x),} 
    