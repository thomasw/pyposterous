"""
Pyposterous API Library.
"""
__version__ = '0.1'
__author__ = 'Thomas Welfley'
__license__ = 'MIT'

from pyposterous.api import API
from pyposterous.cursor import Cursor

# Unauthenticated instance of the API
api = API()