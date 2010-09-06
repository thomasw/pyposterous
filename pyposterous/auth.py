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
        
class TwitterAuth(Auth):
    
    def __init__(self, consumer_key, consumer_secret, token_key, token_secret, xauth_sp='https://api.twitter.com/1/account/verify_credentials.json'):
        import oauth2 as oauth
        
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        
        self.token_key = token_key
        self.token_secret = token_secret
        self.token = oauth.Token(key=token_key, secret=token_secret)
        
        self.xauth_sp = xauth_sp
        self.version = '1.0'
        
    def gen_request(self, url):
        req = urllib2.Request(url)
        
        req.add_header("X-Auth-Service-Provider", self.xauth_sp)
        req.add_header("X-Verify-Credentials-Authorization", self.__build_verify_credentials_string())
        
        return req
    
    def __build_verify_credentials_string(self):
        import oauth2 as oauth
        import time
        
        # Setting up a signed oauth2 Request object generates a solid verify
        # credentials string, so we'll let it do the hard stuff for us.
        params = oauth.Request(method="GET", url=self.xauth_sp, \
            parameters = {
                'oauth_version': self.version,
                'oauth_nonce': oauth.generate_nonce(),
                'oauth_timestamp': int(time.time()),
                'oauth_token': self.token.key,
                'oauth_consumer_key': self.consumer.key,
            })
        params.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        
        # Our verify credentials string is accessed via the 'Authorization'
        # key. It has a bonus realm="" in it, so we remove that before we 
        # return it.
        return params.to_header()['Authorization'].replace(' realm="",', '')

    def __unicode__(self):
        return self.__build_verify_credentials_string()