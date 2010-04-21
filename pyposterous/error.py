class PyposterousError(Exception):
    """Pyposterous exception that accepts an optional posterous error code."""
    def __init__(self, error, error_code=None):
        self.error_message = error
        self.error_code = error_code

    def __str__(self):        
        if error_code:
            return "%s - %s" % (self.error_code, self.error_message)
        
        return self.error_message

