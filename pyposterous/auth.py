import urllib2

class Auth(object):
    def gen_request(url):
        raise NotImplementedError

class BasicAuth(Auth):
    
    def __init__(self, username='', password=''):
        self.username = username
        self.password = password
        
    def gen_request(self, url):
        import base64
        
        req = urllib2.Request(url)
        
        if self.username and self.password:
            base64string =  base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
            authheader =  "Basic %s" % base64string
            req.add_header("Authorization", authheader)

        # We need to always supply the credentials because some of the
        # posterous API auth enabled calls optionally accept authentication,
        # but do not require authentication.
        # In those cases urllib2's PasswordMgr just won't supply the 
        # credentials and I can't figure how to force it to.
        # The block above this comment forces the credentials to be provided
        # if they are specified.
        # TODO: Fix the code below.
        
        #passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        #passman.add_password("Posterous", 'posterous.com', self.api.username, self.api.password)
        #authhandler = urllib2.HTTPBasicAuthHandler(passman)
        #opener = urllib2.build_opener(authhandler)
        #urllib2.install_opener(opener)
        
        return req
        