.. _tutorial:


*****************
Using Pyposterous
*****************

Introduction
============

Thanks for checking out Pyposterous. If you have any issues using the library, please be sure to post something on the `project's issues page <http://github.com/thomasw/pyposterous/issues>`_.

Start by importing Pyposterous::

	import pyposterous

Unauthenticated Methods
=======================

Many of Posterous's API calls do not require authentication. If you're only using these methods, you can just use the api object that's automatically instantiated when you import the library::

	api = pyposterous.api

Here's a list of methods that you can use without authenticating:

#. :ref:`read_posts <read_posts_method>`
#. :ref:`get_tags <get_tags_method>`
#. :ref:`get_post <get_post_method>`

As you might expect, read_posts won't return private posts and get_tags won't return tags of private posts/sites if you're not authenticated.

Here's how to get all public posts tagged with 'api' from a site::

	api.read_posts(hostname='pyposttest', tag='api')
	
get_tags works in a similar way::

	api.get_tags(hostname='pyposttest')

get_post is a part of the `post.ly api <http://posterous.com/api/postly>`_ and it's a little differently. Instead of accepting a numeric post id (e.g. post.id), it accepts a post.ly short code (which will always be a string). 

The shortcode is the combination of letters and numbers following the last slash in a post.ly URL. For example, given http://post.ly/d8W2 as the post.ly url, here's the appropriate code to get the post that the URL points at::

	api.get_post(id='d8S6')

If you had the URL stored in a variable, the following would also work::

 	url = 'http://post.ly/d8W2'
	api.get_post(id=url.replace('http://post.ly/',''))
	
Authenticated Methods
=====================

Most of the fun methods require authentication. For that, a new API instance must be instantiated with a username and password. Here's how::

	api = pyposterous.API(username='username', password='password')
	
Note the difference in case from our earlier code. pyposterous.API is the class and pyposterous.api is an unauthenticated instance of the API class.

With an authenticated API instance, you can then call the following without Pyposterous raising an exception:

#. :ref:`get_sites <get_sites_method>`
#. :ref:`new_post <new_post_method>`
#. :ref:`update_post <update_post_method>`
#. :ref:`new_comment <new_comment_method>`

One of the most important authenticated method is get_sites. It returns a list of all the authenticated user's sites::

	sites = api.get_sites()
	
This method can also be used to test the validity of credentials because it will fail if the username and password combination is invalid.
	
To post a new article to one of those sites returned by get_sites, either of the following would work::

	sites[0].new_post(title="Test!", body="This is a test post. How cool.")
	
	post = api.new_post(site_id=sites[0].id, title="Test!", body="This is a test post. How cool.")

Posting a comment on that article::

	# Easy way!
	post.new_comment("This article is ridiculous.")
	
	# Hard way!
	api.new_comment(post_id=post.id, "This article is ridiculous.")
	
Updating the posted article::

	# Easy way
	post.title = "TEST TEST TEST TEST"
	post.body = "This title is so much more appropriate."
	post.update_post()
	
	# Hard way
	api.update_post(post_id=post.id, title="TEST TEST TEST TEST", body="This title is so much more appropriate.")

Data Returned
=============

All API methods (with the exception of :ref:`upload <upload_method>` and :ref:`upload_and_post <upload_and_post_method>`) will return an object or list of objects that are instances of one of following classes:

* :ref:`Post <post_class>`
* :ref:`Site <site_class>`
* :ref:`Tag <tag_class>`
* :ref:`Comment <comment_class>`

Due to Posterous API inconsistencies, instances of the same type will not always have the same set of attributes. Read, bookmark, and re-read the `Posterous API docs <http://posterous.com/api>`_, as they indicate the set of data that each API call will return.

In addition to the Post, Site, Comment, and Tag classes, there are also :ref:`Image <image_class>` and :ref:`Media <media_class>` classes. Your application will only encounter these as children of Post objects::

	# Returns a list of media instances
	post.media
	
	# Media objects with type='image', will have the following attributes:
	# Both of these attributes are Image instances
	post.media[0].medium
	post.media[0].thumbnail
	
	# You can also get Comment instances as children of posts.
	# The following Returns a list of comment instances
	post.comments
	
Some of these objects have :ref:`helper methods <helper_functions>`. For example, Post instances have a method that makes submitting updated content super easy. 

Read the :ref:`documentation about helper methods <helper_functions>`. Using these methods will make your code much cleaner.

Uploading Media
===============

Attaching media to an article is really easy. Simply pass a file object or a list of file objects to the appropriate parameter (typically 'media').

To attach an image ('images/0001.jpg') to a new post, try the following::

	test_file = open('images/00011.jpg')
	post = api.new_post(title='Testing single file upload', media=test_file)
	test_file.close()

Pyposterous can also handle cases where there are multiple media assets that need to be attached to a post. Here's an example that assumes images/ is a directory with multiple jpeg files::

	from os import listdir, path
	images = [open(path.join('images', fname)) for fname in listdir('images') if '.jpg' in fname]

	# Post the images and close them
	title = 'Multi-file upload test!'
	post = api.new_post(title=title, media=images)
	[image.close() for image in images]
	

Twitter Methods
===============

Posterous has two API calls that use Twitter credentials instead of Posterous credentials. In both cases, the functions that represent those calls require a twitter username and a twitter password as parameters.

Here's an upload example (which doesn't post a Tweet to the user's Twitter account)::

	post1 = api.upload(username='twitter_username', password='twitter_password', title="Yay", body="Body of post!")

upload_and_post works the same way, but upload_and_post will also Tweet a link to your new article using the specified twitter credentials.

Both methods return a dictionary that contains the following data::

	post1['mediaid']
	post1['mediaurl']
	
If necessary, you can retrieve a post object representing your uploaded content by using get_post::

	post1 = self.api.get_post(id=post2['mediaurl'].replace('http://post.ly/', ''))

Paginated Results (Cursor Tutorial)
===================================

Results returned by read_posts are paginated with a limited number of posts returned per page. Thus, just calling read_posts with a site specified will not necessarily return all posts on that site. In fact, it would only return the first page of results.

To make iterating over paginated result sets easier, Pyposterous includes a Cursor class.

Here's an example::

	from pyposterous import Cursor
	
	for post in Cursor(method=api.read_posts, start_page=5, parameters={'hostname':'pyposttest',}):
		print "%s -- %s" % (post.title, post.url)
		
This may seem a little tricky at first, but it's really not that bad. You just need to create a cursor object, specify which method that you want it to call to retrieve posts, and then iterate as if you were looping over a list. Your cursor object will then automatically retrieve new pages as needed. Check out the :ref:`Cursor documentation <cursor_class>` for additional information.

The only API call that returns paginated data is read_posts. This means that the Cursor class can only be used with API.read_posts and Site.read_posts. If anything else is passed to the method parameter, an exception will be raised.