from pyposterous.error import PyposterousError

class PosterousData(object):
    def __init__(self, api):
        self.api = api

class Site(PosterousData):    
    def get_tags(self):
        """Call get_tags with either self.id or self.hostname. If neither are present,
        raise an error."""
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