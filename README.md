memodrop
========

Rapid learning process for people with tight schedules. Implementation of [flash cards](https://en.wikipedia.org/wiki/Flashcard) in Python 3 and Django.

[![Build Status](https://travis-ci.org/joeig/memodrop.svg?branch=master)](https://travis-ci.org/joeig/memodrop)

Features
--------

### Implementation of the Leitner system

Improve your learning effectiveness using the [Leitner system](https://en.wikipedia.org/wiki/Leitner_system). It uses a simple algorithm that asks you for cards in the first areas more frequently. Correctly answered cards are moved to the next area. Incorrectly answered cards are moved back to the previous area ("defensive mode") or first area ("strict mode").

### Collaborative categories

Organize your flash cards in categories and find faster what you're looking for. You can even share your categories with your classmates!

### Flash cards with hints

You don't have any clue what your flash card is talking about? No problem, just write short clues and display them if you need to.

### Responsive interface

Use these features on your mobile phone or tablet as well!

### Multi-user

Create personalized user accounts for your friends with their own categories and cards.

### REST API

If you intend to migrate your existing cards, just use the `/api/categories/` and `/api/cards/` endpoints.

Screenshots
-----------

* [Braindump session page](/docs/screenshots/braindump_session.png?raw=true)
* [Braindump session page (mobile optimized)](/docs/screenshots/braindump_session_mobile.png?raw=true)
* [Index page](/docs/screenshots/braindump_index.png?raw=true)
* [Category detail page](/docs/screenshots/category_detail.png?raw=true)

Installation
------------

### Docker setup

~~~ bash
docker pull joeig/memodrop:latest
docker run -d -p 8000:8000 joeig/memodrop:latest
~~~

This command starts a standalone web service with a local SQlite database in development mode. In this case, the database file is part of the container volume.

**A few words about production usage:** You should mount a custom settings file to `memodrop/settings/production.py` (template: `production.py.dist`) containing the configuration for an external DBMS like PostgreSQL or MySQL. Also consider to use the WSGI interface instead of the standalone web service.

Run the production container like this:

~~~ bash
docker run -d -v /path/to/your/production.py:/usr/src/app/memodrop/settings/production.py:ro -e DJANGO_SETTINGS_MODULE=memodrop.settings.production -p 8000:8000 joeig/memodrop:latest
~~~

Now proceed to create the initial super-user:

~~~ bash
docker exec -ti <container ID> python manage.py createsuperuser
~~~

### Manual setup

1. Install Python 3.6
2. You may want to create a virtual environment now
3. Install the dependencies: `python setup.py install`
4. Production preparation: Copy `memodrop/settings/production.py.dist` to `memodrop/settings/production.py` and adjust the values
5. Create a database or let Django do that for you (it will choose SQLite3 by default)
6. Migrate the database: `python manage.py migrate [--settings memodrop.settings.production]`
7. Create a super-user account: `python manage.py createsuperuser [--settings memodrop.settings.production]`
8. * Start the application as WSGI
   * Alternative: Start the standalone web service: `python manage.py runserver [--settings memodrop.settings.production]`

Create regular user accounts
----------------------------

You can do this with super-user permissions in Django's administration interface (`/admin/`).

API Authorization
-----------------

The API needs a user-specific token to authorize requests. This is accomplished by dispatching an `Authorization: Token <token>` header with all API requests.

Tokens are user-specific and can be optained by perfoming a POST request containing the username and password to the authorization endpoint `/api/auth-token/`. Example:

~~~ text
$ curl -X POST --data "username=<username>&password=<password>" "http://127.0.0.1:8000/api/auth-token/"
{
    "token": "091c4c1204422cb682cc9426d097d492a56a2013"
}
~~~

Contribution
------------

### Setup

Setup the development environment:

~~~ bash
python setup.py develop
pip install -e ".[dev]"
~~~

There are some fixtures for different scenarios:

~~~ bash
python manage.py loaddata demo_users  # use demo credentials from categories/fixtures/demo_users.yaml
python manage.py loaddata demo_categories
python manage.py loaddata demo_share_contracts
python manage.py loaddata demo_cards
~~~

### Test

Feel free to write and run some unit tests after you've finished your work.

~~~ bash
coverage run manage.py test .
coverage report
flake8
~~~

### Release

Commit and tag your work (following the [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) guidelines):

~~~ bash
bumpversion patch  # use major, minor or patch
git push origin master --tags
~~~
