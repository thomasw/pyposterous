#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="pyposterous",
      version="0.1",
      description="Posterous library for python",
      license="MIT",
      author="Thomas Welfley",
      author_email="info@matchstrike.net",
      url="http://github.com/thomasw/pyposterous",
      dependency_links=["http://github.com/thomasw/urllib2_file/tarball/master#egg=urllib2_file",],
      install_requires="urllib2_file",
      packages = find_packages(),
      keywords= "posterous library",
      zip_safe = False)
