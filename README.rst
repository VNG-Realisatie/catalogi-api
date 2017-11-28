

.. image:: https://requires.io/bitbucket/maykinmedia/ztc/requirements.svg?branch=master
     :target: https://requires.io/bitbucket/maykinmedia/ztc/requirements/?branch=master
     :alt: Requirements Status

Project layout
==============

The project layout was made in such a way that code is seperated from non-code
files that you typically want to serve in another way (static and media files)
or keep in a different location (like the virtual environment)::

    ztc
    |
    +-- bin                 -- Useful scripts (mostly for developers).
    |
    +-- build               -- All Gulp tasks.
    |
    +-- doc                 -- Documentation source and generated files.
    |
    +-- env                 -- Virtual environment files.
    |
    +-- log                 -- All log files are stored here.
    |
    +-- media               -- Default location for uploaded media files.
    |
    +-- requirements        -- Project requirements for each type of installation.
    |
    +-- src                 -- Container for one or more source directories.
    |   |
    |   +-- ztc
    |       |
    |       +-- conf        -- Django settings files.
    |       |
    |       +-- js          -- JavaScript source files.
    |       |
    |       +-- sass        -- Sass (css pre-processor) source files.
    |       |
    |       +-- static      -- Default location for project static files.
    |       |
    |       +-- templates   -- Project templates.
    |       |
    |       +-- test        -- Automated tests.
    |       |
    |       +-- utils       -- Project-wide utility functions.
    |       |
    |       +-- ...         -- Project specific applications.
    |
    +-- static              -- Default location for collected static files.


Installation
============

New installations (for development or production) should follow the steps
below.

1. Navigate to the location where you want to place your project.

2. Get the code::

    $ git clone ssh://git@bitbucket.org/maykinmedia/ztc.git
    $ cd ztc

3. Bootstrap the virtual environment and install all required libraries. The
   ``bootstrap.py`` script basically sets the proper Django settings file to be
   used::

    $ python bootstrap.py <production|staging|test|dev>

4. Activate your virtual environment and create the statics and database::

    $ source env/bin/activate
    $ python src/manage.py collectstatic --link
    $ python src/manage.py migrate


Developers
----------

Optionally, you can load demo data and extract demo media files::

    $ python src/manage.py loaddata demo
    $ cd media
    $ tar -xzf demo.tgz

You can now run your installation and point your browser to the address given
by this command::

    $ python src/manage.py runserver

If you are making local, machine specific, changes, add them to
``src/ztc/conf/local.py``. You can base this file on
the example file included in the same directory.

Install the front-end CLI tools if you've never installed them before::

    $ npm install -g gulp
    $ npm install

Enable watch tasks::

    $ gulp

By default this will compile the sass to css on every sass file save.

For more information on SASS, see: http://sass-lang.com/.
For more information on Node.js, see: http://nodejs.org/.


Staging and production
----------------------

See https://bitbucket.org/maykinmedia/maykin-deployment/ on how to enable
Ansible deployments.


Update installation
===================

When updating an existing installation:

1. Activate the virtual environment::

    $ cd ztc
    $ source env/bin/activate

2. Update the code and libraries::

    $ git pull
    $ pip install -r requirements/<production|staging|test|dev>.txt
    $ npm install

3. Update the statics and database::

    $ python src/manage.py collectstatic --link
    $ python src/manage.py migrate
