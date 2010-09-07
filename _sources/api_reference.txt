.. _api_reference:


*************
API Reference
*************

Base Methods
============

These methods represent the base Posterous methods documented on the `Posterous API site <http://posterous.com/api>`_.

Reading
-------

Methods for reading data from Posterous.com. See http://posterous.com/api/reading for more information.

.. _get_sites_method:
.. automethod:: pyposterous.api.get_sites

.. _get_tags_method:
.. automethod:: pyposterous.api.get_tags

.. _read_posts_method:
.. automethod:: pyposterous.api.read_posts

Writing
-------

Methods that allow posting or commenting. See http://posterous.com/api/posting for more information.

.. _new_post_method:
.. automethod:: pyposterous.api.new_post

.. _update_post_method:
.. automethod:: pyposterous.api.update_post

.. _new_comment_method:
.. automethod:: pyposterous.api.new_comment

Post.ly
-------

Post.ly methods. See http://posterous.com/api/postly for more information.

.. _get_post_method:
.. automethod:: pyposterous.api.get_post

Twitter
-------

Posterous' Twitter methods. See http://posterous.com/api/twitter for more information.

.. _upload_method:
.. automethod:: pyposterous.api.upload

Data Classes and Helper Methods
===============================

.. _helper_functions:

Instances of the following classes are instantiated based on the data returned by Posterous. Due to inconsistencies in the Posterous API, instance attributes will vary depending on the API call that created the instance. Use `Posterous's docs <http://posterous.com/api>`_ as an attribute reference.

Many of the classes include helper functions that make working with Pyposterous cleaner than solely relying on the Base API methods. You should use the helper methods below whenever possible.

.. _post_class:
.. autoclass:: pyposterous.models.Post
	:members:

.. _site_class:
.. autoclass:: pyposterous.models.Site
	:members:

.. _tag_class:
.. autoclass:: pyposterous.models.Tag
	:members:

.. _comment_class:
.. autoclass:: pyposterous.models.Comment
	:members:

.. _media_class:
.. autoclass:: pyposterous.models.Media
	:members:

.. _image_class:
.. autoclass:: pyposterous.models.Image
	:members:

.. _user_class:
.. autoclass:: pyposterous.models.User
	:members:

Cursor
======

.. _cursor_class:
.. autoclass:: pyposterous.cursor.Cursor

Exceptions
==========

.. autoexception:: pyposterous.error.PyposterousError
	
	.. attribute:: error_code
	.. attribute:: error_message

