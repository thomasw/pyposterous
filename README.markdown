# Pyposterous
Pyposterous is a wrapper for the [Posterous API](http://posterous.com/api) written in Python.

Currently (9/6/2010), Pyposterous has 100% API coverage.

## Install

You can install Pyposterous with setuptools:

    > git clone git://github.com/thomasw/pyposterous.git
    > cd pyposterous
    > sudo python setup.py install

Alternatively, just put the pyposterous subdirectory of this repo somewhere on your Python path. If you do it this way, you may also need to grab:

* [urllib2_file](http://github.com/seisen/urllib2_file)
* [ElementTree](http://effbot.org/zone/element-index.htm) (included in Python >2.5)
* [oauth2](http://github.com/simplegeo/python-oauth2)

## Usage

Visit the [Pyposterous documentation](http://thomasw.github.com/pyposterous/) site for additional information.

    import pyposterous

    # For calls that don't require authentication, you can use the module's
    # API instance:
    post = pyposterous.api.get_post(id='dJ6w')
    print "\"%s\" has been viewed %s times" % (post.title, post.views)

    # pyposttest is the posterous site I used for testing.
    for post in pyposterous.api.read_posts(hostname='pyposttest', num_posts=2):
        print "--------------------"
        print "%s - %s" % (post.title, post.url)
        if post.commentsenabled:
            print "%s comment(s)" % post.commentscount

        try:
            if post.media:
                print "\nMedia:"
            for media in post.media:
                print "* %s" % media.medium.url
        except AttributeError:
            pass # No media

        try:
            if post.comments:
                print "\nComments:"
            for comment in post.comments:
                print "* \"%s\" by %s" % (comment.body, comment.author)
        except AttributeError:
            pass # No comments
    print "--------------------"
    
Methods that require authentication will throw an exception.

    try:
        pyposterous.api.get_sites()
    except pyposterous.error.PyposterousError, e:
        print e

You'll need to instantiate your own api object to specify a username and password.

    api = pyposterous.API(username='username', password='password')

    sites = api.get_sites()
    print [site.__dict__ for site in sites] 

    tags = sites[0].get_tags()
    print [str(tag) for tag in tags]

    for post in site.read_posts(tag=tags[0]):
        post.new_comment(body="This article is tagged with %s. How neat." % tags[0])

The read\_posts results are paginated, meaning that only **num_posts** results are returned per page. That can make things tricky when you're trying to iterate over large result sets. To make it easier, you can use the Cursor class. Here's an example:

    for post in pyposterous.Cursor(method=api.read_posts, limit=50, start_page=4, parameters={'hostname':'pyposttest'}):
        print "%s -- %s" % (post.title, post.url)

The cursor object will retrieve additional pages of results as they're needed.

In order to use the Twitter based Posterous methods, you'll need to instantiate your own API object and pass it a TwitterAuth instance:

	from pyposterous.auth import TwitterAuth
	api = pyposterous.API(auth=TwitterAuth("consumer_key", "consumer_secret", "user_key", "user_secret"))
	
	post = api.upload(message="This is the title.", body="This is the post body.")
    print post.url

## Everything else
If you'd like to hire me, check out the [Match Strike](http://matchstrike.net/) site.

I looked to [Tweepy](http://github.com/joshthecoder/tweepy) a lot while writing this library. If you're working on something that needs to talk to Twitter, give it a go. You'll love it.

[urllib2_file](http://github.com/seisen/urllib2_file) saved me a lot of time and trouble. Kudos to [seisen](http://github.com/seisen).

Copyright (c) 2010 [Thomas Welfley](http://cyproject.net/). See [LICENSE](http://github.com/thomasw/pyposterous/blob/master/LICENSE) for details.
    