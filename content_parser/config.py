import os
import sys
import logging

# Define logging level
LOG_LEVEL = logging.DEBUG

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Application threads.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = '87a089hlpquvc54fjr4obhnqz6439hfyxiorsdew'

# Secret key for signing cookies
SECRET_KEY = CSRF_SESSION_KEY

# Disable 404 help
ERROR_404_HELP = False

PARSERS_PACKAGE = 'parsers'
RESOURCES_DIR = '/tmp/'

# DB
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}?timeout=20'.format(os.path.join(BASE_DIR, 'app.db'))
# Celery
BROKER_URL = 'sqla+{}'.format(SQLALCHEMY_DATABASE_URI)
CELERY_RESULT_BACKEND = 'db+{}'.format(SQLALCHEMY_DATABASE_URI)
# Run crawler every N seconds
CELERY_PROCESS_TIMEDELTA_SECONDS = 10
CELERY_CHECK_TIMEDELTA_SECONDS = 300
