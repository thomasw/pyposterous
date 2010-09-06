from pyposterous.error import PyposterousError
from pyposterous.utils import parse_date, try_parse_int

class PosterousData(object):
    def __init__(self, api):
        self.__api = api
    
    def api(self):
        return self.__api

class Site(PosterousData):    
    def get_tags(self):
        """Returns the tags for this site using self.id first and self.hostname
        second. If neither is specified, a PosterousError is raised.
        
        """
        try:
            return self.api().get_tags(site_id=self.id)
        except AttributeError:
            try:
                return self.api().get_tags(hostname=self.hostname)
            except AttributeError:
                raise PyposterousError('No ID or hostname attributes have been defined for this site instance.')
                
    def read_posts(self, num_posts=None, page=None, tag=None):
        """Returns a list of posts for this site using self.id or self.hostname.
        If niether is specified a PyposterousError is raised.
        
        See pyposterous.API.read_posts for parameter documentation.
        
        """
        try:
            return self.api().read_posts(site_id=self.id, num_posts=num_posts, page=page, tag=tag)
        except AttributeError:
            try:
                return self.api().read_posts(hostname=self.hostname, num_posts=num_posts, page=page, tag=tag)
            except AttributeError:
                raise PyposterousError('No ID or hostname attributes have been defined for this site instance.')
            
    
    def new_post(self, media=None, title=None, body=None, autopost=None, private=None, date=None, tags=None, source=None, sourceLink=None):
        """Posts a new blog post to this site using self.id. If self.id isn't
        specified, a PyposterousError is raised.
        
        See pyposterous.API.new_post for parameter documentation.
        
        """
        try:
            return self.api().new_post(self.id, media, title, body, autopost, private, date, tags, source, sourceLink)
        except AttributeError:
            raise PyposterousError('No id attribute defined for this site instance.')

class Tag(PosterousData):
    def __str__(self):
        try:
            return self.tag_string
        except AttributeError:
            return ''

class Post(PosterousData):
    def update_post(self, media=None):
        """Updates the post this object represents based on the values of 
        self.id, self.title, and self.body. If self.id isn't specified, a
        PyposterousError is raised.
        
        media -- a file or a list of files to APPEND to the existing post.
        
        """
        kwargs = {}
        try:
            kwargs['post_id'] = self.id
        except:
            raise PyposterousError('No id attribute defined for this post instance.')
        
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
        """Posts a new comment to this post using the value of self.id. If self.id
        isn't specified, a PyposterousError is raised.
        
        This method is compatible with the Cursor class.
        
        See pyposterous.API.new_comment for parameter documentation.
        
        """
        try:
            self.id
        except AttributeError:
            raise PyposterousError('No id attribute defined for this post instance.')
            
        return self.api().new_comment(self.id, body, name, email, date)
    new_comment.pagination=True

class Comment(PosterousData):
    pass

class Media(PosterousData):
    pass

class Image(PosterousData):
    pass

class User(PosterousData):
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
    'image':Image,
    'user':User
    }

# Attributes specified in the key are cleaned by the function specified in 
# the value
attribute_map = {
    ('id'):lambda x: try_parse_int(x),
    ('views', 'filesize', 'height', 'width', 'commentscount', 'num_posts', 'size', ):int,
    ('private', 'commentsenabled', 'primary'):lambda x: x.upper() == 'TRUE',
    ('body',):lambda x: x.strip(), # Hopefully whitespace will not be significant. 
    ('timestamp',):lambda x: parse_date(x, '%a %b %d %H:%M:%S %Y'),
    ('date',):lambda x: parse_date(x),} 
    