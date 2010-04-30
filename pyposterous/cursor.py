from pyposterous.error import PyposterousError

class Cursor(object):
    """Allows for iterating over multiple pages of Posterous results.
    
    Keyword arguments:
    
    * method -- The method with paginated results
    * num_posts -- (Optional) The number of posts to request from posterous per page
    * start_page -- (Optional) The page to start on.
    * limit -- (Optional) Only return LIMIT results.
    * parameters -- (Optional) parameters you'd like to pass to the specified method
    
    """
    def __init__(self, method, num_posts=20, start_page=1, limit=0, parameters={}):
        # pagination will be equal to true if this method supports it
        if not getattr(method, 'pagination', False):
            raise PyposterousError('This method does not support pagination.')
            
        self.parameters = parameters
        self.num_posts = num_posts
        self.method = method
        self.start_page = start_page
        self.current_page = start_page
        self.iter_items = []
        self.done = False
        
        self.returned_count = 0
        self.limit = limit
        
        if self.parameters.pop('page', None) or self.parameters.pop('num_posts', None):
            raise PyposterousError('When using a cursor object, you shouldn\'t specify a page or num_posts for the function. The Cursor object does that for you.')
        
    def __iter__(self):
        return self
    
    def next(self):
        # Get more items from posterous
        if not self.done and not self.iter_items and (not self.limit or self.limit > self.returned_count):
            self.iter_items = self.method(page=self.current_page, num_posts=self.num_posts, **self.parameters)
            self.current_page += 1
        
            if len(self.iter_items) < self.num_posts:
                self.done = True
        
        # Return one item
        if self.iter_items and (not self.limit or self.limit > self.returned_count):
            self.returned_count += 1
            return self.iter_items.pop()
            
        # Reset stuff
        self.current_page = self.start_page
        self.done = False
        self.returned_count = 0
        self.iter_items = []
        
        raise StopIteration        