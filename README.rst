maceoutliner
============

**NOT READY FOR USE YET**

A story structure outliner loosely based on Mary Robinette Kowal’s MACE
nesting, Dan Well’s presentations on seven point story structure, and
any hundred other outlining suggestions I’ve come across over the last
few years.

|CircleCI| |Coverage Status| |Documentation Status| |Built with Cookiecutter Django|

License
    BSD

Settings
--------

Moved to
`settings <http://cookiecutter-django.readthedocs.io/en/latest/settings.html>`__.

Basic Commands
--------------

Setting Up Your Users
~~~~~~~~~~~~~~~~~~~~~

-  To create a **normal user account**, just go to Sign Up and fill out
   the form. Once you submit it, you’ll see a “Verify Your E-mail
   Address” page. Go to your console to see a simulated email
   verification message. Copy the link into your browser. Now the user’s
   email should be verified and ready to go.
-  To create an **superuser account**, use this command:

::

       $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and
your superuser logged in on Firefox (or similar), so that you can see
how the site behaves for both kinds of users.

Test coverage
~~~~~~~~~~~~~

To run the tests, check your test coverage, and generate an HTML
coverage report:

::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ py.test

Live reloading and Sass CSS compilation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Moved to `Live reloading and SASS
compilation <http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html>`__.

Django-q
~~~~~~~~

This app comes with Django-Q for handling asyncronous tasks.

To run a the worker cluster use Django’s management command.

.. code:: 

    cd maceoutliner
    python manage.py qcluster

Email Server
~~~~~~~~~~~~

In development, it is often nice to be able to see emails that are being
sent from your application. If you choose to use
`MailHog <https://github.com/mailhog/MailHog>`__ when generating the
project a local SMTP server with a web interface will be available.

To start the service, make sure you have nodejs installed, and then type
the following:

.. code::

    $ npm install
    $ grunt serve

(After the first run you only need to type ``grunt serve``) This will
start an email server that listens on ``127.0.0.1:1025`` in addition to
starting your Django project and a watch task for live reload.

To view messages that are sent by your application, open your browser
and go to ``http://127.0.0.1:8025``

The email server will exit when you exit the Grunt task on the CLI with
Ctrl+C.

Sentry
~~~~~~

Sentry is an error logging aggregator service. You can sign up for a
free account at https://sentry.io/signup/?code=cookiecutter or download
and host it yourself. The system is setup with reasonable defaults,
including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

Deployment
----------

The following details how to deploy this application.

Heroku
~~~~~~

See detailed `cookiecutter-django Heroku
documentation <http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html>`__.

.. |CircleCI| image:: https://circleci.com/gh/maceoutliner/maceoutliner.svg?style=svg
   :target: https://circleci.com/gh/maceoutliner/maceoutliner
.. |Coverage Status| image:: https://coveralls.io/repos/github/maceoutliner/maceoutliner/badge.svg
   :target: https://coveralls.io/github/maceoutliner/maceoutliner
.. |Documentation Status| image:: https://readthedocs.org/projects/maceoutliner/badge/?version=latest
   :target: http://maceoutliner.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |Built with Cookiecutter Django| image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
   :target: https://github.com/pydanny/cookiecutter-django/
