"""Django development settings
"""

from .base import *
from ._generate_secret_key import generate_secret_key
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

print('Loading development settings')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# We're using the SECRET_KEY stored in "development.key", otherwise we're generating a new one:
key_file = path.join(here, 'development.key')
if os.path.exists(key_file):
    with open(key_file, 'r') as f:
        SECRET_KEY = f.read().strip()
else:
    # key_file does not exist:
    SECRET_KEY = None

# Key file does not exist or is empty:
if not SECRET_KEY:
    print('Generating new secret key')
    SECRET_KEY = generate_secret_key()
    with open(key_file, 'w') as f:
        f.write(SECRET_KEY)
else:
    print('Using the secret key stored in "{}"'.format(key_file))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# Queue

Q_CLUSTER = {
    'sync': True,
    'orm': 'default',
}
