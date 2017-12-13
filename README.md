edupy
=====

Implementation of [flash cards](https://en.wikipedia.org/wiki/Flashcard) in Python 3 and Django.

Features
--------

### Implementation of the Leitner system

Improve your learning effectiveness using the [Leitner system](https://en.wikipedia.org/wiki/Leitner_system). It uses a simple algorithm that asks you for cards in the first areas more frequently. Correctly answered cards are moved to the next area. Incorrectly answered cards are moved back to the previous or first area.

### Categories

Organize your flash cards in categories and find faster what you're looking for.

### Flash cards with hints

You don't have any clue what your flash card is talking about? No problem, just write short clues and display them if you need to.

### Responsive interface

Use these features on your mobile phone or tablet as well!

Installation
------------

1. Install Python 3.6 or use Docker
2. You may want to create a virtual environment
3. Install the dependencies: `pip install -r requirements.txt`
4. Production preparation: Copy `edupy/settings.py` to `edupy/settings_prod.py` and adjust the values (change `SECRET_KEY`, set `DEBUG` to `False`, define your database setup etc.)
5. Create a database or let Django do that for you (it will choose SQLite3 by default)
6. Migrate the database: `python manage.py migrate [--settings edupy.settings_prod]`
7. Start the application as WSGI (alternative for developers: `python manage.py runserver [--settings edupy.settings_prod]`)

Development
-----------

Feel free to run some unit tests: `python manage.py test`
