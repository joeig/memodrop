edupy
=====

Rapid learning process for people with tight schedules. Implementation of [flash cards](https://en.wikipedia.org/wiki/Flashcard) in Python 3 and Django.

[![Build Status](https://travis-ci.org/joeig/edupy.svg?branch=master)](https://travis-ci.org/joeig/edupy)

Features
--------

### Implementation of the Leitner system

Improve your learning effectiveness using the [Leitner system](https://en.wikipedia.org/wiki/Leitner_system). It uses a simple algorithm that asks you for cards in the first areas more frequently. Correctly answered cards are moved to the next area. Incorrectly answered cards are moved back to the previous area ("defensive mode") or first area ("strict mode").

### Categories

Organize your flash cards in categories and find faster what you're looking for.

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

1. Install Python 3.6 or `docker pull joeig/edupy`
2. You may want to create a virtual environment
3. Install the dependencies: `pip install -r requirements.txt`
4. Production preparation: Copy `edupy/settings/production.py.dist` to `edupy/settings/production.py` and adjust the values
5. Create a database or let Django do that for you (it will choose SQLite3 by default)
6. Migrate the database: `python manage.py migrate [--settings edupy.settings.production]`
7. Create a super-user account: `python manage.py createsuperuser [--settings edupy.settings.production]`
8. Start the application as WSGI (alternative for developers: `python manage.py runserver [--settings edupy.settings.production]`)

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

Setup the development environment:

~~~ bash
pip install -r requirements.txt
pip install -r requirements_dev.txt
~~~

There are some fixtures for different scenarios:

~~~ bash
python manage.py loaddata demo_users
python manage.py loaddata demo_categories
python manage.py loaddata demo_cards
~~~

Feel free to write and run some unit tests after you've finished your work.

~~~ bash
coverage run manage.py test .
coverage report
~~~
