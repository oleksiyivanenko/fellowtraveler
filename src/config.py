import os

DEBUG = bool(os.getenv('FT_DEBUG', False))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'postgresql://postgres:root@localhost/fellowtraveler'
)
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.getenv('FT_CSRF_SESSION_KEY', os.urandom(24).encode('hex'))

SECRET_KEY = os.getenv('FT_SECRET_KEY', os.urandom(24).encode('hex'))
