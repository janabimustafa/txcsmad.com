txcsmad.com
=======

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/txcsmad/txcsmad.com/master/LICENSE
    :alt: MIT Licensed

The main online hub for MAD, built with Django.

* Information about MAD
* User system
* Event system with QR code check-in
* URL shortener
* Admin panel
* REST API
* UTCS lab status page
* MADcon registration

Development
-----

Local Deployment
^^^^^^^^^^^^^^^^

Get all the dependencies we'll need to run Django.
::
    # Use Homebrew for macOS. Replace with appropriate package manager for your platform
    brew install python3
    git clone git@github.com:txcsmad/txcsmad.com.git
    pip3 install -r requirements/local.txt

Install Postgres app(http://postgresapp.com/) and start Postgres.
::
    # Create the Postgres DB
    createdb mad_web
    # Populate the DB with test data
    python3 manage.py migrate

We use Gulp_ 4 for our build system. It automates the process of compiling styles and minifying static assets. To install it (and all of its dependencies) locally\:
::
    # Get
    brew install npm
    npm install gulpjs/gulp.git#4.0 --save-dev
    npm install

.. _Gulp: http://gulpjs.com

In ``config/settings``, rename ``config.template.json`` to ``config.json``. The default values should be fine for local development.

Several run configurations are available. Check ``gulpfile.js`` for more details.
::
    # Runs all build steps, then launches the site
    gulp run

Use ``gulp watch`` to automatically recompile any assets you modify in the background while you work.

Importing test data and users
^^^^^^^^^^^^^^^^^^^^^

Each app includes fixtures_. Load them with
::
    python manage.py loaddata <fixture-name>

.. _fixtures: https://docs.djangoproject.com/en/1.10/howto/initial-data/

All included test users have the password ``test``.

Running Tests
^^^^^^^^^^^^^
Just run
::
    py.test

Checking Coverage
^^^^^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report
::
    coverage run manage.py test
    coverage html
    open htmlcov/index.html


Manually manipulating data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. In the local environment, check your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

To create an **superuser account**
::
    python manage.py createsuperuser

To mark an existing account as superuser and staff
::
    psql mad_web
    mad_web# UPDATE users_user SET is_superuser = true AND is_staff = true WHERE id = 1;

Server Deployment
----------

First time
^^^^^^^^^^
Ensure that Python 3.5 and Postgres are installed, then run the below.
::
    git clone git@github.com:txcsmad/txcsmad.com.git
    pip3 install -r requirements/production.txt
    npm install
    npm install gulpjs/gulp.git#4.0 --save-dev
    npm install --global gulp-cli
    createdb mad_web
    python3 manage.py migrate

Install a `Django stack`_ on a DigitalOcean Droplet. You will need more than the base droplet as 512Mb of RAM is too little to install everything.

.. _Django stack: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

Get SSL certificates from `Let's Encrypt`_, and configure Nginx to serve them.

.. _Let's Encrypt: https://letsencrypt.org/

Rename ``config.template.json`` to ``config.json`` in ``config/settings``. The Django key should be a unique 50 character key. You can generate a new key `here`_. Make sure that you generate or retrieve the other keys as well.

.. _here: http://www.miniwebtool.com/django-secret-key-generator/

Updates
^^^^^^^
The MAD server is configured with an ``updatemad`` command, which is an alias for the below.
::
    # Update and use master ( not pull, to enforce using whatever is on master )
    git fetch
    git reset --hard origin/master

    # update pip & python packages
    pip3 install --upgrade pip
    pip3 install -r requirements/production.txt

    # update nodejs packages
    npm install

    # migrate database changes
    python3 manage.py migrate

    # Update sass and js files
    gulp

    # Gather all static files and update them
    python3 manage.py collectstatic --noinput

    # Restart server with new code::
    sudo systemctl restart gunicorn && sudo systemctl restart nginx
