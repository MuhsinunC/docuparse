# backend/app/api/v1/endpoints/__init__.py

# Import the router objects from each endpoint file
from . import parse
from . import upload
from . import extract
from . import split
from . import webhooks
from . import jobs

# (Optional) Define __all__ if you want to control what 'from .endpoints import *' does
# __all__ = ['parse', 'upload', 'extract', 'split', 'webhooks', 'jobs'] 