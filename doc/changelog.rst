.. _changelog:

************
ChangeLog
************

Pyposterous v0.3.2
==================
* The thumb attribute for video attachments is now a string containing the URL of the thumbnail and not an empty object. Pyposterous was trying to convert the XML element that represents this attribute to a Pyposterous Image object, but the source data was only a string (not the set of child elements that Posterous typically uses to represent images). It should be noted that the thumb and mp4 attributes for video attachments are unavailable until Posterous finishes transcoding the uploaded media.

Pyposterous v0.3.1
==================
* Fixed a Python 2.5 incompatibility that prevented Pyposterous from working in Python <2.6

Pyposterous v0.3.0
==================

* Removed old Twitter BasicAuth methods from the IDL.
* Added new Posterous api v2 Twitter upload method (which requires OAuth Echo authentication).
* Added TwitterAuth class to handle signing Twitter request with the appropriate OAuth credentials.

