class Site(object):
    pass

class Post(object):
    pass

class Comment(object):
    pass

class Media(object):
    pass

# Posterous element -> class mapping
element_map = {
    'site':Site,
    'post':Post,
    'comment':Comment,
    'Media':Media,
    }