# Handy

Handy is a simple Django app that provides the user with a working, if
simple, search rank algorithm matching maintenance experts with the
properties they've maintained.  Handy starts with an initial dataset
provided from a CSV file.

# Installation

This script requires Python3 and Sqlite.

1. Create a new virtual environment:
```
    $ virtualenv --python=python3 handy
    $ cd handy
    $ source bin/activate ;# this is the bash instruction; use what your env demands
    $ pip install django
    $ git clone <this repository> handy
    $ cd handy ;# Yes, twice: handy/handy.
    $ rm db.sqlite3
    $ ./manage.py migrate auth admin sessions
    $ ./manage.py migrate ranksearch 0001_initial
    $ ./manage.py recoverhandy
    $ ./manage.py runserver
```
"Recoverhandy" is a custom command that imports the CSV into the
database, creating owners, properties, maintainers, and jobs
progressively.  It does a lot of 'get\_or\_create' commands, so on
SQLite it's pretty slow.

After entering the 'handy' app home, you can also

    $ ./manage.py test

This will run a simple unit test that asserts both the database
structure and client status are adequate.

# Status

**July 3, 2016**: This project is **completed**.  No new features are
being considered.  Bug reports will (probably) not be addressed.

# Process

The first thing is to understand the data.

The problem:

* A *maintainer* starts with a *score*
* For the problem space, the score is artificial
* A rating is given to a *maintainer* on a given *date*
* More precisely: The maintainer gets a set of scores in order
* The maintainer's *overall score* is:
* *score* when there are zero jobs
* *score* + (sum ratings / 10) between 1 and 9 jobs
* (sum ratings / num sits) for 10 o more jobs

Tables:
*    Property Owners
*    Properties (owner_id)
*    Maintainers 
*    Jobs (maintainer_id, property_id, start_date, end_date, rating, comments)

I'm big on slugs.  I'm *very* big on navigable and bookmarkable URLs.
If a property owner comes to like a particular maintainer, that
maintainer should have their own URL the owner can always navigate to,
to see if the maintainer is available.

I know it's bad form to write your own pagination kit, but I couldn't
help myself; it's a bit of showing off, especially with the history
thing in-lined.

# Analysis

This was *fun*.  I haven't worked in Django in almost three years, and
the things that have changed since 1.4 and within Python 3 make
development even more interesting than usual.

# Postscript

If you're reading this and you can't figure out what this is *really*
for, you probably don't need it.
